from sklearn.base import BaseEstimator, TransformerMixin
import pandas as pd
import numpy as np
import logging 
logger = logging.getLogger(__name__)


def removeNonNumeric(df):
    return pd.DataFrame(df[df.apply(lambda row : isNumeric(row), axis=1)], dtype=np.float64)

    
def isNumeric(row):
    try:
        row.astype('float')
    except Exception as e:
        logger.info('--------------------NON-NUMERIC-DATA-ERROR--------------------')
        logger.info(row)
        logger.info(e)
        logger.info('-----------------------ERROR-ENDS-HERE------------------------')
        return False
    return True


#--------------------------------End Of Utility Common Functions---------------------------
class DataFrameSelector(BaseEstimator, TransformerMixin):

    def __init__(self, attribute_names):
        self.attribute_names = attribute_names

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        """
        Expects a list of panda data frames
        """
        tr = []
        for x in X:
            x = removeNonNumeric(x)
            tr.append(x[self.attribute_names])
        return tr

# -----------------------------End Of DataFrame Selector -------------------------


class CoordinateNormalizer(BaseEstimator, TransformerMixin):
    
    def __init__(self):
        pass
    
    def fit(self, X, y=None):
        return self
    
    def transform(self, X):
        tr = []
        for x in X:
            first_row = x.iloc[0]
            tr.append(x.apply(lambda row: self.norm(row, first_row), axis=1))
        return tr
        
    def norm(self, row, first_row):
        try:
            return row.astype('float') - first_row.astype('float')
        except Exception as e:
            logger.error(row)
            logger.error(e)
            return False
            
# ----------------------- End Of Coordinate Normalizer -------------------


class AccelerometerNormalizer(BaseEstimator, TransformerMixin):
    
    def __init__(self):
        pass
    
    def fit(self, X, y=None):
        return self
    
    def transform(self, X):
        tr = []
        for x in X:
            tr.append(x.apply(lambda row: self.norm(row), axis=1))
        return tr
        
    def norm(self, row):
        return row.astype('float')
#         return np.sign(row.astype('float'))          

# --------------------------End Of Accelerometer Normalizer---------------------


class AnalogVoltageScaler(BaseEstimator, TransformerMixin):      
    
    def __init__(self):
        pass
    
    def fit(self, X, y=None):
        return self
    
    def transform(self, X):
        tr = []
        for x in X:
            first_row = x.iloc[0]
            tr.append(x.apply(lambda row: self.norm(row, first_row), axis=1))
        return tr
    
    def norm(self, row, first_row):
        try:
            return row.astype('float') - first_row.astype('float')
        except Exception as e:
            logger.error(row)
            logger.error(e)
            return False
    
