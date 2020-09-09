FROM python:3.7
WORKDIR /usr/app
COPY requirements.txt ./
RUN ["pip3", "install", "-r", "requirements.txt"]
COPY app ./app
ENV PYTHONPATH .
CMD ["python", "/usr/app/app/main.py", "run", "--reload"]
