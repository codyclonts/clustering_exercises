# ignore warnings
import warnings
warnings.filterwarnings("ignore")

# Wrangling
import pandas as pd
import numpy as np

# Exploring
import scipy.stats as stats

# Visualizing

import matplotlib.pyplot as plt
import seaborn as sns

from env import get_db_url
import os

# default pandas decimal number display format
pd.options.display.float_format = '{:20,.2f}'.format




######################################

def get_iris_data():
    filename = 'iris_data.csv'
    
    if os.path.isfile(filename):
        return pd.read_csv(filename, index_col = 0)
    else:
        df = pd.read_sql(
        '''
        SELECT *
        FROM measurements
        JOIN species 
        USING (species_id);
        '''
        ,
        get_db_url('iris_db')
        )
        
        df.to_csv(filename)
        
        return df
