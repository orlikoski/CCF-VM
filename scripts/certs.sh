#!/bin/bash

sudo docker run -it --rm --name certbot \
  -v /etc/nginx/certs/letsencrypt:/etc/letsencrypt \
  -v /var/log/letsencrypt:/var/log/letsencrypt \
  -v /usr/share/nginx/html/letsencrypt:/var/www/.well-known \
  quay.io/letsencrypt/letsencrypt -t certonly \
  --agree-tos --renew-by-default \
  --webroot -w /var/www \
  -d skadi.theknightlyserver.com
