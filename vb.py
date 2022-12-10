import pandas as pd
import sys

print(pd.read_csv(sys.argv[-1]).groupby(['state', 'protocol'])[['voltage_base']].describe())
