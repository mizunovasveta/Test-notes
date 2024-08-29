FROM postgres:latest

ENV POSTGRES_USER=default_user
ENV POSTGRES_PASSWORD=default_password
ENV POSTGRES_DB=default_db

CMD ["postgres"]
