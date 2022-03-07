FROM python:latest
# The layers have been optimized to reduce rebuilding.
RUN apt-get -y -qq update
RUN apt-get -y -qq upgrade
RUN pip3 install --upgrade pip
WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
RUN pip install --upgrade  -q -r /code/requirements.txt
RUN mkdir /code/logs

# This can be done a number of ways including in docker-compose. You can also completely ignore the configuration and use defaults.
COPY ./config.json /code/config.json
COPY ./app /code/app

CMD ["python", "./app/app.py"]