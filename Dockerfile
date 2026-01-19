FROM python:latest

RUN mkdir -p /home/.teenylauncher

COPY . /home/.teenylauncher
WORKDIR /home/.teenylauncher

RUN python -m pip install -U pip
RUN python -m pip install -r requeriments.txt

EXPOSE 9892-9892

CMD ["flet", "run", "-w", "-p 9892",  "main.py"]