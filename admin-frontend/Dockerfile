FROM node:20-alpine

WORKDIR /app

# Copy package files for deterministic installs
COPY package.json package-lock.json* ./

# Install dependencies (use ci if lock file exists, else install)
RUN if [ -f package-lock.json ]; then npm ci; else npm install; fi

# Copy project files
COPY . .

# Expose port
EXPOSE 5173

# Start development server
CMD ["npm", "run", "dev", "--", "--host"]
