### Simple command line query to return top holders of a company

from sys import argv, exit
from sqlalchemy import create_engine
import pandas as pd
import queryfunctions


try:
    query_str, n_results = argv[1], argv[2]
    
except IndexError:
    exit("Please provide a search pattern and number of top results output")
    
    
username = 'remoteuser'
password = 'password'
host = 'localhost'
database = 'sec13f'

if __name__ == "__main__":
    engine = create_engine(f"mysql+pymysql://{username}:{password}@{host}/{database}")
    query_str = queryfunctions.top_holdings(query_str, n_results)
    
    print(pd.read_sql_query(query_str, con = engine))
