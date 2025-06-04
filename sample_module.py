# sample_module.py - A file with various import statements for testing.

import os
import sys
import json, csv # Multiple imports on one line (simple case)

from datetime import datetime, date as d_alias
from collections import Counter, defaultdict, deque as custom_deque

import numpy as np
import pandas as pd

# A more complex from import
from concurrent.futures import (
    ThreadPoolExecutor,
    ProcessPoolExecutor,
    wait as wait_futures
)

# Some comments
# import commented_out_module

def a_function():
    # Test import inside a function (should not be picked up as module dependency by simple AST top-level scan)
    # import local_module
    pass

class SomeClass:
    # import another_local_module
    pass

if __name__ == '__main__':
    print(f"os imported: {os}")
    print(f"datetime imported: {datetime}")
    print(f"Counter imported: {Counter}")
    print(f"numpy (as np) imported: {np}")
    print(f"ThreadPoolExecutor imported: {ThreadPoolExecutor}")
