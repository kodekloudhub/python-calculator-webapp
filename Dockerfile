FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
COPY python_calc.py .
COPY src/calc.py ./src/

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 80
CMD ["python", "python_calc.py"]