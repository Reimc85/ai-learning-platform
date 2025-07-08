# Stage 1: Build the React frontend
FROM node:18-alpine as frontend-builder
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm install
COPY frontend/. .
RUN npm run build

# Stage 2: Build the Python backend and serve the frontend
FROM python:3.9-slim-buster
WORKDIR /app

# Copy backend requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the built frontend from the previous stage
# This copies the 'build' output from the frontend-builder stage
# into '/app/frontend/dist' in the final image, as expected by app.py
COPY --from=frontend-builder /app/frontend/build /app/frontend/dist

# Copy the rest of your backend code (app.py, Procfile, src/ etc.)
COPY . .

# Set environment variables for Flask
ENV FLASK_APP=app.py
ENV FLASK_ENV=production # Or development, based on your needs

# Expose the port Gunicorn will listen on
EXPOSE 5000 # Your app.py defaults to 5000, so let's use that internally

# Command to run the application
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:5000"]
v
