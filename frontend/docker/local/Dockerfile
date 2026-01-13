FROM docker.io/node:20.11-alpine3.18 as base

# --- Build Stage ---
# This stage installs dependencies and is cached as long as package.json doesn't change.
FROM base as node-build-stage

WORKDIR /app

RUN apk add --no-cache libc6-compat

COPY package.json yarn.lock* package-lock.json* pnpm-lock.yaml* ./

RUN \
  if [ -f yarn.lock ]; then yarn --frozen-lockfile; \
  elif [ -f package-lock.json ]; then npm ci; \
  elif [ -f pnpm-lock.yaml ]; then corepack enable pnpm && pnpm i; \
  else echo "Lockfile not found." && exit 1; \
  fi


# --- Run Stage ---
# This is the final image for development.
FROM base as node-run-stage

ARG APP_HOME=/app
WORKDIR ${APP_HOME}

# 1. Create the user and group FIRST. This will always be cached.
RUN addgroup -g 1001 -S nodejs && \
  adduser -S nextjs -u 1001 -G nodejs

# 2. Copy dependencies from the build stage. This will be cached.
#    We also set ownership here, which is more efficient.
COPY --chown=nextjs:nodejs --from=node-build-stage /app/node_modules ./node_modules
# Also copy package.json for the 'npm run dev' command to work
COPY --chown=nextjs:nodejs --from=node-build-stage /app/package.json ./package.json

# 3. Change to the non-root user.
USER nextjs

# 4. Copy the rest of your application code LAST.
#    This is the only layer that will be rebuilt frequently.
COPY --chown=nextjs:nodejs . .

# 5. The command to run the application.
CMD [ "npm", "run", "dev" ]