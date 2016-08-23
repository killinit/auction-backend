FROM nginx
COPY nginx.conf /etc/nginx/nginx.conf
ADD sites-enabled/ /etc/nginx/sites-enabled
RUN echo Y | apt-get update && echo Y | apt-get install ngrep
