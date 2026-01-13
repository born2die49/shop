FROM docker.io/python:3.12.2-slim-bookworm as python

# Stage 1: Build dependency wheels
FROM python AS python-build-stage

ARG BUILD_ENVIRONMENT=local

RUN apt-get update && apt-get install --no-install-recommends -y \
  build-essential \
  libpq-dev

COPY ./requirements .

RUN pip wheel --wheel-dir /usr/src/app/wheels \
  -r ${BUILD_ENVIRONMENT}.txt


# Stage 2: Python run stage
FROM python as python-run-stage

ARG BUILD_ENVIRONMENT=local

ARG APP_HOME=/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV BUILD_ENV ${BUILD_ENVIRONMENT}

WORKDIR ${APP_HOME}

# --- Steps that rarely change are done first ---
# Install system packages
RUN apt-get update && apt-get install --no-install-recommends -y \
  sudo git bash-completion nano ssh libpq-dev gettext \
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*

# Create user and directories
RUN addgroup --system django && \
  adduser --system --ingroup django django && \
  mkdir -p ${APP_HOME}/staticfiles && \
  chown django:django ${APP_HOME}/staticfiles && \
  chmod 775 ${APP_HOME}/staticfiles

# --- Steps that change occasionally are next ---
# Install Python dependencies from the pre-built wheels
COPY --from=python-build-stage /usr/src/app/wheels /wheels/

RUN pip install --no-cache-dir --no-index --find-links=/wheels/ /wheels/* \
  && rm -rf /wheels/

# Copy all the entrypoint and start scripts
COPY --chown=django:django ./docker/local/django/entrypoint.sh /entrypoint
RUN sed -i 's/\r$//g' /entrypoint && chmod +x /entrypoint

COPY --chown=django:django ./docker/local/django/start.sh /start
RUN sed -i 's/\r$//g' /start && chmod +x /start

COPY --chown=django:django ./docker/local/django/celery/worker/start.sh /start-celeryworker
RUN sed -i 's/\r$//g' /start-celeryworker && chmod +x /start-celeryworker

COPY --chown=django:django ./docker/local/django/celery/beat/start.sh /start-celerybeat
RUN sed -i 's/\r$//g' /start-celerybeat && chmod +x /start-celerybeat

COPY --chown=django:django ./docker/local/django/celery/flower/start.sh /start-flower
RUN sed -i 's/\r$//g' /start-flower && chmod +x /start-flower

# --- The step that changes most frequently is LAST ---
# Copy the application source code
COPY --chown=django:django . ${APP_HOME}

# --- Final setup ---
USER django
ENTRYPOINT [ "/entrypoint" ]