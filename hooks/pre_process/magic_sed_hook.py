import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import py.magic_sed

if __name__ == "__main__": 
    print("MAGIC SED HOOK START")

    sys.argv = "magic_sed.py --auto-input-norec * --auto-input-rec tex --debug".split()

    py.magic_sed.main()

    print("MAGIC SED HOOK END")
