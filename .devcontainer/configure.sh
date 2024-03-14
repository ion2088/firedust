#!/bin/bash

echo "Configuring the dev environment..."

# git credentials and keys
git config --global user.name "$DEV_NAME"
git config --global user.email "$DEV_EMAIL"
chmod 600 /root/.ssh/id_rsa

# testpypi
poetry config pypi-token.testpypi "$TEST_PYPI_TOKEN"

echo "Done."