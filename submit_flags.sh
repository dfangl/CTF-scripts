#!/bin/sh
# Usage: request_token.sh TOKEN PAYLOAD
# Payload must have following format:
# { "data": ["flag1", "flag2", ...] }

SERVER=10.10.40.200
PORT=8443

curl -X POST "https://$SERVER:$PORT/api/flags" \
      -H "accept: */*" \
      -H "Authorization: Bearer $1" \
      -H "Content-Type: application/json" \
      -d $1 \
      -k