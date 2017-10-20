FROM python:3.6
RUN apt-get update && apt-get -y install build-essential && apt-get clean
ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt
ADD . /code
WORKDIR /code
CMD ["python", "app.py"]
