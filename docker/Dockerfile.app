# docker/Dockerfile.app
FROM node:22

# Install pnpm globally
RUN npm install -g pnpm

WORKDIR /usr/src/app

# Copy package.json and pnpm-lock.yaml
# COPY package.json pnpm-lock.yaml ./

# RUN pnpm install
# RUN pnpm run dev

# COPY . .

CMD ["pnpm", "run", "dev"]
