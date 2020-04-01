import pandas as pd
import numpy as np
from model import generteTrainAndTestSet, setupAndTrainModel, evaluate, showInfo

def prepearModel(candlesticsAndFeaturesWithTargetHistory: pd.DataFrame):
    X_train, X_test, y_train, y_test = generteTrainAndTestSet(
        candlesticsAndFeaturesWithTargetHistory
    )
    xg_reg = setupAndTrainModel(X_train, y_train)
    evaluate(xg_reg, X_test, y_test)
    showInfo(xg_reg)
    return xg_reg

def generateSignals(model, period: pd.DataFrame) -> pd.DataFrame:
    result = pd.DataFrame(period.copy())

    period = period.drop(columns=["open time", "close time"])
    period = period.drop(period.columns[1], axis=1).iloc[:, :-1]
    result["pred"] = model.predict(period)

    upTreshold = 0.4
    downTreshold = -0.2
    conditions = [result["pred"] > upTreshold, result["pred"] < downTreshold]
    choices = ["BUY", "SELL"]
    result["trade"] = np.select(conditions, choices, default="none")
    result["trade price"] = result.shift(periods=-1)["open"]
    return result
