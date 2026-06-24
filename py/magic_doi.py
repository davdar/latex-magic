# /// script
# requires-python = ">=3.14"
# dependencies = [
#   "requests",
#   "bibtexparser>=2.0b0,<3.0"
# ]
# ///

from pathlib import Path
import argparse
import tomllib
import re
import bibtexparser
import pickle

import requests

from magic_helpers import *

__VERSION__ = "0.0.0.1"

def process_command_line_arguments():
    ap = argparse.ArgumentParser(description=" ".join([ 
        "Automatically download bibtex entries",
        "from doi urls.",
    ]))
    ap.add_argument(
        "-v","--version",
        action="store_true",
        help= "Show version.")
    ap.add_argument(
       "-d","--debug",
       action="store_true",
       help="Debug mode: log internal state")
    ap.add_argument(
       "-l","--log-level",
       type=int,
       default=1,
       help="Log level to use if in debug mode.")
    ap.add_argument(
       "-s","--silent",
       action="store_true",
       help="Suppress stdout output.")
    ap.add_argument(
        "--db-file",
        default="bib/doi_db",
        help="DOI DB cache to use.")
    ap.add_argument(
        "--files",
        nargs="+",
        default=["tex/*.tex"],
        help="Input files to use.")
    ap.add_argument(
        "--bib-file",
        default="bib/magic-doi.bib",
        help="Output bib file.")
    ap.add_argument(
        "--no-cache",
        action="store_true",
        help="Do not read or write to the DOI DB cache.")
    ap.add_argument(
        "--clean-cache",
        action="store_true",
        help="Do not read (but still write) to the DOI DB cache.")
    return ap.parse_args()

def main():
    args = process_command_line_arguments()

    l = logger_silent(args.silent)
    d = logger_debug(args.debug, args.log_level)

    l.log_begin("MAGIC DOI HOOK BEGIN")

    if args.version: 
        l.log(f"VERSION: {__VERSION__}")

    d.log(1, f"args={args}")

    filenames = [ str(p) for g in args.files for p in Path().glob(g) ]
    l.log(f"FILES: {", ".join(filenames)}")

    db = {}

    if args.no_cache:
        l.log(f"NOT LOADING DB CACHE (--no-cache)")
    elif args.clean_cache:
        l.log(f"DB CACHE FILE: {args.db_file}")
        l.log(f"NOT LOADING DB CACHE (--clean-cache)")
    else:
        if Path(args.db_file).exists():
            if Path(args.db_file).stat().st_size > 0:
                l.log(f"LOADING DB FROM CACHE: {args.db_file}")
                if not isinstance(db, dict):
                    raise TypeError(f"DB file not a dictionary")
                with open(args.db_file, "rb") as f:
                    db = pickle.load(f)
            else:
                l.log(f"CACHE FILE EXISTS BUT IS EMPTY")
        else:
            l.log(f"CACHE FILE DOES NOT EXIST")

    db_keys = db.keys()
    d.log(2, f"db_keys={db_keys}")
    d.log(3, f"db={db}")

    needed_keys = set()

    for fn in filenames:
        s = Path(fn).read_text()
        dois = re.findall(r"DOI:(10\.\d+/[\w\d\-.]+)", s)
        needed_keys |= set(dois)
    
    l.log(f"DOI KEYS FOUND: {len(needed_keys)}")
    d.log(2, f"needed_keys={needed_keys}")

    cached_keys = needed_keys & db_keys
    l.log(f"CACHE HITS: {len(cached_keys)}")
    d.log(2, f"cached_keys={cached_keys}")

    new_keys = needed_keys - db_keys
    l.log(f"DOI KEYS TO FETCH: {len(new_keys)}")
    d.log(2, f"new_keys={new_keys}")

    # Extend the db by fetching new db entries

    for k in new_keys:
        try:
            l.log(f"FETCHING: https://doi.org/{k}")
            response = requests.get(
                    f"https://doi.org/{k}", 
                    headers={"Accept": "application/x-bibtex"})
            response.raise_for_status()
            db[k] = response.text.strip()
            bibtex = bibtexparser.parse_string(response.text)
            bibtex.entries[0].key = f"DOI:{k}"
            db[k] = bibtexparser.write_string(
                    bibtex,
                    prepend_middleware=[
                        bibtexparser.middlewares.SortFieldsAlphabeticallyMiddleware()
                    ])
        except requests.HTTPError as e:
            print(f"Fetching doi failed: {k}")

    l.log(f"WRITING BIB FILE")

    Path(args.bib_file).parent.mkdir(parents=True, exist_ok=True)
    with open(args.bib_file, "w") as f:
        for key, value in sorted(db.items()):
            f.write(value)
            f.write("\n")

    if not args.no_cache:
        l.log(f"WRITING CACHE FILE")
        with open(args.db_file, "wb") as f:
            pickle.dump(db, f)

    l.log_end("MAGIC DOI HOOK END  ")

if __name__ == "__main__": main()

