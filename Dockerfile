# Dockerfile
# ---------- base image ----------
    FROM python:3.11-slim AS base

    # Avoids prompts & sets Python buffering
    ENV     PYTHONUNBUFFERED=1 \
            PIP_NO_CACHE_DIR=1 \
            PIP_DISABLE_PIP_VERSION_CHECK=1
    
    # Install system deps only once (cached layer)
    RUN apt-get update && apt-get install -y --no-install-recommends \
            build-essential curl && \
        rm -rf /var/lib/apt/lists/*
    
    # ---------- runtime layer ----------
    WORKDIR /app
    COPY requirements.txt .
    
    RUN pip install --upgrade pip && \
        pip install -r requirements.txt
    
    # Copy the source after deps (keeps cache)
    COPY src/ ./src/
    COPY data/ ./data/
    
    # Expose Streamlit default port
    EXPOSE 8501
    
    # Default command
    CMD ["streamlit", "run", "src/app/main.py", \
         "--server.port", "8501", "--server.address", "0.0.0.0"]
    