FROM node:10.19.0

WORKDIR /app
COPY kin-frontend/package.json .
RUN npm install

COPY kin-frontend .

CMD npm start
