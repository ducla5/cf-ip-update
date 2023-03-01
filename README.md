## Cloudflare DNS IP Update
Use to dynamic update your IP to DNS Record on Cloudflare

```shell
python update_dns_record.py
```

Can be built to a docker container and run on home lab.

```shell
version: "3.9"
services:
 cf-ip-update:
   image: ducla6/cf-ip-update:latest
   environment:
    - API_KEY
    - ZONE_ID
    - DOMAIN_NAMES
```