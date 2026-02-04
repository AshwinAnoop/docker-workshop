# Use Python 3.13 image as base
FROM python:3.13.10-slim

# Install Uv from Astral's GitHub Container Registry
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/

# Set up a virtual environment for the application
# Python from the base image will be used to create the venv
ENV PATH="/app/.venv/bin:$PATH"

# Set working directory
WORKDIR /app

# Copy dependency files
COPY "pyproject.toml" ".python-version" "uv.lock" ./

# Install dependencies using Uv
RUN uv sync --locked

#Copy pipeline code to container from local machine
COPY pipeline.py ./pipeline.py

# Set the entrypoint to run the pipeline using Uv
ENTRYPOINT ["python","pipeline.py"]