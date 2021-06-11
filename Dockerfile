FROM nikolaik/python-nodejs:python3.9-nodejs16

RUN pip3 install requests

WORKDIR /home/root

COPY . .

CMD node exploit-runner/exploit-runner.js | python3 flags/flag_parser.py | python3 flags/flag_submission.py