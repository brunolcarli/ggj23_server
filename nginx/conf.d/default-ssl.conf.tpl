server {
    listen 80 default_server;
    server_name yggdrasil.beelzeware.dev;

    location /.well-known/acme-challenge/ {
        root /vol/www/;
    }

    location / {
        return 301 https://$host$request_uri;
    }

    location /subscriptions {
        return 301 https://$host$request_uri;
    }
}

server {
    listen      443 ssl default_server;
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
       proxy_pass  http://104.237.1.145:11000;
       proxy_http_version 1.0;
    }

    location /subscriptions {
        proxy_pass http://104.237.1.145:11000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade "WebSocket";
        proxy_set_header Connection "Upgrade";

        #proxy_redirect off;
        #proxy_set_header Host $host;
        #proxy_set_header X-Real-IP $remote_addr;
        #proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        #proxy_set_header X-Forwarded-Host $server_name;
    }
}

