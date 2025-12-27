FROM node:18-alpine as builder

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci

# Copy source code
COPY . .

# Build application
RUN npm run build

# Production stage
FROM node:18-alpine

WORKDIR /app

# Copy built files from builder
COPY --from=builder /app/build ./build

# Copy built files to backend static directory (will be mounted as volume)
# In production, you would copy these to the backend container
CMD ["sh", "-c", "cp -r build/* /shared/static/"]

