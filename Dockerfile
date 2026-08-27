# --------------------------------------------------
# 1. A small base image
# --------------------------------------------------
FROM python:3.12-slim

# --------------------------------------------------
# 2. Add image metadata
# This can be inspected docker image inspect image-name
# --------------------------------------------------
LABEL maintainer="Hosea Mutwiri"
LABEL version="1.0.0"
LABEL description="Dockerized Binance Crypto Price ETL"

# --------------------------------------------------
# 3. Set environment variables
# --------------------------------------------------
# Prevent Python from creating .pyc files
ENV PYTHONDONTWRITEBYTECODE=1

# Make Python output appear immediately in Docker logs
ENV PYTHONUNBUFFERED=1

# --------------------------------------------------
# 4. Create a non-root user
# create a home dir for appuser and when the user use
# shell to use bash useful when you enter the container 
#interactively docker exec -it <container> /bin/bash
# --------------------------------------------------
RUN useradd --create-home --shell /bin/bash appuser

# --------------------------------------------------
# 5. Set working directory
# --------------------------------------------------
WORKDIR /app

# --------------------------------------------------
# 6. Copy requirements first
#    This improves Docker build caching
# --------------------------------------------------
COPY requirements.txt .

# --------------------------------------------------
# 7. Install Python dependencies
#    --no-cache-dir prevents pip cache from
#    increasing image size
# --------------------------------------------------
RUN pip install --no-cache-dir -r requirements.txt

# --------------------------------------------------
# 8. Copy application files
# --------------------------------------------------
COPY app/ ./app/
COPY config/ ./config/
COPY main.py .


# --------------------------------------------------
# Create directories required at runtime
RUN mkdir -p /app/logs /app/data
# --------------------------------------------------
# 9. Give the application user ownership
# including all subdir and files
# --------------------------------------------------
RUN chown -R appuser:appuser /app

# --------------------------------------------------
# 10. Switch from root to non-root user
# from this point run commands a appuser and not root
# --------------------------------------------------
USER appuser

# --------------------------------------------------
# 11. Start the ETL application
# 
# --------------------------------------------------
ENTRYPOINT ["python", "main.py"]