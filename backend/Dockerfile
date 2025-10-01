# Multi-stage Dockerfile for Claudipedia Backend
FROM python:3.11-slim as builder

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Runtime stage
FROM python:3.11-slim

# Create non-root user for security
RUN groupadd -r claudipedia && useradd -r -g claudipedia claudipedia

# Set working directory
WORKDIR /app

# Install runtime system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy installed packages from builder stage
COPY --from=builder /root/.local /home/claudipedia/.local

# Create necessary directories
RUN mkdir -p /app/logs && chown -R claudipedia:claudipedia /app

# Copy application code
COPY . .

# Set ownership
RUN chown -R claudipedia:claudipedia /app

# Switch to non-root user
USER claudipedia

# Add local bin to PATH
ENV PATH=/home/claudipedia/.local/bin:$PATH

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Start the application
CMD ["python", "main.py"]

