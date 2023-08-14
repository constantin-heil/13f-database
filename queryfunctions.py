### This module contains functions that return text strings that represent
### complete SQL queries

def top_holders(issuer: str, n_results: int = None) -> str:
    """SQL query of top 10 holders for a given issuer

    Args:
        issuer (str): Pattern to match INFOTABLE.NAMEOFISSUER
        n_results (int): Number of top results to return

    Returns:
        str: String that can be passed to SQL engine as query
    """
    sql_query = (
        f'SELECT c.FILINGMANAGER_NAME, q.NAMEOFISSUER, q.VALUE, t.YEAR, t.QUARTAL FROM COVERPAGE c '
        f'INNER JOIN '
        f'(SELECT * FROM sec13f.INFOTABLE i WHERE MATCH(NAMEOFISSUER) AGAINST("{issuer}" IN BOOLEAN MODE)) AS q '
        f'ON c.ACCESSION_NUMBER = q.ACCESSION_NUMBER '
        f'INNER JOIN '
        f'TIMEMAP t '
        f'ON c.ACCESSION_NUMBER = t.ACCESSION_NUMBER '
        f'ORDER BY q.VALUE DESC '
        )

    if n_results:
        limit_str = f'LIMIT {n_results};'
    else:
        limit_str = f';'
    
    return sql_query + limit_str

def top_holdings(manager_name: str, n_results: int = None) -> str:
    """Return the holdings for a given manager

    Args:
        manager_name (str): Name of institutional investor
        n_results (int, optional): Number of top results to return. Defaults to None.

    Returns:
        str: String that can be passed to SQL engine as query
    """
    sql_query = (
        f'SELECT q.FILINGMANAGER_NAME, i.NAMEOFISSUER , i.VALUE, t.`YEAR`, t.QUARTAL  FROM '
	    f'(SELECT * FROM COVERPAGE c WHERE MATCH(FILINGMANAGER_NAME) AGAINST("{manager_name}" IN BOOLEAN MODE)) AS q'
        f'INNER JOIN INFOTABLE i ON q.ACCESSION_NUMBER = i.ACCESSION_NUMBER '
        f'LEFT JOIN TIMEMAP t ON i.ACCESSION_NUMBER = t.ACCESSION_NUMBER '
    )
    
    if n_results:
        limit_str = f'LIMIT {n_results};'
    else:
        limit_str = f';'
        
    return sql_query + limit_str