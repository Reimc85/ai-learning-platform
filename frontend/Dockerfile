# Stage 1: Build the React application
FROM node:18-alpine as builder

# Set the working directory inside the builder image
# This will be the root of your frontend application within the Docker image
WORKDIR /app/frontend

# Copy package.json and package-lock.json
# These are now relative to /app/frontend
COPY package*.json ./

# Install ALL dependencies (dev and prod) for building
RUN npm install

# Copy the rest of the frontend source code
# This copies everything from your frontend/ directory into /app/frontend
COPY . .

# Build the React app for production
# This will create the 'build' folder inside /app/frontend
RUN npm run build

# Stage 2: Serve the application with a lightweight Node.js server
FROM node:18-alpine

# Set the working directory inside the final image
WORKDIR /app/frontend

# Copy the built React app from the builder stage
# It's now at /app/frontend/build from the builder stage
COPY --from=builder /app/frontend/build ./build

# Copy your server.js and package.json for the runtime
COPY server.js ./
COPY package.json ./

# Install only production dependencies for the server (e.g., express)
RUN npm install --production

# Expose the port your server listens on
EXPOSE 8080

# Command to run the server
CMD ["node", "server.js"]
