# /// script
# requires-python = ">=3.14"
# ///

import subprocess

if __name__ == "__main__": 
    print("⇒⇒⇒⇒ MAGIC SED HOOK START")

    subprocess.run(
            " ".join([
                "uv run py/magic_jinja.py",
                "--toml-files=bib/*.toml",
                "--tmpl-files=tex/**/*.tex",
                "--out-dir=.",
                "--angle-delimiters"]), 
            shell=True)

    print("⇒⇒⇒⇒ MAGIC SED HOOK END")

