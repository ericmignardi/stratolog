FROM python:3.9

WORKDIR /stratolog

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . /stratolog

CMD [ "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80" ]