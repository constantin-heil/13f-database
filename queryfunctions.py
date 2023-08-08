### This module contains functions that return text strings that represent
### complete SQL queries

def top_holdings(issuer: str, n_results: int = 10) -> str:
    """SQL query of top 10 holdings for a given issuer

    Args:
        issuer (str): Pattern to match INFOTABLE.NAMEOFISSUER
        n_results (int): Number of top results to return

    Returns:
        str: String that can be passed to SQL engine as query
    """
    sql_query = (
        f'SELECT c.FILINGMANAGER_NAME, q.VALUE, t.YEAR, t.QUARTAL FROM COVERPAGE c '
        f'INNER JOIN '
        f'(SELECT * FROM sec13f.INFOTABLE i WHERE MATCH(NAMEOFISSUER) AGAINST("{issuer}")) AS q '
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
