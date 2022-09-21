import pandas as pd
import os
import numpy as np

# specify the csv file name and read it to dataframe
dispatch_data = 'Dispatch_shuffled_data_0.csv'
LMP_data = 'LMP_shuffled_data_0.csv'
df_dispatch = pd.read_csv(dispatch_data)

# convert to hdf5
print('start to convert')
filename = 'Dispatch_shuffled_data_0.h5'
df_dispatch.to_hdf(filename, 'df', mode='w', format='table')
print('convert completed')

# conclusion: unable to work because of limitation of hdf5 files header
# hdf5 files has limitation of header of 64kb (about 2000 colunms)
# https://stackoverflow.com/questions/27203161/convert-large-csv-to-hdf5
