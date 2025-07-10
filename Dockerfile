# Stage 1: Build the React frontend
FROM node:18-alpine as frontend-builder
WORKDIR /app/frontend

# Copy package.json and lock file
COPY frontend/package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the frontend code and build the app
COPY frontend/. .
RUN npm run build

# Stage 2: Build the Python backend and serve the frontend
FROM python:3.9-slim-buster
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install backend dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the built frontend from the previous stage
COPY --from=frontend-builder /app/frontend/dist /app/frontend/dist

# Copy the rest of your backend application code
COPY . .

# Expose the port the app will listen on
EXPOSE 5000

# Command to run the application using Gunicorn (the single source of truth)
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
