FROM python:3.9.18-slim

WORKDIR /app

ARG password \
    msg

ENV PYTHONDONTWRITEBYTECODE=1\
    PYTHONUNBUFFERED=1 \
    KP_PASS=$password \
    KP_MSG=$msg

COPY requirements.txt .

RUN python -m pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8080

CMD streamlit run st_front.py --server.port 8080
#docker build --build-args password=no-real-pass --build-args msg=no-real-msg --pull --rm -f "Dockerfile" -t dfvalidator:latest "."