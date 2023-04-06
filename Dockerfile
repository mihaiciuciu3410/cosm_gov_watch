FROM python:3.8.16-alpine3.17

RUN mkdir /proposal_bot

COPY . /proposal_bot
WORKDIR /proposal_bot

ENV VIRTUAL_ENV=/proposal_bot/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN pip install -r requirements.txt
RUN pip install -e .

CMD ["cosm_gov_watch"]