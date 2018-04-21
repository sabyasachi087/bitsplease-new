from sklearn.base import BaseEstimator, ClassifierMixin
from predictor.dtw import fastdtw
import numpy as np
import pandas as pd

class DTWClassifier(BaseEstimator, ClassifierMixin):  

    def __init__(self, neighbours=5, dist='minkowski', normalize=False):
        """
        dist: Distance metrics - euclidean, minkowski
        neighbours: Nearest neighbours
        """       
        self.neighbours = neighbours
        self.dist = dist
        self.normalize = normalize

    def fit(self, X, y):
        self.X = X
        self.y = np.array(y)
        return self

    def predict(self, x_test):
        pred = []; err = []
        for id_test in range(len(x_test)):
            result = np.zeros(len(self.y))
            for id_train in range(len(self.X)):
                try:
                    min_dist = fastdtw(self.X[id_train], x_test[id_test], self.dist)                    
                    result[id_train] = min_dist
                except Exception as e:
                    print(self.y[id_train]) 
                    print(self.X[id_train]) 
                    print(x_test[id_test])    
                    print(e)
            if(self.normalize):
                result = self.norm(result)       
            res_indx = result.argsort()[:self.neighbours]
            pred.append((self.y[res_indx], result[res_indx]))
        return pred
    
    def _naive_bayes_prob(self, X_test):        
        preds = self.predict([X_test])
        resultDf = pd.DataFrame(columns=['gesture', 'distance'])
        for gesture, distance in preds:        
            for idx in range(len(gesture)):
                resultDf.loc[len(resultDf)] = [gesture[idx], distance[idx]]
        resultDf['distance'] = resultDf['distance'].apply(lambda x : (1 - x) / len(resultDf))
        resultDf = resultDf.groupby(['gesture'], as_index=False).sum()
        total_dist = resultDf['distance'].sum()
        resultDf['distance'] = resultDf['distance'].apply(lambda x : x / total_dist)
        gest_res = resultDf.ix[resultDf['distance'].idxmax()]
        return (gest_res["gesture"], gest_res["distance"])
    
    def norm(self, x):
        max_x = np.max(x);min_x = np.min(x)
        if (max_x - min_x) == 0:
            print(x)
            return np.ones(len(x))
        else:
            return (x - min_x) / (max_x - min_x)
        
    def score(self, X, y):
        score = [];preds = []
        for _x in X:
            preds.append(self._naive_bayes_prob(_x))
        for indx in range(len(y)):
            if y[indx] == preds[indx][0]:
                score.append(preds[indx][1])
            else:
                score.append(0.)
        return np.average(score)
