import pandas as pd
import os
import numpy as np

for i in range(682052,682152):
    os.system(f"qdel -j {i}")