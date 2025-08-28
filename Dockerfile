FROM python:alpine3.21

RUN apk add --no-cache gcc musl-dev libffi-dev python3-dev

RUN pip install names-dataset unidecode pandas

WORKDIR /app

CMD ["python3"]
