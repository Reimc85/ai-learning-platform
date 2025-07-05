# Stage 1: Build the React application
FROM node:18-alpine as builder

# Set the working directory inside the builder image to the root of the app
WORKDIR /app

# Copy the frontend's package.json and package-lock.json
# from the build context (which is the repository root)
COPY frontend/package*.json ./frontend/

# Set the working directory to the frontend app within the builder image
WORKDIR /app/frontend

# Install dependencies
RUN npm install

# Copy the rest of the frontend source code
# from the build context (repository root) into the current WORKDIR (/app/frontend)
COPY frontend/. .

# Build the React app for production
RUN npm run build

# Stage 2: Serve the application with a lightweight Node.js server
FROM node:18-alpine

# Set the working directory inside the final image
WORKDIR /app/frontend

# Copy the built React app from the builder stage
COPY --from=builder /app/frontend/build ./build

# Copy your server.js and package.json for the runtime
# These paths are relative to the build context (repository root)
COPY frontend/server.js ./
COPY frontend/package.json ./

# Install only production dependencies for the server (e.g., express)
RUN npm install --production

# Expose the port your server listens on
EXPOSE 8080

# Command to run the server
CMD ["node", "server.js"]
