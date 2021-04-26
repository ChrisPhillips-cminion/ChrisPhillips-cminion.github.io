---
layout: post
categories: APIConnect
date: 2021-04-26 00:15:00
title: Reverse Proxy API Connect - Nginx

---

I got asked recently how to build a reverse proxy for API Conect. I had a few minutes free so I researched this and knocked it up.


<!--more-->

A reverse proxy allows you to put your target application (in this case API Management component) in separate network zones and provide a network route to it. It must handle hostname changes as well as rewriting the urls in the body. I chose to use NGINX instead of Apache, no real reason why.

This took me about 10 minutes to knock up so please be aware this is provided with no support and should be considered as a starter for ten. Your mileage may vary.

You will need to create a config file in `/etc/nginx/conf.d/` and restart nginx after you have updated the config.

For API Connect each endpoint has its own hostname and so the following should be repeated for the four management endpoints in the same config file. If you want to expose the GW and Portal application paths that would require an additional two. I would not expect there to be a need for the portal or  gateway management endpoints to be exposed, or either of the analytic endpoints.

*note: the reverse proxy must be exposed via SSL*



```

server {
    server_name platform-api.apps.hostname.cf;
    location / {
       proxy_pass https://minimum-mgmt-platform-api-cp4i.mycluster-lon04-c3c-16x32-uuid-0000.eu-gb.containers.appdomain.cloud;
       proxy_redirect https://minimum-mgmt-platform-api-cp4i.mycluster-lon04-c3c-16x32-uuid-0000.eu-gb.containers.appdomain.cloud https://$host;
       proxy_cache off;
       proxy_store off;
       proxy_buffering off;
       proxy_http_version 1.1;
       proxy_read_timeout 36000s;
       proxy_set_header Host minimum-mgmt-platform-api-cp4i.mycluster-lon04-c3c-16x32-uuid-0000.eu-gb.containers.appdomain.cloud;
       proxy_set_header Origin https://minimum-mgmt-platform-api-cp4i.mycluster-lon04-c3c-16x32-uuid-0000.eu-gb.containers.appdomain.cloud;
       proxy_set_header Upgrade $http_upgrade;
       proxy_set_header Connection $connection_upgrade;
       proxy_set_header X-Real-IP $remote_addr;
       proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
       proxy_set_header X-Forwarded-Proto $scheme;
       proxy_set_header Referer "";
       client_max_body_size 0;
  }

    listen 443 ssl; # managed by Certbot
    ssl_certificate /etc/letsencrypt/live/platform-api.apps.hostname.cf/fullchain.pem; # managed by Certbot
    ssl_certificate_key /etc/letsencrypt/live/platform-api.apps.hostname.cf/privkey.pem; # managed by Certbot
    include /etc/letsencrypt/options-ssl-nginx.conf; # managed by Certbot
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem; # managed by Certbot

}

```


**Key lines**

`server_name platform-api.apps.hostname.cf;` The host name exposed by the reverse proxy

`location / {` the context route exposed by the proxy

```
proxy_pass https://minimum-mgmt-platform-api-cp4i.mycluster-lon04-c3c-16x32-uuid-0000.eu-gb.containers.appdomain.cloud
proxy_redirect https://minimum-mgmt-platform-api-cp4i.mycluster-lon04-c3c-16x32-uuid-0000.eu-gb.containers.appdomain.cloud https://$host;
```
Where the reverse proxy is forwarding on requests to.


```
proxy_set_header Host minimum-mgmt-platform-api-cp4i.mycluster-lon04-c3c-16x32-uuid-0000.eu-gb.containers.appdomain.cloud;
proxy_set_header Origin https://minimum-mgmt-platform-api-cp4i.mycluster-lon04-c3c-16x32-uuid-0000.eu-gb.containers.appdomain.cloud;
```
Setting the host and origin headers

The other lines can be kept the same .



