FROM python:3 AS stage

WORKDIR /firedust

# Env variables and dep versions
ENV POETRY_VERSION=1.6
ENV APP="firedust"
ENV PYTHONPATH="${PYTHONPATH}:/firedust"

# Install poetry and copy pyproject
RUN pip install poetry=="$POETRY_VERSION"
COPY pyproject.toml poetry.lock ./

# --------------------------------------------------
# Dev image
# --------------------------------------------------
FROM stage as firedust-dev

ENV PATH="{/home/vscode/local/bin:$PATH}"
ENV ENV="local"

RUN apt-get update && apt-get install -y git
RUN git config --global --add safe.directory /workspaces/firedust
RUN git config --global user.email "$DEV_EMAIL"
RUN git config --global user.name "$DEV_NAME"

RUN poetry install
CMD ["/bin/bash" "ln" "-s" "$(poetry env info --path)" "~/.venv"]

COPY . .

# --------------------------------------------------
# Prod image
# --------------------------------------------------
FROM stage as firedust-prod

ENV ENV="prod"
RUN poetry install --no-dev

COPY . .

# What are we trying to achieve here?