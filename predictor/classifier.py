import predictor.curator as crt
from predictor.gesture_transformers import CoordinateNormalizer, AccelerometerNormalizer, DataFrameSelector, AnalogVoltageScaler
from sklearn.pipeline import Pipeline
from predictor.dtw_classifier import DTWClassifier
from predictor.gesture_ensembler import HandGestureEnsembler

from logger.app_logger import setup_logging
setup_logging()

        
def init():
    X_train, y_train = crt.getTrainData()
    gyro_attr_names = ["cord_x", "cord_y", "cord_z"]
    acc_attr_names = ["tilt_x", 'tilt_y', 'tilt_z']
    fgr_attr_names = ['thumb', 'index', 'middle', 'ring', 'little']
    
    all_pipelines = []
    gyro_pipeline = Pipeline([       
            ('selector', DataFrameSelector(gyro_attr_names)),
            ('cord_norm', CoordinateNormalizer()),
            ('estimator', DTWClassifier(neighbours=3, dist='euclidean', normalize=True)),
        ])
    all_pipelines.append(gyro_pipeline)
    
    acc_pipeline = Pipeline([       
            ('selector', DataFrameSelector(acc_attr_names)),
            ('acc_norm', AccelerometerNormalizer()),
            ('estimator', DTWClassifier(neighbours=3,normalize=True)),
        ])
    all_pipelines.append(acc_pipeline)
    
    flex_pipeline = Pipeline([       
            ('selector', DataFrameSelector(fgr_attr_names)),
            ('std_scaler', AnalogVoltageScaler()),
            ('estimator', DTWClassifier(neighbours=2, normalize=True)),
        ])
    all_pipelines.append(flex_pipeline)
    
    ensember = HandGestureEnsembler(all_pipelines, pt=75)
    ensember.fit(X_train, y_train)
    print('Ensembler is trained and ready for prediction ')
    return ensember

