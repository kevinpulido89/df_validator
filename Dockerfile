FROM python:3.9.18-slim

LABEL Name=Streamlit_Frontend_8080 Version=1.0.1

WORKDIR /app

ARG password

ENV PYTHONDONTWRITEBYTECODE=1\
    PYTHONUNBUFFERED=1 \
    KP_PASS=$password

COPY requirements.txt .

RUN pip install -r requirements.txt
#--no-cache-dir --upgrade
COPY . .

EXPOSE 8080

CMD ["streamlit" , "run", "st_front.py", "--server.port", "8080"]

#docker build --pull --rm -f "Dockerfile" -t dfvalidator:latest "."