FROM python:latest

WORKDIR /app

ADD build /app
ADD writer.py /app

RUN pip install --trusted-host pypi.python.org -r requirements.txt
RUN apt-get update
RUN apt-get -y install vim

CMD ["python", "writer.py"]
