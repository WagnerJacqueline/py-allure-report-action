FROM openjdk:8-jre-alpine
COPY --from=python:3 /  /

ARG RELEASE=2.13.8
ARG ALLURE_REPO=https://repo.maven.apache.org/maven2/io/qameta/allure/allure-commandline
ADD . /app
WORKDIR /app

RUN apk add curl

RUN curl -s -o /tmp/allure-$RELEASE.tgz $ALLURE_REPO/$RELEASE/allure-commandline-$RELEASE.tgz \
  && tar zxf /tmp/allure-$RELEASE.tgz -C /\
  && rm -rf /tmp/*

RUN rm -rf /var/cache/apk/*

RUN chmod -R +x /allure-$RELEASE/bin

ENV PATH=$PATH:/allure-$RELEASE/bin

RUN pip install --target=/app requests

ENV PYTHONPATH /app
CMD ["python", "/app/main.py"]