FROM python3.7-slim

WORKDIR /app

ADD ./app

RUN pip install -trusted-host pypi.python.org -r requirements.txt

ENV GOOGLE_APPLICATION_CREDENTIALS="/app/docker-kubernetes-370811-f49003f1ee92.json"

CMD ["python", "ga4-test"]