FROM python:3.12.7-bookworm

RUN mkdir -p /home/.teenylauncher

COPY . /home/.teenylauncher
WORKDIR /home/.teenylauncher

RUN python -m pip install -U pip
RUN python -m pip install -r requeriments.txt

EXPOSE 9892-9892

CMD ["python",  "main_web.py"]