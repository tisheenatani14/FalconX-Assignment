import pandas as pd
import os
import glob

#retrieving all the 3 files and saving in pandas

path = os.getcwd()
csv_files = glob.glob(os.path.join(path, "*.csv"))
data = []
for f in csv_files:
    df = pd.read_csv(f)
