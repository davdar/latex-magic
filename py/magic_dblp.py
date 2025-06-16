import argparse
import subprocess
import os
import pickle
import sys

__VERSION__ = "0.0.0.2"

def process_command_line_arguments():
    ap = argparse.ArgumentParser(description=" ".join([ 
        "Automatically create a bib file by searching latex",
        "files for occurrences of DBLP:*/*/* and automatically",
        "fetching bib entries from dblp.org. Supports caching."]))
    ap.add_argument(
        "-v","--version",
        action="store_true",
        help=" ".join([
            "Show version."]))
    ap.add_argument(
       "-d","--debug",
       action="store_true",
       help = " ".join([
           "Debug mode. Logs lots of internal scipt state"]))
    ap.add_argument(
        "--dump-db",
        action="store_true",
        help = " ".join([
            "When printing debug messages, also dump the whole db in",
            "the log message. This has no effect if `--debug` is not set"]))
    ap.add_argument(
        "--use-wget",
        action="store_true",
        help=" ".join([
            "Use `wget` as the utility for downloading files from the web.",
            "If neither `--use-wget` nor `--use-curl` are set, then infer",
            "from whichever is available on the system. If both are",
            "available, or both are selected as options, then `curl`",
            "is used."]))
    ap.add_argument(
        "--use-curl",
        action="store_true",
        help=" ".join([
            "Use `curl` as the utility for downloading files from the web.",
            "If neither `--use-wget` nor `--use-curl` are set, then infer",
            "from whichever is available on the system. If both are",
            "available, or both are selected as options, then `curl`",
            "is used."]))
    ap.add_argument(
        "--auto-input-norec",
        nargs="*",
        help=" ".join([
            "Automatically find latex files reachable from",
            "the given directories to use as files to search for the",
            "DBLP:*/*/* pattern. Does not search recursively.",
            "Supports multiple arguments."]))
    ap.add_argument(
        "--auto-input-rec",
        nargs="*",
        help=" ".join([
            "Automatically find latex files reachable from",
            "the given directories to use as files to search for the",
            "DBLP:*/*/* pattern. Searches recursively.",
            "Supports multiple arguments."]))
    ap.add_argument(
        "--auto-input-exclude",
        nargs="*",
        help=" ".join([
            "When automatically finding latex files, exclude these",
            "directories. This has no effect if `--auto-input-norec` and",
            "`--auto-input-rec` are not set.",
            "Supports multiple arguments",
            "Example arguments for `--auto-input-rec` and `--auto-input-exclude`",
            "are `*` and `excluded`, or `tex` and `tex/excluded`.",
            "Per the first example, giving arguments as `.` and `excluded` doesn't",
            "work because the internal logic uses the `find` system command, which",
            "is overly syntactic when it comes to excluded path names."]))
    ap.add_argument(
        "--db-file",
        default="dblp_db",
        help=" ".join([
            "The input/output file used for storing the database.",
            "If the file already exists, it is used as an existing",
            "database, and only new entries are fetched from the web."]))
    ap.add_argument(
        "--bib-file",
        default="dblp.bib",
        help=" ".join([
            "The output bib file. If the file already exists it is overwritten."]))
    ap.add_argument(
        "input_files",
        nargs="*",
        help=" ".join([
            "A list of files (typically latex) to search for",
            "occurrences of DBLP:*/*/*"]))
    return ap.parse_args()

def before_exit(args):
    print("↑↑↑↑ David Darais's Janky DBLP LaTeX Tool ↑↑↑↑")

