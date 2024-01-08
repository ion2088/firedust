FROM python:3 AS stage

WORKDIR /firedust

# Env variables and dep versions
ENV POETRY_VERSION=1.6
ENV APP="firedust"
ENV PYTHONPATH="${PYTHONPATH}:/firedust"

# Install aws and login to the app user
RUN apt-get update -y
RUN apt-get install -y curl
RUN apt-get install -y unzip
RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
RUN unzip awscliv2.zip
RUN ./aws/install

# Install postgresql dependencies
# RUN apt-get install -y libpq-dev python-dev

# Install poetry
RUN pip install poetry=="$POETRY_VERSION"

# Install uvicorn and dependencies
RUN apt-get install -y uvicorn
RUN pip install uvloop
# RUN pip install httptools==0.1.*

COPY pyproject.toml poetry.lock ./

# --------------------------------------------------
# Dev image
# --------------------------------------------------
FROM stage as firedust-dev

ARG AWS_ACCESS_KEY_ID
ARG AWS_SECRET_ACCESS_KEY

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

RUN poetry install
COPY firedust firedust/

EXPOSE 8080
ENV PORT 8080

CMD ["poetry", "run", "uvicorn", "firedust.api.main:firedust", "--host", "0.0.0.0", "--port", "8080"]