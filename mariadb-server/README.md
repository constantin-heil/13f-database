# Most basic installation and configuration of a mariadb server

This contains a dockerfile that installs a basic db server in alpine linux docker container.

The dockerfile executes the following steps:

1. Start from the latest alpine linux image

```
FROM alpine
```

2. Update packages and install mariadb

```
apk update
apk add mariadb mariadb-client
```

3. Installation of the server

```
mysql_install_db --user mysql --datadir=/var/lib/mysql
```

4. Change the root password

This is run with a small bash script so that it can be run without opening a new terminal

```
sh change_root_password.sh
```

5. Secure the installation

These are the steps normally carried out by mysql_secure_installation, i.e.:
	- delete the default user
	- disallow remote login for root
	- delete the test database
	- reset the priviledge tables

We run these steps from a script because the original command is interactive.

```
sh secure_installation.sh
```

6. Database ready

Access database as root with:

```
mysql -u root -ppassword
```

