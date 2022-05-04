FROM python:3

MAINTAINER "nv.noelvalent@gmail.com"

RUN apt-get update \
	&& apt-get install -y --no-install-recommends \
		postgresql-client \
	&& rm -rf /var/lib/apt/lists/*

COPY . /opt/hciwdcw2

WORKDIR /opt/hciwdcw2

RUN pip install -r requirements.txt

RUN python manage.py makemigrations
RUN python manage.py migrate

ENV DJANGO_SUPERUSER_PASSWORD lecturer
ENV DJANGO_SUPERUSER_EMAIL lecturer@example.com
ENV DJANGO_SUPERUSER_USERNAME lecturer

RUN python manage.py loaddata ./initial_backup_data.json
RUN python manage.py loaddata ./init.json

RUN python manage.py createsuperuser \
    --noinput \
    --username $DJANGO_SUPERUSER_USERNAME \
    --email $DJANGO_SUPERUSER_EMAIL

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
