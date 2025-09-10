# Use an official Python base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port (optional but harmless)
EXPOSE 8000

# Start the FastAPI app using Render's dynamic port
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "${PORT}"]


