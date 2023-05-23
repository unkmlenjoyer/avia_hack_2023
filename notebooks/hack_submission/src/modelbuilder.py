from catboost import CatBoostClassifier


class ModelBuilder:
    """Class for construction Catboost models"""

    @staticmethod
    def from_file(path: str) -> CatBoostClassifier:
        """Create model from file

        Parameters
        ----------
        path : str
            Path to model file

        Returns
        -------
        model : CatBoostClassifier
            Pretreined classifier for service
        """

        model = CatBoostClassifier()
        model.load_model(path)

        return model
