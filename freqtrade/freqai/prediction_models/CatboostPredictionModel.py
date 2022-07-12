import logging
from typing import Any, Dict

from catboost import CatBoostRegressor, Pool

from freqtrade.freqai.prediction_models.BaseRegressionModel import BaseRegressionModel


logger = logging.getLogger(__name__)


class CatboostPredictionModel(BaseRegressionModel):
    """
    User created prediction model. The class needs to override three necessary
    functions, predict(), train(), fit(). The class inherits ModelHandler which
    has its own DataHandler where data is held, saved, loaded, and managed.
    """

    def fit(self, data_dictionary: Dict) -> Any:
        """
        User sets up the training and test data to fit their desired model here
        :params:
        :data_dictionary: the dictionary constructed by DataHandler to hold
        all the training and test data/labels.
        """

        train_data = Pool(
            data=data_dictionary["train_features"],
            label=data_dictionary["train_labels"],
            weight=data_dictionary["train_weights"],
        )

        test_data = Pool(
            data=data_dictionary["test_features"],
            label=data_dictionary["test_labels"],
            weight=data_dictionary["test_weights"],
        )

        model = CatBoostRegressor(
            allow_writing_files=False,
            verbose=100,
            early_stopping_rounds=400,
            **self.model_training_parameters,
        )
        model.fit(X=train_data, eval_set=test_data)

        return model