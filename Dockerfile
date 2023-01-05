FROM python:3.9
RUN mkdir /app
WORKDIR /app
RUN mkdir BlockChain
COPY BlockChain BlockChain
COPY pyproject.toml .
COPY poetry.lock .

ENV PYTHONPATH=${PYTHONPATH}:${PWD}
RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev

RUN mkdir Keys
COPY Keys/PublicKey.pem Keys
COPY config.py .
COPY settings.toml .

ENV SINGULARITY_ORIGIN_IP="host.docker.internal"
ENV SINGULARITY_HOST_PORT=10001
ENV SINGULARITY_HOST_API_PORT=5000
EXPOSE 10001
EXPOSE 5000

CMD ["python3", "-u", "-m", "BlockChain.Application"]