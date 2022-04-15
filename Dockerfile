FROM python:latest
ENV VIRTUAL_ENV "/venv"
RUN python -m venv $VIRTUAL_ENV
ENV PATH "$VIRTUAL_ENV/bin:$PATH"

RUN apt-get update && apt-get upgrade -y
RUN python -m pip install --upgrade pip
RUN git clone https://github.com/Krakinz/ScarLord.git
RUN cd ScarLord

WORKDIR /ScarLord
RUN pip install -r SƈαɾLσɾԃ.txt
CMD python3 hypefile.py
