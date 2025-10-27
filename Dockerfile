FROM python:3.13.9-alpine3.22

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt /app/
RUN pip3 install --upgrade pip \
    && pip3 install -r requirements.txt --trusted-host pypi.org --trusted-host files.pythonhosted.org

COPY ./core /app/