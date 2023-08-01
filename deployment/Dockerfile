# Nilmal Service.
# Copyright (C) 2022 Nilmal.
# This file is distributed under the same license as the nilmal package.
# Sajad Rezvani <majidstic@gmail.com>, 2022.


# Build stage
FROM python:3.10-slim AS builder

WORKDIR /

RUN apt-get update && apt-get install -y gcc git libpq-dev procps cron vim netcat-traditional gettext zlib1g-dev libjpeg-dev libpangocairo-1.0-0

# install production requirements
COPY requirements.txt .
RUN pip install --disable-pip-version-check --no-cache-dir -r requirements.txt

## Final image
#FROM python:3.10-slim

# set common work directory
WORKDIR /usr/app

# Install required dependencies
#RUN apt-get update
#RUN apt-get install -y --fix-missing --no-install-recommends libpq-dev procps cron vim netcat gettext

# Copy pip installed packages
#COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages

# Mount sourse code
COPY . .

# Configure Timezone
ENV TZ=Asia/Tehran

RUN echo 'Configuring timezone:' $TZ \
    && ln -snf /usr/share/zoneinfo/$TZ /etc/localtime \
    && echo $TZ > /etc/timezonero

# Set Environment configs
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# In production stage `DEBUG` is always False!
ARG DEBUG=True

# Make entrypoint executable and run the entrypoint to start jobs, gunicorns, liveness
RUN cp /usr/app/deployment/entrypoint.sh .
RUN chmod +x /usr/app/entrypoint.sh
CMD /usr/app/entrypoint.sh

# Expose the port that Django use it
EXPOSE 8000
