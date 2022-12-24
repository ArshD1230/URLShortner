FROM python:latest
 
WORKDIR /app

ADD build /app
ADD urlshortner /app

RUN pip install --trusted-host pypi.python.org -r requirements.txt
RUN apt-get update
RUN apt-get -y install vim

EXPOSE 80

CMD ["python", "app.py"]
