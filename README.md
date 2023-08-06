# Database and queries of SEC Form 13f data

Form 13f is a disclosure of investment holdings that all institutional investors
larger than 100 million dollars must release quarterly.

More information can be found here:
https://www.investor.gov/introduction-investing/investing-basics/glossary/form-13f-reports-filed-institutional-investment

The complete dataset is too large to be effectively accessed in memory, therefore
the approach here is to load all the data into a SQL dataset (MariaDB).

## MariaDB server

This is a docker image, defined by a Dockerfile, that installs the mariadb server 
on Alpine linux and configures it with a local root user and a remote user. 

Start the server like this:
```
cd mariadb-server
docker build -t mariadb .
docker run --rm mariadb
```

## Data extraction from SEC website

The script **datadownload.py** does the following things:
1. Creates the sec13f database
2. Downloads and parses the website https://www.sec.gov/dera/data/form-13f
3. Downloads the quarterly datasets that has this [schema](https://www.investor.gov/introduction-investing/investing-basics/glossary/form-13f-reports-filed-institutional-investment)
4. Write the data into the database
5. Create indexes of some columns to actually allow interesting queries

At this point, the database can be tested with **gettopholdings.py**. It's usage:
```
gettopholdings.py Microsoft

              FILINGMANAGER_NAME         VALUE  YEAR QUARTAL
0             VANGUARD GROUP INC  178160347092  2023       2
1             VANGUARD GROUP INC  146672566610  2023       1
2              STATE STREET CORP   84214184961  2023       2
3              STATE STREET CORP   70644900477  2023       2
4              STATE STREET CORP   70644900477  2023       2
5              STATE STREET CORP   70644900477  2023       1
6                        FMR LLC   44569458965  2023       2
7  GEODE CAPITAL MANAGEMENT, LLC   41532557019  2023       2
8                        FMR LLC   36955783546  2023       1
9        Capital World Investors   25257061423  2023       2
```