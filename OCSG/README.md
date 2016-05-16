
## Mysql db

```sh
docker run --rm --name ocsg6-mysql -e MYSQL_ROOT_PASSWORD=welcome1 -e MYSQL_DATABASE=ocsg -e MYSQL_USER=ocsg -e MYSQL_PASSWORD=ocsg -d mysql:5.6
```

## OCSG

```sh
docker build -t netapps/ocsg:6.0 .
docker run --rm --name ocsg6 -p 7001:7001 --link ocsg6-mysql:mysqldb -t -i netapps/ocsg:6.0 
```

For debugging:

```sh
docker run --rm --name ocsg6 -p 7001:7001 --link ocsg6-mysql:mysqldb -t -i netapps/ocsg:6.0 /bin/bash
```

## TODO:

1. Delete used files
2. Change admin password asn ENV variable
3. PTE?
4. Allow nodes instead of only admin?
