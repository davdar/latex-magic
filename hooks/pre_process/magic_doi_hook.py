# /// script
# requires-python = ">=3.14"
# ///

import subprocess

if __name__ == "__main__": 
    print("⇒⇒⇒⇒ MAGIC SED HOOK START")

    subprocess.run("uv run py/magic_doi.py", shell=True)

    print("⇒⇒⇒⇒ MAGIC SED HOOK END")
