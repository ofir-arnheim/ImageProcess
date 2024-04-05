FROM python:alpine

COPY webserver.py .
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "webserver.py"]

EXPOSE 20000