def main():
    args = process_command_line_arguments()

    print("↓↓↓↓ David Darais's Janky DBLP LaTeX Tool ↓↓↓↓")

    if args.debug:   print(f"DEBUG: args={args}")
    if args.version: print(f"dblp.py: version {__VERSION__}")

    curl_command = "curl -s -L"
    wget_command = "wget -q -O -"

    fetch_url_command = None

    sys.stdout.flush()
    curl_exists = os.system("command -v curl >/dev/null 2>&1") == 0
    wget_exists = os.system("command -v wget >/dev/null 2>&1") == 0

    if args.debug: print(f"DEBUG: curl_exists={curl_exists}")
    if args.debug: print(f"DEBUG: wget_exists={wget_exists}")

    if args.use_curl:
        if not curl_exists:
            print("ERROR: `curl` specified but `curl` does not exist")
            sys.exit(1)
        fetch_url_command = curl_command
    elif args.use_wget:
        if not wget_exists:
            print("ERROR: `wget` specified but `wget` does not exist")
            sys.exit(1)
        fetch_url_command = wget_command
    elif curl_exists:
        fetch_url_command = curl_command
    elif wget_exists:
        fetch_url_command = wget_command
    else:
        print("ERROR: neither `curl` nor `wget` exists")
        sys.exit(1)

    if args.debug: print(f"DEBUG: fetch_url_command={fetch_url_command}")

    auto_input_norec_arg = " ".join(args.auto_input_norec)
    auto_input_rec_arg = " ".join(args.auto_input_rec)
    auto_input_exclude_arg = (
        " ".join(
            map((lambda x: " ".join(["-path",x,"-prune -or"])),
                args.auto_input_exclude or [])))

    if args.debug: print(f"DEBUG: auto_input_norec_arg={auto_input_norec_arg}")
    if args.debug: print(f"DEBUG: auto_input_rec_arg={auto_input_rec_arg}")
    if args.debug: print(f"DEBUG: auto_input_exclude_arg={auto_input_exclude_arg}")

    auto_input_norec_cmd = " ".join([
        f"find {auto_input_norec_arg}",
        f"{auto_input_exclude_arg}",
        f"-name '*.tex' -maxdepth 0 -print"])

    auto_input_rec_cmd = " ".join([
        f"find {auto_input_rec_arg}",
        f"{auto_input_exclude_arg}",
        f"-name '*.tex' -print"])

    if args.debug: print(f"DEBUG: auto_input_rec_cmd={auto_input_rec_cmd}")
    if args.debug: print(f"DEBUG: auto_input_norec_cmd={auto_input_norec_cmd}")
    sys.stdout.flush()

    auto_input_files = None
    if auto_input_norec_arg:
        if auto_input_rec_arg:
            # YES norec arg
            # YES rec   arg
            auto_input_files = (
                subprocess.check_output(
                    f"{auto_input_norec_cmd} && {auto_input_rec_cmd}",
                    shell=True)
                .decode("utf-8")
                .splitlines())
        else:
            # YES  norec arg
            # NO  rec   arg
            auto_input_files = (
                subprocess.check_output(
                    f"{auto_input_norec_cmd}",
                    shell=True)
                .decode("utf-8")
                .splitlines())
    else:
        if auto_input_rec_arg:
            # NO  norec arg
            # YES rec   arg
            auto_input_files = (
                subprocess.check_output(
                    f"{auto_input_rec_cmd}",
                    shell=True)
                .decode("utf-8")
                .splitlines())
        else:
            # NO  norec arg
            # NO  rec   arg
            auto_input_files = []

    if args.debug: print(f"DEBUG: auto_input_files={auto_input_files}")

    input_files_list = " ".join(set(args.input_files).union(set(auto_input_files)))

    if args.debug: print(f"DEBUG: input_files_list={input_files_list}")

    # If the `db_file` or `bib_file` have directory paths in them,
    # create those directories.
    sys.stdout.flush()
    os.system(f"mkdir -p ./{os.path.dirname(args.db_file)}")
    os.system(f"mkdir -p ./{os.path.dirname(args.bib_file)}")

    # Read the `db_file` (if it exists)
    db = None
    if os.path.exists(args.db_file):
        with open(args.db_file, "rb") as f:
            db = pickle.load(f)
    else: 
        db = {}

    # Extract the keys of the database
    db_keys = set(db.keys())

    if args.debug and args.dump_db : print(f"DEBUG: db={db}")
    if args.debug: print(f"DEBUG: db_keys={db_keys}")

    # Generate new database keys by grepping input files
    new_keys = None
    if input_files_list:
      new_keys = set(subprocess.check_output(
              " ".join([
                f"grep -hoE 'DBLP:[[:alnum:]]*/[[:alnum:]]*/[[:alnum:]-]*' {input_files_list}",
                "| sort -u",
                "| sed s/DBLP://"]),
              shell=True).decode("utf-8").splitlines())
    else:
        new_keys = set()

    if args.debug: print(f"DEBUG: new_keys={new_keys}")

    # test if the new keys includes elements not in old keys
    if new_keys.issubset(db_keys):
        print("→→→→ DBLP DATABASE - NO CHANGE")
        # touch the bib_file so that make can see it's been updated
        sys.stdout.flush()
        os.system(f"touch {args.bib_file}")
    else:
        print("→→→→ DBLP DATABASE - CHANGED")
        # Build the bib file. For each key, look it up in the db, or
        # fetch it if it's not already there.
        for key in new_keys:
            value = None
            if key in db:
                # value is in the old db, reuse it
                print(f"→→→→ CACHED dblp.org/rec/{key}.bib")
                sys.stdout.flush()
            else:
                # value is not in the old db, fetch it and cache it
                print(f"→→→→ FETCHING dblp.org/rec/{key}.bib")
                sys.stdout.flush()
                try:
                    value = subprocess.check_output(
                            f"{fetch_url_command} dblp.org/rec/{key}.bib", 
                            shell=True).decode("utf-8")
                    print(f"→→→→ RECEIVED dblp.org/rec/{key}.bib")
                    sys.stdout.flush()
                    db[key] = value
                except:
                    print(f"→→→→ ERROR: Fetching url via `{fetch_url_command}` failed.")
                    sys.stdout.flush()
                    before_exit(args)
                    exit(1)

    # save the updated db
    with open(args.db_file, "wb") as f:
        pickle.dump(db, f)

    new_bib_contents = "\n".join(map(lambda key: f"% {key}\n{db[key]}",sorted(new_keys)))
    if args.debug and args.dump_db: print(f"DEBUG: new_bib_contents={new_bib_contents}")

    old_bib_contents = None
    if os.path.exists(args.bib_file):
        with open(args.bib_file, "rb") as f:
            old_bib_contents = f.read().decode("utf-8")

    if args.debug and args.dump_db: print(f"DEBUG: old_bib_contents={old_bib_contents}")

    if old_bib_contents == new_bib_contents:
        print(f"→→→→ BIB FILE - NO CHANGE")
    else:
        print(f"→→→→ BIB FILE - CHANGED")
        with open(args.bib_file, "wb") as f: 
            f.write(new_bib_contents.encode("utf-8"))

    before_exit(args)

if __name__ == "__main__": main()
