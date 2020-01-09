FROM ubuntu:18.04


COPY . /app
WORKDIR /app

RUN apt-get update && apt-get install -y \
        software-properties-common
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt-get update && apt-get install -y \
	python3.7 \
	python3-pip
RUN python3.7 -m pip install pip
RUN pip3 install -r /app/requirements.txt 

CMD ["python3", "Predictor.py"]

