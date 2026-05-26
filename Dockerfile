FROM nginx:alpine

# Copy docs (index.html, styles.css, script.js) to /app/docs/
# Copy assets (SVGs) to /app/assets/
# nginx root is /app/docs/ so ../assets/ in index.html resolves to /app/assets/
COPY docs/   /app/docs/
COPY assets/ /app/assets/

COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 8080

CMD ["nginx", "-g", "daemon off;"]
