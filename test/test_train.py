import joblib
import os
from train import train_and_save_model

def test_train_and_save_model():
    train_and_save_model()
    
    assert os.path.exists('model.joblib')
    
    model = joblib.load('model.joblib')
    from sklearn.ensemble import RandomForestClassifier
    assert isinstance(model, RandomForestClassifier)
