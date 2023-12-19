FROM python:3.10

WORKDIR /app

COPY lib/ lib/
COPY assets/ assets/
COPY main.py .
COPY requirements.txt .

RUN ["pip", "install", "--upgrade", "pip"]
RUN ["pip", "install", "-r", "requirements.txt"]

ENV OPENAI_SECRET_KEY ""
ENV REDIS_HOST "127.0.0.1"
ENV REDIS_PORT ""

EXPOSE 8080

CMD ["python", "main.py"]