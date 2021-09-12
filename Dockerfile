FROM python:3.8.5
WORKDIR /code
COPY .  .
COPY requirements/ requirements/
RUN python -m pip install --upgrade pip
RUN pip install -r requirements/develop.txt
CMD python manage.py runserver 0.0.0.0:8000
