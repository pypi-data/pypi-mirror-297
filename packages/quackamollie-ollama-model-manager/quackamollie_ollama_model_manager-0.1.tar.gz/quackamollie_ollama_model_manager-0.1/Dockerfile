ARG PROXY_REGISTRY=
FROM ${PROXY_REGISTRY}python:3.10-alpine as base


### Builder ###
FROM base as builder

RUN mkdir /install
WORKDIR /install

COPY ./dist/* /dist/

RUN pip install --upgrade pip setuptools wheel
RUN pip install --no-warn-script-location --prefix=/install /dist/*.whl


### Release ###
FROM registry.gitlab.com/forge_of_absurd_ducks/quackamollie/lib/quackamollie_core:latest

COPY --chown=root:root --from=builder /install /usr/local

ENTRYPOINT ["quackamollie"]
CMD ["-vv", "serve"]
