FROM python:alpine3.10
COPY . /opt
WORKDIR /opt
RUN pip install -r requirements.txt
EXPOSE 18000/tcp
ENTRYPOINT ["python","/opt/darp-exporter.py"]


