# Use the official Python base image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /app

# Copy the backend code to the container
COPY . /app/

# Install dependencies, including SQLAlchemy
RUN pip install --no-cache-dir fastapi selenium pytest chromedriver-autoinstaller uvicorn sqlalchemy


# Expose the port the app will run on
EXPOSE 8000

# Start the FastAPI application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
