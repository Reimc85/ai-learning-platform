# Stage 1: Build the React application
FROM node:18-alpine as builder

WORKDIR /app/frontend

# Copy package.json and package-lock.json (if you have one)
# to leverage Docker cache
COPY frontend/package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the frontend source code
COPY frontend/ .

# Build the React app for production
RUN npm run build

# Stage 2: Serve the application with a lightweight Node.js server
FROM node:18-alpine

WORKDIR /app/frontend

# Copy the built React app from the builder stage
COPY --from=builder /app/frontend/build ./build

# Copy your server.js and package.json for the runtime
COPY frontend/server.js .
COPY frontend/package.json .

# Install only production dependencies for the server (e.g., express)
RUN npm install --production

# Expose the port your server listens on
EXPOSE 8080

# Command to run the server
CMD ["node", "server.js"]
