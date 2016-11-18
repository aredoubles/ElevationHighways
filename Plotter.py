import pandas as pd
from ggplot import *
import glob

# Empty master dataframe
# Will later concat temp DFs into it, with highway name in a column
bigdf = pd.DataFrame()

path = "elev_csv/*.csv"
for fname in glob.glob(path):
    tempdf = pd.read_csv(fname, index_col='longitude')
    tempdf['hwy'] = fname[9:12]
    if bigdf.empty: bigdf = tempdf.copy()
    else: bigdf = pd.concat([bigdf, tempdf])
bigdf.reset_index(inplace=True)

p = ggplot(bigdf, aes('longitude', 'elevation', 'hwy')) + geom_line() + xlab('Longitude') + ylab('Elevation') + \
    ggtitle('Interstate Highways') + theme_bw()

ggplot.save(p, filename='allplot.png')
