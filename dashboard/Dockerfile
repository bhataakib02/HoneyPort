FROM node:20-alpine

# Set working directory
WORKDIR /app

# Install dependencies for building native modules
RUN apk add --no-cache python3 make g++

# Copy package files
COPY package.json package-lock.json* ./

# Install dependencies
RUN npm ci --only=production

# Copy source code
COPY . .

# Expose port
EXPOSE 5173

# Set environment variables
ENV NODE_ENV=development
ENV VITE_API_URL=http://localhost:8000
ENV VITE_HONEYPOT_URL=http://localhost:2222

# Start development server
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]



