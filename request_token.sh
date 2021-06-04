#!/bin/sh
# Usage: request_token.sh LAB0_USERNAME LAB0_PASSWORD

SERVER=10.10.40.200
PORT=8443

curl -X POST "https://$SERVER:$PORT/api/auth/login" -H "accept: */*" \
      -H "Content-Type: application/json" \
      -d "{ \"username\": \"$1\", \"password\": \"$2\"}" \
      -k