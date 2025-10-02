FROM python:3.11-alpine

WORKDIR /app

RUN apk add --no-cache gcc musl-dev linux-headers
RUN pip install --no-cache-dir flask==3.0.3

COPY . .

EXPOSE 8080

CMD ["python", "server.py"]