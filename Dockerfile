FROM python:3.12-slim

WORKDIR /app

RUN pip install --no-cache-dir flask==3.0.3

COPY server.py index.html ./

RUN mkdir -p /data && chown -R 1000:1000 /app /data

USER 1000:1000
EXPOSE 5000

CMD ["python", "server.py"]
