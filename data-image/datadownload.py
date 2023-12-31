import requests
from shutil import rmtree
import bs4
import re
from pathlib import Path
import pandas as pd
import zipfile
import pymysql
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
import sqlalchemy
import json
from functools import partial
from multiprocessing import Process
import logging
import sys

logging.basicConfig(
    filename = "/logging/log.txt",
    encoding = "utf-8",
    level = logging.DEBUG
)

def import_json(fn: str) -> dict:
    with open(fn, 'r') as fh:
        loadedjson = json.load(fh)

    return loadedjson

def download_write(datapath: str, 
                   tmppath: str, 
                   engine: sqlalchemy.engine,
                   datecols: dict,
                   coltypes: dict) -> None:
    filestem = Path(datapath).stem
    year, quartal = filestem.replace("_form13f", "").split("q")
    logging.info(f"Writing year: {year} quartal: {quartal}")

    dl_path = BASEURL + dp
    r = requests.get(dl_path)

    with open(tmppath / "tmp.zip", "wb") as fh:
        fh.write(r.content)

    with zipfile.ZipFile(tmppath / "tmp.zip") as zh:
        zh.extractall(tmppath)

    datafiles = tmppath.rglob("*.tsv")
    filenames_dic = {str(p.stem): str(p.resolve()) for p in datafiles}

    for file in filenames_dic:
        df = pd.read_csv(filenames_dic[file], 
                         sep = "\t", 
                         parse_dates = datecols[file], 
                         date_format = "%d-%b-%Y",
                         dtype = coltypes[file])

        df.to_sql(file, con = engine, index = False, if_exists = "append")

        if file == "SUBMISSION":
            meta_df = pd.DataFrame({"ACCESSION_NUMBER": df["ACCESSION_NUMBER"], "YEAR": year, "QUARTAL": quartal})
            meta_df.to_sql("TIMEMAP", con = engine, index = False, if_exists = "append")

def block_until_connected(engine: sqlalchemy.engine) -> None:
    """
    Run a loop that terminates when error is no longer thrown
    """
    while True:
        try:
            engine.connect()
        except SQLAlchemyError as err:
            logging.info("Trying to connect to db...")
            continue

        break

username = 'remoteuser'
password = 'password'
host = 'db'
database = 'sec13f'

engine = create_engine(f"mysql+pymysql://{username}:{password}@{host}")
block_until_connected(engine)

with engine.connect() as c:
    c.execute(text(f"CREATE DATABASE IF NOT EXISTS {database};"))

engine = create_engine(f"mysql+pymysql://{username}:{password}@{host}/{database}")

wd = Path(__file__).resolve().parent

coltypes = import_json(wd / "dataspecs/columntypes.json")
datecols = import_json(wd / "dataspecs/dateix.json")

TARGETSITE = "https://www.sec.gov/dera/data/form-13f"
BASEURL = "https://www.sec.gov"
TMPDATAPATH = wd / "datapath"

res = requests.get(TARGETSITE)
if res.status_code == 403:
    logging.error("REQUEST RATE THRESHOLD EXCEEDED: Wait before running again!")
    sys.exit()

target_html = res.content
target_parsed = bs4.BeautifulSoup(target_html, features = "html.parser")



allurls = [u.get("href") for u in target_parsed.find_all("a")]
datapaths = [ref for ref in allurls if re.search(r"\.zip$", str(ref))]

pathstr = "\n".join(datapaths)
logging.info(f"Getting data for\n{pathstr}")

TMPDATAPATH.mkdir(exist_ok = True)

fixedkwargs = {
    "engine": engine,
    "tmppath": TMPDATAPATH,
    "datecols": datecols,
    "coltypes": coltypes
}

ingestdata = partial(download_write, **fixedkwargs)
for dp in datapaths:
    ingestdata(dp)

rmtree(str(TMPDATAPATH))

### Create indexes
logging.info("Creating indexes...")
with engine.connect() as c:
    c.execute(text("CREATE FULLTEXT INDEX infotable_nameofissuer ON INFOTABLE(NAMEOFISSUER)"))
    c.execute(text("CREATE FULLTEXT INDEX coverpage_filingmanager_name ON COVERPAGE(FILINGMANAGER_NAME)"))
    c.execute(text("CREATE INDEX covertable_accession on COVERPAGE(ACCESSION_NUMBER)"))
    c.execute(text("CREATE INDEX timemap_accession on TIMEMAP(ACCESSION_NUMBER)"))
