FROM kennethreitz/pipenv
ENV PORT '5000'
COPY . /app
CMD python3 app.py
EXPOSE 5000