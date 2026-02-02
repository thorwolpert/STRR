FROM mcr.microsoft.com/devcontainers/python:3.11-bookworm

# 1. FIX: Remove the broken Yarn repository list so apt-get update doesn't fail
RUN rm -f /etc/apt/sources.list.d/yarn.list

# 2. SYSTEM DEPENDENCIES: Install Pango for WeasyPrint
# We run update and install in the same layer to keep the image clean.
# We include 'libpangoft2-1.0-0' which is almost always required alongside standard pango.
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install --no-install-recommends \
    libpango-1.0-0 \
    libpangoft2-1.0-0 \
    postgresql-client \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# 3. POETRY: Install via pip to avoid ARM64/SSL errors
RUN pip install --no-cache-dir poetry

# 4. CONFIG: Set Poetry defaults
RUN poetry config virtualenvs.in-project true
