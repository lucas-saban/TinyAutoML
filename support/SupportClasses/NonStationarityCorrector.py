import logging
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import StandardScaler
from statsmodels.tsa.stattools import adfuller
from ..constants.GLOBAL_PARAMS import WINDOW

class NonStationarityCorrector(BaseEstimator, TransformerMixin):
    """
    Correct columns that don't seem stationary according to Augmented Dicker Fuller statistical stationarity test
    """

    def __init__(self, colsToKeepIntact=None):
        # If the user wants some columns to remain intact, they can be passed as arguments
        if colsToKeepIntact is None:
            colsToKeepIntact = []
        self.colsToKeepIntact = colsToKeepIntact
        self.colsToCorrect = []

    def fit(self, X: pd.DataFrame, y: pd.Series) -> TransformerMixin:
        for col in X.columns:
            if col not in self.colsToKeepIntact:
                test_results = adfuller(X[col].values)[0]
                if test_results < 0:
                    self.colsToCorrect.append(col)
                else:
                    self.colsToKeepIntact.append(col)

        assert len(self.colsToKeepIntact) + len(self.colsToCorrect) == len(X.columns), "Column(s) were lost in process"

        return self

    def transform(self, X: pd.DataFrame, y=None) -> pd.DataFrame:
        X = X.copy()
        logging.info("Correcting non-stationarity on the dataset...")
        print(X)
        if X.shape[0]>WINDOW:
            for col in self.colsToCorrect:
                # Depending on the window size, std can be null.
                # In that situation the actual value can be replaced by the last non null value
                start = X.index[0]
                # We also use loc[start+WINDOW:] in order to leave the WINDOW first rows intact. Otherwise, it would be nans
                X[col].loc[start+WINDOW:] = (X[col] - X[col].rolling(window=WINDOW).mean()) / X[col].rolling(window=WINDOW).std(
                    skipna=True).replace(to_replace=0., method='ffill').loc[start+WINDOW:]

            if self.colsToKeepIntact: X[self.colsToKeepIntact] = StandardScaler().fit_transform(X[self.colsToKeepIntact])
            print(X)
            return X

        else:
            X[X.columns] = StandardScaler().fit_transform(X[X.columns])
            assert type(X) == pd.DataFrame, 'type error'
            return X
