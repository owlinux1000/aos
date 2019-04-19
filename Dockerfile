FROM python:3.7.0
LABEL maintainer=encry1024
ADD ./ /root
WORKDIR /root
RUN pip install pipenv && pipenv install
EXPOSE 8000
ENTRYPOINT ["pipenv", "run", "python", "main.py"]
