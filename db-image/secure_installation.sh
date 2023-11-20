/usr/bin/mysqld_safe --datadir='/var/lib/mysql' &
sleep 5

# change root password
mysql -u root -e "ALTER USER 'root'@'localhost' IDENTIFIED BY 'password';"

# delete anonymous users
mysql -u root -ppassword -e "DELETE FROM mysql.user WHERE User='';"

# block root login for root
mysql -u root -ppassword -e "DELETE FROM mysql.user WHERE User='root' AND Host NOT IN ('localhost', '127.0.0.1', '::1');"

# remove test database
mysql -u root -ppassword -e "DROP DATABASE test;"
mysql -u root -ppassword -e "DELETE FROM mysql.db WHERE Db='test' OR Db='test\\_%';"

# rest priviledges
mysql -u root -ppassword -e "FLUSH PRIVILEGES;"
