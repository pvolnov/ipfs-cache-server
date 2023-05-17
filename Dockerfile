FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8
WORKDIR /workdir
COPY . .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt


#CMD ["python", "src/run_web.py"]
