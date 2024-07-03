#!/bin/bash

echo "Configuring the dev environment..."

# git credentials and keys
git config --global user.name "$DEV_NAME"
git config --global user.email "$DEV_EMAIL"

# Ensure the SSH_AUTH_SOCK environment variable is set
if [ -z "$SSH_AUTH_SOCK" ]; then
    echo "SSH_AUTH_SOCK is not set. Exiting..."
    exit 1
fi

# testpypi
poetry config pypi-token.testpypi "$TEST_PYPI_TOKEN"
poetry config repositories.testpypi https://test.pypi.org/legacy/

# pypi
poetry config pypi-token.pypi "$PYPI_TOKEN"

echo "Done."