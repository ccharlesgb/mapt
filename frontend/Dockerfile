FROM node:14
WORKDIR /usr/app
COPY package.json yarn.lock ./
RUN yarn install --ignore-optional && yarn cache clean
COPY public ./public
COPY src ./src
EXPOSE 8000
CMD ["yarn", "start"]
