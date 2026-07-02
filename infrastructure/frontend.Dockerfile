FROM node:20-alpine

WORKDIR /app

COPY apps/web/package.json ./
COPY apps/web/package-lock.json ./
COPY apps/web/tsconfig.json ./
COPY apps/web/next-env.d.ts ./
COPY apps/web/next.config.ts ./
COPY apps/web/jest.config.js ./
COPY apps/web/jest.setup.ts ./
COPY apps/web/app ./app
COPY apps/web/lib ./lib
COPY apps/web/public ./public

RUN npm install

ENV NEXT_PUBLIC_APP_VERSION=0.1.0a0 \
    NEXT_PUBLIC_ENVIRONMENT=development \
    NEXT_PUBLIC_ARCHITECTURE_VERSION=GAR-0001 \
    NEXT_PUBLIC_SPRINT_VERSION=GAR-SPRINT-0001 \
    NEXT_PUBLIC_BACKEND_URL=http://localhost:8000

EXPOSE 3000

CMD ["npm", "run", "dev", "--", "--hostname", "0.0.0.0"]
