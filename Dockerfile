FROM python:3.7
COPY . /app
WORKDIR /app
# RUN pip install --trusted-host pypi.python.org -r requirements.txt
RUN pip install -r requirements.txt
CMD ["python", "app.py"]