import requests
from shutil import rmtree
import bs4
import re
from pathlib import Path
import pandas as pd
import zipfile
import pymysql
from sqlalchemy import create_engine, text

username = 'remoteuser'
password = 'password'
host = 'localhost'
database = 'sec13f'

engine = create_engine(f"mysql+pymysql://{username}:{password}@{host}")

with engine.connect() as c:
    c.execute(text(f"CREATE DATABASE IF NOT EXISTS {database};"))

engine = create_engine(f"mysql+pymysql://{username}:{password}@{host}/{database}")

TARGETSITE = "https://www.sec.gov/dera/data/form-13f"
BASEURL = "https://www.sec.gov"
TMPDATAPATH = Path(__file__).resolve().parent / "datapath"

target_html = requests.get(TARGETSITE).content
target_parsed = bs4.BeautifulSoup(target_html, features = "html.parser")

allurls = [u.get("href") for u in target_parsed.find_all("a")]
datapaths = [ref for ref in allurls if re.search(r"\.zip$", str(ref))]

TMPDATAPATH.mkdir(exist_ok = True)

for dp in datapaths:
    filestem = Path(dp).stem
    year, quartal = filestem.replace("_form13f", "").split("q")
    print(f"Writing year: {year} quartal: {quartal}")

    dl_path = BASEURL + dp
    r = requests.get(dl_path)

    with open(TMPDATAPATH / "tmp.zip", "wb") as fh:
        fh.write(r.content)

    with zipfile.ZipFile(TMPDATAPATH / "tmp.zip") as zh:
        zh.extractall(TMPDATAPATH)

    datafiles = TMPDATAPATH.rglob("*.tsv")
    filenames_dic = {str(p.stem): str(p.resolve()) for p in datafiles}
    for file in filenames_dic:
        df = pd.read_csv(filenames_dic[file], sep = "\t")
        df.to_sql(file, con = engine, index = False, if_exists = "append")

        if file == "SUBMISSION":
            meta_df = pd.DataFrame({"ACCESSION_NUMBER": df["ACCESSION_NUMBER"], "YEAR": year, "QUARTAL": quartal})
            meta_df.to_sql("TIMEMAP", con = engine, index = False, if_exists = "append")
            
rmtree(str(TMPDATAPATH))

### Create indexes
print("Creating indexes...")
with engine.connect() as c:
    c.execute(text("CREATE FULLTEXT INDEX infotable_nameofissuer ON INFOTABLE(NAMEOFISSUER)"))
    c.execute(text("CREATE FULLTEXT INDEX coverpage_filingmanager_name ON COVERPAGE(FILINGMANAGER_NAME)"))
    c.execute(text("CREATE INDEX covertable_accession on COVERPAGE(ACCESSION_NUMBER)"))
    c.execute(text("CREATE INDEX timemap_accession on TIMEMAP(ACCESSION_NUMBER)"))
