FROM python:3.9.10-slim

COPY main.py utils.py requirements.txt ./

RUN pip install -r requirements.txt

CMD python main.py