**Full Sample**
```

server {
    error_log /var/log/nginx-debug debug;
    server_name platform-api.apps.hostname.cf;
    location / {
       proxy_pass https://minimum-mgmt-platform-api-cp4i.mycluster-lon04-c3c-16x32-uuid-0000.eu-gb.containers.appdomain.cloud;
       proxy_redirect https://minimum-mgmt-platform-api-cp4i.mycluster-lon04-c3c-16x32-uuid-0000.eu-gb.containers.appdomain.cloud https://$host;
       proxy_cache off;
       proxy_store off;
       proxy_buffering off;
       proxy_http_version 1.1;
       proxy_read_timeout 36000s;
       proxy_set_header Host minimum-mgmt-platform-api-cp4i.mycluster-lon04-c3c-16x32-uuid-0000.eu-gb.containers.appdomain.cloud;
       proxy_set_header Origin https://minimum-mgmt-platform-api-cp4i.mycluster-lon04-c3c-16x32-uuid-0000.eu-gb.containers.appdomain.cloud;
       proxy_set_header Upgrade $http_upgrade;
       proxy_set_header Connection $connection_upgrade;
       proxy_set_header X-Real-IP $remote_addr;
       proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
       proxy_set_header X-Forwarded-Proto $scheme;
       proxy_set_header Referer "";
       client_max_body_size 0;
  }

    listen 443 ssl; # managed by Certbot
    ssl_certificate /etc/letsencrypt/live/platform-api.apps.hostname.cf/fullchain.pem; # managed by Certbot
    ssl_certificate_key /etc/letsencrypt/live/platform-api.apps.hostname.cf/privkey.pem; # managed by Certbot
    include /etc/letsencrypt/options-ssl-nginx.conf; # managed by Certbot
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem; # managed by Certbot

}

server {
    error_log /var/log/nginx-debug debug;
    server_name consumer-api.apps.hostname.cf;
    location / {
       proxy_pass https://minimum-mgmt-consumer-api-cp4i.mycluster-lon04-c3c-16x32-uuid-0000.eu-gb.containers.appdomain.cloud;
       proxy_redirect https://minimum-mgmt-consumer-api-cp4i.mycluster-lon04-c3c-16x32-uuid-0000.eu-gb.containers.appdomain.cloud https://$host;

       proxy_cache off;
       proxy_store off;
       proxy_buffering off;
       proxy_http_version 1.1;
       proxy_read_timeout 36000s;
       proxy_set_header Host minimum-mgmt-consumer-api-cp4i.mycluster-lon04-c3c-16x32-uuid-0000.eu-gb.containers.appdomain.cloud;
       proxy_set_header Origin https://minimum-mgmt-consumer-api-cp4i.mycluster-lon04-c3c-16x32-uuid-0000.eu-gb.containers.appdomain.cloud;
       proxy_set_header Upgrade $http_upgrade;
       proxy_set_header Connection $connection_upgrade;
       proxy_set_header X-Real-IP $remote_addr;
       proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
       proxy_set_header X-Forwarded-Proto $scheme;
       proxy_set_header Referer "";
       client_max_body_size 0;
  }

    listen 443 ssl; # managed by Certbot
    ssl_certificate /etc/letsencrypt/live/consumer-api.apps.hostname.cf/fullchain.pem; # managed by Certbot
    ssl_certificate_key /etc/letsencrypt/live/consumer-api.apps.hostname.cf/privkey.pem; # managed by Certbot
    include /etc/letsencrypt/options-ssl-nginx.conf; # managed by Certbot
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem; # managed by Certbot

}

server {
    error_log /var/log/nginx-debug debug;
    listen      80;
    server_name manager.apps.hostname.cf;
    location / {
       proxy_pass https://minimum-mgmt-api-manager-cp4i.mycluster-lon04-c3c-16x32-uuid-0000.eu-gb.containers.appdomain.cloud;
       proxy_redirect https://minimum-mgmt-api-manager-cp4i.mycluster-lon04-c3c-16x32-uuid-0000.eu-gb.containers.appdomain.cloud https://$host;

       proxy_cache off;
       proxy_store off;
       proxy_buffering off;
       proxy_http_version 1.1;
       proxy_read_timeout 36000s;
       proxy_set_header Host minimum-mgmt-api-manager-cp4i.mycluster-lon04-c3c-16x32-uuid-0000.eu-gb.containers.appdomain.cloud;
       proxy_set_header Origin https://minimum-mgmt-api-manager-cp4i.mycluster-lon04-c3c-16x32-uuid-0000.eu-gb.containers.appdomain.cloud;
       proxy_set_header Upgrade $http_upgrade;
       proxy_set_header Connection $connection_upgrade;
       proxy_set_header X-Real-IP $remote_addr;
       proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
       proxy_set_header X-Forwarded-Proto $scheme;
       proxy_set_header Referer "";
       client_max_body_size 0;
  }
  listen 443 ssl; # managed by Certbot
  ssl_certificate /etc/letsencrypt/live/manager-api.apps.hostname.cf/fullchain.pem; # managed by Certbot
  ssl_certificate_key /etc/letsencrypt/live/manager-api.apps.hostname.cf/privkey.pem; # managed by Certbot
  include /etc/letsencrypt/options-ssl-nginx.conf; # managed by Certbot
  ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem; # managed by Certbot
}

server {
    error_log /var/log/nginx-debug debug;
    server_name admin.apps.hostname.cf;
    location / {
       proxy_pass https://minimum-mgmt-admin-cp4i.mycluster-lon04-c3c-16x32-uuid-0000.eu-gb.containers.appdomain.cloud;
       proxy_redirect https://minimum-mgmt-admin-cp4i.mycluster-lon04-c3c-16x32-uuid-0000.eu-gb.containers.appdomain.cloud https://$host;

       proxy_cache off;
       proxy_store off;
       proxy_buffering off;
       proxy_http_version 1.1;
       proxy_read_timeout 36000s;
       proxy_set_header Host minimum-mgmt-admin-cp4i.mycluster-lon04-c3c-16x32-uuid-0000.eu-gb.containers.appdomain.cloud;
       proxy_set_header Origin https://minimum-mgmt-admin-cp4i.mycluster-lon04-c3c-16x32-uuid-0000.eu-gb.containers.appdomain.cloud;
       proxy_set_header Upgrade $http_upgrade;
       proxy_set_header Connection $connection_upgrade;
       proxy_set_header X-Real-IP $remote_addr;
       proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
       proxy_set_header X-Forwarded-Proto $scheme;
       proxy_set_header Referer "";
       client_max_body_size 0;
  }

    listen 443 ssl; # managed by Certbot
    ssl_certificate /etc/letsencrypt/live/admin.apps.hostname.cf/fullchain.pem; # managed by Certbot
    ssl_certificate_key /etc/letsencrypt/live/admin.apps.hostname.cf/privkey.pem; # managed by Certbot
    include /etc/letsencrypt/options-ssl-nginx.conf; # managed by Certbot
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem; # managed by Certbot

}


map $http_upgrade $connection_upgrade {
  default upgrade;
  ''      close;
}

server {
    if ($host = manager.apps.hostname.cf) {
        return 301 https://$host$request_uri;
    } # managed by Certbot
    listen      80;
    server_name manager.apps.hostname.cf;
    return 404; # managed by Certbot
}

server {
    if ($host = admin.apps.hostname.cf) {
        return 301 https://$host$request_uri;
    } # managed by Certbot
    listen      80;
    server_name admin.apps.hostname.cf;
    return 404; # managed by Certbot
}

server {
    if ($host = platform-api.apps.hostname.cf) {
        return 301 https://$host$request_uri;
    } # managed by Certbot


    listen      80;
    server_name platform-api.apps.hostname.cf;
    return 404; # managed by Certbot


}

server {
    if ($host = consumer-api.apps.hostname.cf) {
        return 301 https://$host$request_uri;
    } # managed by Certbot


    listen      80;
    server_name consumer-api.apps.hostname.cf;
    return 404; # managed by Certbot
}

```
