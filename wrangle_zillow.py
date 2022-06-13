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

def get_zillow_data():
    filename = 'zillow_data.csv'
    
    if os.path.isfile(filename):
        return pd.read_csv(filename, index_col = 0)
    else:
        df = pd.read_sql(
        '''
        SELECT *
        FROM properties_2017
        JOIN propertylandusetype 
        USING (propertylandusetypeid)
        JOIN predictions_2017
        USING (parcelid)
        WHERE propertylandusedesc = 'Single Family Residential';
        '''
        ,
        get_db_url('zillow')
        )
        
        df.to_csv(filename)
        
        return df


def handle_missing_values(df, prop_required_column = .5, prop_required_row = .75):
    threshold = int(round(prop_required_column * len(df.index), 0))
    df.dropna(axis=1, thresh = threshold, inplace = True)
    threshold = int(round(prop_required_row * len(df.columns), 0))
    df.dropna(axis = 0, thresh = threshold, inplace = True)
    return df
    



def split_zillow_data(df):

    train_validate, test = train_test_split(df, test_size=.2, 
        random_state=123)

    train, validate = train_test_split(train_validate, test_size=.3, 
        random_state=123)
    return train, validate, test





def wrangle_zillow():
    df =  get_zillow_data()
    df = handle_missing_values(df, prop_required_column = .9, prop_required_row = .9)
    return df



