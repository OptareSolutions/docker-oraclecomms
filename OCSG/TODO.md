
- Avoid one Docker instance with everything, at least one for Admin, one for Portal and one for DB
- Same approach should be done with OCCAS


Mysql:

Run mysql:
docker run --name ocsg6-mysql -e MYSQL_ROOT_PASSWORD=welcome1 -d mysql:5.6

Run the machine connected to mysql:
docker run --name myocsg --link ocsg6-mysql:mysql -t -i ocsg:6.0 /bin/bash
