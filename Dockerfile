FROM python:3.8-alpine

WORKDIR / 

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

COPY requirements.txt requirements.txt
RUN apk add --no-cache gcc musl-dev linux-headers
RUN pip install -r requirements.txt

COPY . .

CMD ["python3", "-m", "plants.web_app"]
