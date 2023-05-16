FROM python:3.8

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

COPY req.txt /app/
RUN pip install -r req.txt

COPY core/ /app/core/
#COPY media/ /app/media/
COPY shelterWebApp/ /app/shelterWebApp/
#COPY static/ /app/static/
#COPY templates/ /app/templates/
COPY manage.py /app/

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]