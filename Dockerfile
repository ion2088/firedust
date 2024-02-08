FROM python:3 AS stage

WORKDIR /workspaces/firedust

# Env variables and dep versions
ENV POETRY_VERSION=1.6 \
    APP="firedust" \
    PYTHONPATH="${PYTHONPATH}:/workspaces/firedust/src" \
    PATH="$PATH:/root/.poetry/bin"

# Install poetry and copy pyproject
RUN pip install poetry=="$POETRY_VERSION"
COPY pyproject.toml poetry.lock ./

# --------------------------------------------------
# Dev image
# --------------------------------------------------
FROM stage as firedust-dev

ENV PATH="/home/vscode/local/bin:$PATH" \
    ENV="local"

# Install development dependencies
RUN apt-get update && \
    apt-get install -y git && \
    rm -rf /var/lib/apt/lists/* && \
    poetry install

# Git configuration
RUN git config --global --add safe.directory /workspaces/firedust && \
    git config --global user.email "$DEV_EMAIL" && \
    git config --global user.name "$DEV_NAME"

COPY . .

# --------------------------------------------------
# Prod image
# --------------------------------------------------
FROM stage as firedust-prod

ENV ENV="prod"
RUN poetry install --no-dev

COPY . .

# What are we trying to achieve here?