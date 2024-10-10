FROM phidata/python:3.12

ARG USER=app
ARG APP_DIR=${USER_LOCAL_DIR}/${USER}
ENV APP_DIR=${APP_DIR}
# Add APP_DIR to PYTHONPATH
ENV PYTHONPATH="${APP_DIR}:${PYTHONPATH}"

# Create user and home directory
RUN groupadd -g 61000 ${USER} \
  && useradd -g 61000 -u 61000 -ms /bin/bash -d ${APP_DIR} ${USER}

WORKDIR ${APP_DIR}

# Copy requirements and install
COPY requirements.txt pyproject.toml ./
RUN --mount=type=cache,target=/root/.cache/uv \
    uv pip sync requirements.txt --system

# Copy project files
COPY . .

COPY scripts /scripts
USER ${USER}
ENTRYPOINT ["/scripts/entrypoint.sh"]
CMD ["chill"]
