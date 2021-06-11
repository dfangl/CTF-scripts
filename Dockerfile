from nikolaik/python-nodejs:python3.9-nodejs16

RUN mkdir /home/root

WORKDIR /home/root

COPY . .

WORKDIR /home/root/flags

RUN pip3 install requests

WORKDIR /home/root

CMD node exploit-runner/exploit-runner.js | python3 flags/flag_parser.py | python3 flags/flag_submission.py