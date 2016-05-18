# OCSG PTE Docker image

The first thing you need to do is download the following files indicated by the .download extension in this repo.

After do that, build the image as usual:

```sh
docker build -t netapps/ocsgpte:6.0 .
```

## Run as docker instances

```sh
docker run --name ocsg6-mysql -e MYSQL_ROOT_PASSWORD=welcome1 -e MYSQL_DATABASE=ocsg -e MYSQL_USER=ocsg -e MYSQL_PASSWORD=ocsg -d mysql:5.6
docker run -d --name ocsg6 -p 7001:7001 --link ocsg6-mysql:mysqldb netapps/ocsg:6.0 
docker run -d --name ocsg6pte -p 5900:5900 --link ocsg6:ocsg6 netapps/ocsgpte:6.0 
```

## Run with docker compose

```sh
docker-compose up
```

For debugging:

```sh
docker run --rm --name ocsg6pte -p 5900:5900 --link ocsg6:ocsg6 -t -i netapps/ocsgpte:6.0 /bin/bash
```

## How to connect

Using a VNC client, open session against localhost. For instance, http://www.tightvnc.com/download.php


## TODO:

- [x] Delete used files
- [x] Docker compose
- [ ] Populate PTE fields with the right data (ocsg6, etc.)
