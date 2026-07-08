#!/bin/bash
set -uo pipefail

# pytest and pytest-json-ctrf are baked into the environment image (environment/Dockerfile).
mkdir -p /logs/verifier

pytest /tests/test_outputs.py -rA --ctrf /logs/verifier/ctrf.json
STATUS=$?

if [ "$STATUS" -eq 0 ]; then
  echo 1 > /logs/verifier/reward.txt
else
  echo 0 > /logs/verifier/reward.txt
fi

exit 0
