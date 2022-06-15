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


def handle_outliers(df, cols, k):
    # Create placeholder dictionary for each columns bounds
    bounds_dict = {}

    # get a list of all columns that are not object type
    non_object_cols = df.dtypes[df.dtypes != 'object'].index


    for col in cols:
        # get necessary iqr values
        q1 = df[col].quantile(0.25)
        q3 = df[col].quantile(0.75)
        iqr = q3 - q1
        upper_bound =  q3 + k * iqr
        lower_bound =  q1 - k * iqr

        #store values in a dictionary referencable by the column name
        #and specific bound
        bounds_dict[col] = {}
        bounds_dict[col]['upper_bound'] = upper_bound
        bounds_dict[col]['lower_bound'] = lower_bound

    for col in cols:
        #retrieve bounds
        col_upper_bound = bounds_dict[col]['upper_bound']
        col_lower_bound = bounds_dict[col]['lower_bound']

        #remove rows with an outlier in that column
        df = df[(df[col] < col_upper_bound) & (df[col] > col_lower_bound)]
        return df

def handle_outliers2(df):
    df = df[(df.calculatedfinishedsquarefeet < 3900) & (df.calculatedfinishedsquarefeet > 500)]
    df = df[(df.logerror < 3) & (df.logerror > -3)]
    df = df[(df.bedroomcnt < 6) & (df.bedroomcnt > 1)]
    df = df[( df.bathroomcnt < 4) & ( df. bathroomcnt > 1)]
    df = df[(df.lotsizesquarefeet < 14000) & (df.lotsizesquarefeet > 700)]
    df = df[(df.taxvaluedollarcnt < 3500000) & (df.taxvaluedollarcnt > 100000)]
    return df



def wrangle_zillow():
    cols = [
 'bathroomcnt',
 'bedroomcnt',
 'calculatedfinishedsquarefeet',
 'lotsizesquarefeet',
 'taxvaluedollarcnt',
 'logerror']
    df =  get_zillow_data()
    df = handle_missing_values(df, prop_required_column = .9, prop_required_row = .9)
    df = handle_outliers2(df)
    df['month'] = pd.DatetimeIndex(df['transactiondate']).month
    return df




