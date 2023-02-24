server {
    listen 80;
    server_name yggdrasil.beelzeware.dev;

    location /.well-known/acme-challenge/ {
        root /vol/www/;
    }

    location / {
        return 301 https://$host$request_uri;
    }
}

server {
    listen      443 ssl;
    server_name yggdrasil.beelzeware.dev;

    ssl_certificate     /etc/letsencrypt/live/yggdrasil.beelzeware.dev/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yggdrasil.beelzeware.dev/privkey.pem;

    include     /etc/nginx/options-ssl-nginx.conf;

    ssl_dhparam /vol/proxy/ssl-dhparams.pem;

    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;

    location /static {
        alias /vol/static;
    }

    location / {
        proxy_pass        http://ggj23_server:11000;
    }
}