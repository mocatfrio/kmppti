import sys
import os
import pandas as pd
import matplotlib.pyplot as plt
from dotenv import load_dotenv


load_dotenv()

try:
    p_filename = sys.argv[1]
except:
    p_filename = None
try:
    c_filename = sys.argv[2]
except:
    c_filename = None

p_df = None
c_df = None
if p_filename:
    p_filepath = os.getenv("DATASET_PATH") + p_filename
    p_df = pd.read_csv(p_filepath)
if c_filename:
    c_filepath = os.getenv("DATASET_PATH") + c_filename
    c_df = pd.read_csv(c_filepath)

if not p_df is None and not c_df is None:
    frames = [p_df, c_df]
    df = pd.concat(frames)
elif not p_df is None:
    df = p_df
elif not c_df is None:
    df = c_df

if p_filename.split("_")[0] == "fc":
    x_attr = "Aspect"
    y_attr = "Slope"
else:
    x_attr = "attr_1"
    y_attr = "attr_2"

graph = df.plot(kind='scatter',x=x_attr, y=y_attr, color='Black') # scatter plot
graph.set_xlabel("")
graph.set_ylabel("")
plt.show()