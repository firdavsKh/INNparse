FROM python:3.10-alpine
WORKDIR /INNPARSE
COPY requirements.txt /INNPARSE
RUN pip install -r requirements.txt
EXPOSE 3000
COPY . .
CMD ["python", "./index.py"]