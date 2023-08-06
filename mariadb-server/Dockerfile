FROM alpine:latest

RUN mkdir setup_scripts
COPY secure_installation.sh setup_scripts
COPY add_user.sh setup_scripts

RUN apk update && apk add mariadb mariadb-client

RUN mysql_install_db --user=mysql --datadir=/var/lib/mysql
RUN ["sh", "setup_scripts/secure_installation.sh"]
RUN ["sh", "setup_scripts/add_user.sh"]

EXPOSE 3306
 
COPY conf.txt /etc/my.cnf.d/mariadb-server.cnf
CMD ["sh", "/usr/bin/mysqld_safe", "--datadir=/var/lib/mysql"]
