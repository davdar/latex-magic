# /// script
# requires-python = ">=3.14"
# dependencies = [
#   "jinja2",
#   "deepmerge",
# ]
# ///

from pathlib import Path
import argparse
import tomllib
from deepmerge import always_merger

import jinja2

from magic_helpers import *

__VERSION__ = "0.0.0.1"

def process_command_line_arguments():
    ap = argparse.ArgumentParser(description=" ".join([ 
        "Concatenates all of the toml files <toml-files>",
        "and uses them as the data object for",
        "processing jinja template files <tmpl-files>.",
        "Output files are placed in <out-dir>.",
    ]))
    ap.add_argument(
        "-v","--version",
        action="store_true",
        help= "Show version.")
    ap.add_argument(
       "-d","--debug",
       action="store_true",
       help="Debug mode: log internal state.")
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
        "--toml-files",
        nargs="+",
        default=["toml/*"],
        help="Toml files to use.")
    ap.add_argument(
        "--tmpl-files",
        nargs="+",
        default=["tmpl/*"],
        help="Tmpl files to use")
    ap.add_argument(
        "--out-dir",
        default="out",
        help="Output directory")
    ap.add_argument(
        "--angle-delimiters",
        action="store_true",
        help="Change jinja delimieters to angle brackets.")
    return ap.parse_args()

def main():
    args = process_command_line_arguments()

    l = logger_silent(args.silent)
    d = logger_debug(args.debug, args.log_level)

    l.log_begin("MAGIC JINJA HOOK BEGIN")

    if args.version: l.log(f"VERSION: {__VERSION__}")

    d.log(1, f"args={args}")

    toml_filenames = [ str(p) for g in args.toml_files for p in Path().glob(g) ]
    tmpl_filenames = [ str(p) for g in args.tmpl_files for p in Path().glob(g) ]

    l.log(f"TOML FILES: {", ".join(toml_filenames)}")
    l.log(f"TMPL FILES: {", ".join(tmpl_filenames)}")

    toml_data = {}
    for fn in toml_filenames:
        always_merger.merge(toml_data, tomllib.loads(Path(fn).read_text()))

    d.log(2, f"toml_data={toml_data}")

    env = jinja2.Environment()
    if args.angle_delimiters:
        env = jinja2.Environment(
                variable_start_string="<<",
                variable_end_string=">>",
                block_start_string="<@",
                block_end_string="@>",
                comment_start_string="<#",
                comment_end_string="#>",
                )

    for fn in tmpl_filenames:
            tmpl_in = Path(fn).read_text()
            d.log(3, f"tmpl_in=")
            d.log(3, "\n".join([
                f".... {line}"
                for line in tmpl_in.splitlines()
            ]))
            tmpl_out = env.from_string(tmpl_in).render(**toml_data)
            d.log(3, f"tmpl_out=")
            d.log(3, "\n".join([
                f".... {line}"
                for line in tmpl_out.splitlines()
            ]))
            fn = f"{args.out_dir}/{fn}"
            l.log(f"WRITING FILE: {fn}") 
            p = Path(fn)
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(tmpl_out)
    l.log_end("MAGIC JINJA HOOK END  ")

if __name__ == "__main__": main()
