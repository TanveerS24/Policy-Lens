FROM node:20-slim

WORKDIR /app

# Install expo CLI
RUN npm install -g expo-cli

COPY package.json package-lock.json* ./
RUN npm install

COPY . .

EXPOSE 19000 19001 19002

CMD ["expo", "start", "--host", "0.0.0.0"]
