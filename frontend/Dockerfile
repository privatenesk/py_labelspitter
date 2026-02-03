FROM public.ecr.aws/docker/library/node:20-alpine

WORKDIR /app

COPY package.json ./
# Install dependencies
RUN npm install

COPY . .

# Build the application
RUN npm run build

EXPOSE 3000

ENV NUXT_HOST=0.0.0.0
ENV NUXT_PORT=3000

CMD ["node", ".output/server/index.mjs"]
