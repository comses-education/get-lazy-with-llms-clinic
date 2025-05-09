# This allows running the package using 'python -m promptbuilder'
import sys
from .cli import main

if __name__ == "__main__":
    sys.exit(main())