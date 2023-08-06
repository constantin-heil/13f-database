/usr/bin/mysqld_safe --datadir='/var/lib/mysql' &
sleep 5

mysql -u root -ppassword -e "CREATE USER 'remoteuser'@'%' IDENTIFIED BY 'password';"
mysql -u root -ppassword -e "GRANT ALL PRIVILEGES ON *.* TO 'remoteuser'@'%';"
