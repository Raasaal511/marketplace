FROM python:3.11.0-bullseye

WORKDIR /marketplace

COPY ./marketplace_app /marketplace/marketplace_app
COPY ./requirements.txt /marketplace/requirements.txt

RUN pip install --no-cache-dir --upgrade -r ./requirements.txt

COPY . /marketplace

CMD ["uvicorn", "marketplace_app.main:app", "--host", "0.0.0.0", "--port", "8000"]

