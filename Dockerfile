FROM nginx:alpine

COPY docs/   /app/docs/
COPY assets/ /app/docs/assets/

COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 8080

CMD ["nginx", "-g", "daemon off;"]
