from nikolaik/python-nodejs:python3.9-nodejs16

RUN mkdir /home/root

WORKDIR /home/root

COPY . .

WORKDIR /home/root/flag-submitter

RUN pip3 install requests

WORKDIR /home/root

CMD node exploit-runner/exploit-runner.js | python3 flag-parser/flag-parser.py | python3 flag-submitter/flag-submit.py