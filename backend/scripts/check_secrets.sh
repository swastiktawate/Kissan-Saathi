#!/usr/bin/env bash
# check_secrets.sh — scan for committed secrets
set -euo pipefail

ERRORS=0

# Check for .env files tracked by git
if git ls-files --cached | grep -qE '^\\.env$|^\\.env\\.'; then
    echo "FAIL: .env file is tracked by git!"
    ERRORS=$((ERRORS + 1))
fi

# Check for literal API key patterns in tracked files
PATTERNS="AIza|sk-|AKIA|ghp_|gho_|glpat-|xoxb-|xoxp-"
if git grep -lEI "$PATTERNS" -- ':(exclude)*.sh' ':(exclude)check_secrets*' ':(exclude)*.svg' 2>/dev/null; then
    echo "FAIL: Possible API key pattern found in tracked files!"
    ERRORS=$((ERRORS + 1))
fi

# Check for VITE_ secrets leaked in build output
if [ -d "frontend/dist" ]; then
    if grep -rlE "VITE_.*KEY|VITE_.*SECRET" frontend/dist/ 2>/dev/null; then
        echo "FAIL: VITE_ secret found in frontend build output!"
        ERRORS=$((ERRORS + 1))
    fi
fi

if [ "$ERRORS" -gt 0 ]; then
    echo "Security scan FAILED with $ERRORS issue(s)."
    exit 1
fi

echo "Security scan passed. No secrets detected."
exit 0
