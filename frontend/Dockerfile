# Stage 1: Build the React application
FROM node:18-alpine as builder

# Set the working directory inside the builder image
WORKDIR /app

# Copy package.json and package-lock.json from the build context (frontend/)
COPY package*.json ./

# Copy the public directory (containing index.html)
COPY public ./public

# Copy the src directory (containing your React source code)
COPY src ./src

# Install dependencies
RUN npm install

# Copy the rest of the frontend source code from the build context (frontend/)
# This line might become redundant if all necessary files are copied above,
# but it's safer to keep it for now.
COPY . .

# Build the React app for production
RUN npm run build

# Stage 2: Serve the application with a lightweight Node.js server
FROM node:18-alpine

# Set the working directory inside the final image
WORKDIR /app

# Copy the built React app from the builder stage
COPY --from=builder /app/build ./build

# Copy your server.js and package.json for the runtime
COPY server.js .
COPY package.json .

# Install only production dependencies for the server (e.g., express)
RUN npm install --production

# Expose the port your server listens on
EXPOSE 8080

# Command to run the server
CMD ["node", "server.js"]
