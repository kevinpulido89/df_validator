FROM python:3.9.17-slim

LABEL Name=Streamlit_Frontend_8080 Version=1.0.1

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1\
    PYTHONUNBUFFERED=1

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .

EXPOSE 8080

CMD ["streamlit" , "run", "st_front.py", "--server.port", "8080"]

#docker build --pull --rm -f "Dockerfile" -t dfvalidator:latest "."