FROM python:3
ENV PYTHONUNBUFFERED=1
RUN mkdir /local
ADD /PruebaTecnica /local
RUN pip install -r /local/config/requirements.txt
WORKDIR /local

