FROM python:3.7.0-alpine AS builder

# Set up working directory and files.
WORKDIR /app

# Install base dependencies.
RUN apk add -U \
        build-base \
        openssl-dev \
        libssl1.0 \
        libffi-dev \
        libxml2-dev \
        libxslt-dev

# Add app source.
COPY . /app


# Build application and its requirements.
RUN pip install -r requirements-build.txt \
    && pip wheel -r requirements.txt -r runtime/requirements-deploy.txt --wheel-dir=/wheels \
    && pip wheel . --wheel-dir=/wheels


FROM python:3.7.0-alpine

# Set up working directory and files.
WORKDIR /app
COPY --from=builder /wheels /wheels
COPY --from=builder /app/runtime/ /app/
COPY --from=builder /app/requirements.txt /app/

# Install app.
RUN apk add -U --no-cache \
        bash \
        libssl1.0 \
    && pip install --no-index --find-links=/wheels -r requirements.txt -r requirements-deploy.txt \
    && pip install --no-index --find-links=/wheels query_api \
    && rm -f requirements-deploy.txt \
    && rm -rf /wheels


ENTRYPOINT ["/bin/bash", "run.sh"]
