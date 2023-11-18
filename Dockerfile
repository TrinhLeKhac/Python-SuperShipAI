FROM python:3.9

# create FastAPI
WORKDIR /usr/src/supership_ai

# set work directory
WORKDIR /supership_ai

# set env variables
ENV PYTHONDONTWRITTERBYTECODE
ENV PYTHONUNBUFFERED 1
