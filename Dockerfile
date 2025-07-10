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
COPY --from=frontend-builder /app/frontend/build /app/frontend/dist

# Copy the rest of your backend code
COPY . .

# Set environment variables for Flask
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# Expose the port the app will listen on
EXPOSE 5000

# --- DIAGNOSTIC CHANGE: RUN FLASK DIRECTLY ---
# Command to run the application using Flask's built-in server
# This is for debugging the 405 error.
CMD ["python", "app.py"]
