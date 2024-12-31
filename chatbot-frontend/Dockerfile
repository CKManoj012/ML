# Use the Node.js image to build the frontend
FROM node:16 AS build

# Set the working directory in the container
WORKDIR /app

# Copy package.json and install dependencies
COPY package*.json ./
RUN npm install

# Copy the rest of the app files and build
COPY . .
RUN npm run build

# Serve the app using an Nginx image
FROM nginx:alpine
COPY --from=build /app/build /usr/share/nginx/html

# Expose the default Nginx port
EXPOSE 80

# Start the Nginx server
CMD ["nginx", "-g", "daemon off;"]
