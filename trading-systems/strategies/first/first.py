from lib.strategy import Strategy
import pandas as pd
from lib.data_splitter import split_features_and_target_into_train_and_test_set
from dataclasses import InitVar
from models.xgboost.model import XgboostNovice
from lib.tradingSignal import TradingSignal
from dataclasses import dataclass
import abc
from typing import List


@dataclass
class First(Strategy):

    init_candlesticks: InitVar[pd.DataFrame]
    xgboost_novice: XgboostNovice = None

    def __post_init__(self, init_features: pd.DataFrame) -> None:
        self.xgboost_novice = XgboostNovice()
        self.__train(init_features)

    def execute(self, candlesticks: pd.DataFrame, signals: pd.DataFrame) -> TradingSignal:
        features = self.generate_features(candlesticks)
        return self.execute_with_features(features, signals)

    def execute_with_features(self, features: pd.DataFrame, signals: pd.DataFrame) -> TradingSignal:
        if len(features) % 100 == 0:
            print("First Strategy - Start retraining.")
            self.__train(features)
            print("First Strategy - End retraining.")

        prediction = self.xgboost_novice.predict(features)
        return self._execute(features, signals, [prediction])

    def _execute(self, features: pd.DataFrame, signals: pd.DataFrame, predictions: List[float]) -> TradingSignal:
        last_signal = TradingSignal.SELL if len(signals) == 0 else signals.tail(1)["signal"].values[0]
        prediction = predictions[0]

        if last_signal == TradingSignal.SELL and prediction > 1.5:
            return TradingSignal.BUY
        elif last_signal == TradingSignal.BUY and prediction < 0.5:
            return TradingSignal.SELL


    @staticmethod
    def generate_features(candlesticks: pd.DataFrame) -> pd.DataFrame:
        """Should return a dataframe containing all features needed by this strategy (for all its models etc)"""
        xgboostNoviceFeatures = XgboostNovice.generate_features(candlesticks)
        return xgboostNoviceFeatures

    def __train(self, features: pd.DataFrame):
        target = self._generate_target(features)
        (
            training_set_features,
            training_set_target,
            _,
            _,
        ) = split_features_and_target_into_train_and_test_set(features, target, 0)

        self.xgboost_novice.train(training_set_features, training_set_target)

    @staticmethod
    def _generate_target(features: pd.DataFrame) -> pd.DataFrame:
        return XgboostNovice.generate_target(features)
