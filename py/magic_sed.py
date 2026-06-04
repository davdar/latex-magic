# /// script
# requires-python = ">=3.14"
# ///

import subprocess
import os
import sys
import argparse

__VERSION__ = "0.0.0.2"

def process_command_line_arguments():
    ap = argparse.ArgumentParser(description=" ".join([ 
        "Automatically processes all input files given a folder",
        "full of sed files. Files are processed in-place."]))
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
        "--recursive",
        action="store_true",
        help = " ".join([
            "When using `--auto-input`, search the folder recursively"]))
    ap.add_argument(
        "--auto-input-norec",
        nargs="*",
        help=" ".join([
            "Automatically find latex files reachable from",
            "the given directories to use as files to process.",
            "Does not search recursively.",
            "Supports multiple arguments."]))
    ap.add_argument(
        "--auto-input-rec",
        nargs="*",
        help=" ".join([
            "Automatically find latex files reachable from",
            "the given directories to use as files to process.",
            "Searches recursively.",
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
        "--sed-folder",
        default="sed",
        help=" ".join([
            "The folder in which to search for sed files."]))
    ap.add_argument(
        "input_files",
        nargs="*",
        help=" ".join([
            "A list of files (typically latex) to to process"]))
    return ap.parse_args()

def before_exit(args):
    print("↑↑↑↑ David Darais's Janky Sed Processing Tool ↑↑↑↑")

def main():
    args = process_command_line_arguments()

    print("↓↓↓↓ David Darais's Janky Sed Processing Tool ↓↓↓↓")

    if args.debug:   print(f"DEBUG: args={args}")
    if args.version: print(f"dblp.py: version {__VERSION__}")

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

    sed_files = " ".join(sorted(
        subprocess.check_output(f"find {args.sed_folder} -name '*.sed'",shell=True)
        .decode("utf-8")
        .splitlines()))

    if args.debug: print(f"DEBUG: sed_files={sed_files}")

    cmd = " ".join([
        f"for F in {input_files_list} ; do",
        f"  cp $F $F.bu && {{ cat {sed_files} | sed -E -f - $F.bu > $F ; }} && rm $F.bu ; ",
        f"done"])
    if args.debug: print(f"DEBUG: cmd={cmd}")
    sys.stdout.flush()
    os.system(cmd)

    print("→→→→ SED PROCESSING DONE")
    before_exit(args)

if __name__ == "__main__": main()
