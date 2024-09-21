
import pandas as pd
from EcoOpen.core import *

from pathlib import Path
import os
import pdf2doi
from tqdm import tqdm


path = "/home/domagoj/Documents/data.pdf"

# paths = list(Path("/"))


das, dl = find_dataKW(path)

dl