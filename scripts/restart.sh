#!/bin/sh

# Restart the app via Heroku Scheduler  at a predictable time
curl -X DELETE "https://api.heroku.com/apps/texas-covid/dynos" \
  --user "${HEROKU_CLI_USER}:${HEROKU_CLI_TOKEN}" \
  -H "Content-Type: application/json" \
  -H "Accept: application/vnd.heroku+json; version=3"