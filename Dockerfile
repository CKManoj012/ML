# Use Python 3.9 as the base image
FROM python:3.9-slim

# Set the working directory to /app
WORKDIR /app

# Copy all the app files
COPY ./app /app

# Upgrade pip
RUN pip install --upgrade pip

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the application port
EXPOSE 8000

# Run the FastAPI app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
