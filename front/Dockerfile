FROM node:18

RUN yarn global add @angular/cli@14.1.3

WORKDIR /app
COPY package.json /app
RUN npm install
COPY . /app

CMD ng serve --host 0.0.0.0 
EXPOSE 4200