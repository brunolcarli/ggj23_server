server {
    listen 80 default_server;
    server_name  yggdrasil.beelzeware.dev;

    location /.well-known/acme-challenge/ {
        root /vol/www/;
    }

    location / {
        return 301 https://$host$request_uri;
    }
}
