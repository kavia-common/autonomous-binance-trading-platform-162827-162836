#!/bin/bash
cd /home/kavia/workspace/code-generation/autonomous-binance-trading-platform-162827-162836/trading_bot_backend
source venv/bin/activate
flake8 .
LINT_EXIT_CODE=$?
if [ $LINT_EXIT_CODE -ne 0 ]; then
  exit 1
fi

