from sklearn.base import BaseEstimator
import numpy as np
import time
import logging 
import pandas as pd


class HandGestureEnsembler(BaseEstimator):
    
    def __init__(self, pipelines, pt=None):
        """ @param 
            pt (in %) -> Probability Threshold, Minimum matching probability
            for deciding on the gesture. Default value is 75%
        """
        if len(pipelines) == 0:
            raise Exception("No pipelines are defined") 
        self.pipelines = pipelines
        if pt:
            self.probability_threshold = pt / 100
        else:
            self.probability_threshold = None
        self.logger = logging.getLogger(__name__)
    
    def fit(self, X_train, y_train=None):
        for pl in self.pipelines:
            pl.fit(X_train, y_train)            
        return self
    
    def predict(self, X_tests):
        deciders = []
        for X_test in X_tests:
            res = self._decider(X_test)
            if self.probability_threshold != None:
                if res[1] >= self.probability_threshold:
                    deciders.append(res)
                else:
                    deciders.append(('NA', 0.))
            else:
                deciders.append(res)
        return deciders
        
    
    def _decider(self, X_test):
        start_time = time.time()
        for pl in self.pipelines:
            preds = pl.predict([X_test])
            resultDf = pd.DataFrame(columns=['gesture', 'distance'])
            for gesture, distance in preds:        
                for idx in range(len(gesture)):
                    resultDf.loc[len(resultDf)] = [gesture[idx], distance[idx]]
        resultDf['distance'] = resultDf['distance'].apply(lambda x : (1 - x) / len(resultDf))
        resultDf = resultDf.groupby(['gesture'], as_index=False).sum()
        total_dist = resultDf['distance'].sum()
        resultDf['distance'] = resultDf['distance'].apply(lambda x : x / total_dist)
        gest_res = resultDf.ix[resultDf['distance'].idxmax()]
        self.logger.info('Prediction completed in %f seconds' % (time.time() - start_time))
        return (gest_res["gesture"], gest_res["distance"])

    def score(self, X_tests, y):
        score = []
        preds = self.predict(X_tests)
        for indx in range(len(y)):
            if y[indx] == preds[indx][0]:
                score.append(preds[indx][1])
            else:
                score.append(0.)
        return np.average(score)
            
