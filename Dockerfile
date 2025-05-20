FROM python:3.11-slim

# Set environment variables to avoid interactive prompts and Python cache
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libglib2.0-0 \
    libgl1-mesa-glx \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgoogle-perftools4 \
    wget \
    ffmpeg \
    chromium \
    chromium-driver \
      # Additional dependencies for OpenCV
      ffmpeg \
      libsm6 \
      libxext6 \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright and its browser binaries
RUN pip install --no-cache-dir playwright && \
    playwright install --with-deps chromium

# Copy project files
COPY . .

# Expose port
EXPOSE 8000

# Run the FastAPI app
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--no-reload"]

