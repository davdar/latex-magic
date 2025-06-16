import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import py.magic_dblp

if __name__ == "__main__": 
    print("MAGIC DBLP HOOK START")

    sys.argv = "magic_dblp.py --auto-input-norec * --auto-input-rec tex --debug".split()

    py.magic_dblp.main()

    print("MAGIC DBLP HOOK END")
