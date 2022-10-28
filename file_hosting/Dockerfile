FROM python:3.10-slim-buster
WORKDIR /code
COPY requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY . /code
CMD ["uvicorn", "api.main:api", "--reload", "--port", "65432",  "--host", "0.0.0.0"]
