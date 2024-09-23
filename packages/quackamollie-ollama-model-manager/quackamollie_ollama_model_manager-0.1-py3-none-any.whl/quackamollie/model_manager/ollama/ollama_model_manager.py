# -*- coding: utf-8 -*-
__all__ = ["OllamaQuackamollieModelManager"]
__author__ = "QuacktorAI"
__copyright__ = "Copyright 2024, Forge of Absurd Ducks"
__credits__ = ["QuacktorAI"]

import aiohttp
import json

from quackamollie.core.cli.settings import get_settings_from_context, QuackamollieSettings
from quackamollie.core.database.model import ChatMessage
from quackamollie.core.enum.model_family_icon import ModelFamilyIcon
from quackamollie.core.enum.user_type import UserType
from quackamollie.core.meta.model.meta_quackamollie_model import MetaQuackamollieModel
from quackamollie.core.meta.model_manager.meta_quackamollie_model_manager import MetaQuackamollieModelManager
from typing import AsyncIterable, Dict, List, Optional, Tuple, Type


class OllamaQuackamollieModelManager(MetaQuackamollieModelManager, MetaQuackamollieModel):
    """ Model manager managed by the `QuackamollieModelManagerRegistry` and serving models from the Ollama API """

    families: List[ModelFamilyIcon] = [ModelFamilyIcon.LLAMA]
    _raw_model_list: None | List = None

    @classmethod
    async def get_raw_model_list(cls) -> List:
        if cls._raw_model_list is None:
            quackamollie_settings: QuackamollieSettings = get_settings_from_context()
            url = f"{quackamollie_settings.ollama_base_url}/api/tags"

            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        data = await response.json()
                        cls._raw_model_list = data["models"]
                    else:
                        cls._raw_model_list = []
        return cls._raw_model_list

    @classmethod
    async def get_model_list(cls) -> List[str]:
        """ Discover the models available for the model manager at runtime asynchronously

            :return: A list of available models for the model manager
            :rtype: List[str]
        """
        if cls._model_list is None:
            raw_model_list = await cls.get_raw_model_list()
            cls._model_list = [model["name"] for model in raw_model_list]
        return cls._model_list

    @classmethod
    async def get_model_families(cls) -> Dict[str, List[ModelFamilyIcon]]:
        """ Discover the models families available for the model manager at runtime asynchronously

            :return: A dict with values the list of families indexed by model name
            :rtype: Dict[str, List[ModelFamilyIcon]]
        """
        if cls._model_families is None:
            raw_model_list = await cls.get_raw_model_list()
            cls._model_families = {}

            for model in raw_model_list:
                model_name = model["name"]
                model_families: List[ModelFamilyIcon] = [ModelFamilyIcon.DEFAULT]
                if model["details"]["families"]:
                    model_icon = {"llama": ModelFamilyIcon.LLAMA, "clip": ModelFamilyIcon.MULTIMODAL}
                    try:
                        model_families = [model_icon[family] for family in model['details']['families']]
                    except KeyError:
                        # Use a default value when the key is not found
                        model_families = [ModelFamilyIcon.DEFAULT]

                cls._model_families[model_name] = model_families
        return cls._model_families

    @classmethod
    def parse_chat_history(cls, chat_messages: Optional[List[ChatMessage]]) -> List[Dict]:
        """ Parse the chat history given as a list of `ChatMessage` from the database model to a list compatible with
            the model manager's models.

            :param chat_messages: A list of `ChatMessage` from the database model
            :param chat_messages: Optional[List[ChatMessage]]

            :return: A list of messages formatted to be compatible with the model manager's models.
            :rtype: List[Dict]
        """
        chat_history: List[Dict] = []

        # Construct the list of messages in a format supported by Ollama
        if chat_messages:
            for past_msg in chat_messages:
                chat_history.append({
                    "role": past_msg.user.user_type.value,
                    "content": past_msg.content,
                    "images": []
                })

        return chat_history

    @classmethod
    async def get_model_class(cls, model_name: str) -> Optional[Type[MetaQuackamollieModel]]:
        """ Get the model class from the model name

            :param model_name: Name of the model as listed by `cls.get_model_list`
            :type model_name: str

            :return: A subclass of MetaQuackamollieModel
            :rtype: Optional[Type[MetaQuackamollieModel]]
        """
        if model_name in await cls.get_model_list():
            return cls
        else:
            return None

    @classmethod
    def reset(cls):
        """ Reset the model manager dynamic fields to force reloading models. Be careful if used asynchronously """
        cls._raw_model_list = None
        cls._model_list = None
        cls._model_families = None

    @classmethod
    async def astream_answer(cls, content: str, chat_history: List, model_config: Optional[str] = None,
                             model_name: Optional[str] = None, images_base64: Optional[List[str]] = None,
                             **kwargs) -> AsyncIterable[Tuple[str, bool]]:
        """ Asynchronous iterator to stream the answer from a LLM model

            :param content: The new message content
            :type content: str

            :param chat_history: A list of past messages formatted accordingly by model manager
            :type chat_history: List

            :param model_config: Additional configuration given as a string through CLI or Telegram `App Settings`
                                 and retrieved from the database
            :type model_config: Optional[str]

            :param model_name: Name of the model as listed by `cls.get_model_list`
            :type model_name: Optional[str]

            :param images_base64: A list of images formatted as base64 strings
            :type images_base64: Optional[List[str]]

            :param kwargs: Additional streaming arguments
            :type kwargs: kwargs

            :return: An asynchronous iterator giving a tuple containing the new chunk and a boolean indicating
                     if the model is done or not
            :rtype: AsyncIterable[Tuple[str, bool]]
        """
        # Add the current message to the list of past messages and finish building the payload
        chat_history.append(dict(role=UserType.user.value, content=content,
                                 images=[] if images_base64 is None else images_base64))

        # Build the payload for Ollama aiohttp request
        payload = {
            "model": model_name,
            "messages": chat_history,
            "stream": True,
        }

        # Build the Ollama API URL from the config
        quackamollie_settings: QuackamollieSettings = get_settings_from_context()
        ollama_api_url = f"{quackamollie_settings.ollama_base_url}/api/chat"

        # Iterate through the stream of answers given by Ollama from API
        async with aiohttp.ClientSession() as session:
            async with session.post(ollama_api_url, json=payload) as response:
                async for chunk in response.content:
                    if chunk:
                        decoded_chunk = chunk.decode()
                        if decoded_chunk.strip():
                            stream_data = json.loads(decoded_chunk)

                            # Parse the JSON of the request to get chunk and is_done
                            msg = stream_data.get("message", None)
                            if msg is None:
                                chunk = ""
                            else:
                                chunk = msg.get("content", "")
                            is_done = stream_data.get("done", False)

                            yield chunk, is_done
