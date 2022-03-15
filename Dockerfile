FROM python:3.8

RUN apt-get update && apt-get install -y python3-pip

RUN pip install pipenv

COPY . /projects

WORKDIR /projects

RUN pipenv install --system --deploy --ignore-pipfile

ENV PYTHONPATH "${PYTHONPATH}:."

RUN python test/git_test.py

CMD ["python", "main.py"]