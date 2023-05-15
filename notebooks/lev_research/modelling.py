# %%
import pandas as pd

# base metric in this competition is roc_auc
from sklearn.metrics import RocCurveDisplay, roc_auc_score, roc_curve

# scikit-learn base he-he
from sklearn.model_selection import GridSearchCV, StratifiedKFold, train_test_split


# %%
class ModelValidator:
    """Cross validator for model"""

    def grid_validate(self, X, y, model, param_grid, scoring):
        """Method to process cross-validation

        Parameters
        ----------
        X: pd.DataFrame
            Data for train and validate the model

        y: pd.Series
            Target data

        model: Pipeline
            Machine learning pipeline

        param_grid: dict
            Grid with model parameters

        scoring: str
            Name of metric

        Returns
        -------
        best_score: float
            The best score on CV

        best_params: dict
            The best combination of parameters

        """

        gsv = GridSearchCV(
            estimator=model,
            param_grid=param_grid,
            scoring=scoring,
            verbose=2,
            cv=StratifiedKFold(4, shuffle=True, random_state=43),
        )
        gsv.fit(X, y)
        best_score, best_params = gsv.best_score_, gsv.best_params_
        print(f"Best score on CV: {best_score}. Best params are: {best_params}")
        return best_score, best_params


class RocCurveDrawer:
    def plot_draw(self, y_true: np.ndarray, y_pred: np.ndarray) -> None:
        """Method to draw ROC curve

        Parameters
        ----------
        y_true : np.ndarray
            Real true predictions

        y_pred: np.ndarray
            Predictions

        Returns
        -------
        None
        """
        fpr, tpr, thresholds = roc_curve(y_true, y_pred)
        base_metric = roc_auc_score(y_true, y_pred)
        print(f"ROC-AUC score is {base_metric}")
        display = RocCurveDisplay(fpr=fpr, tpr=tpr, roc_auc=base_metric)
        display.plot()


# %%
# catboost
# Best score on CV: 0.8892123900304957. Best params are:
# {'model__depth': 6, 'model__iterations': 400,
# 'model__learning_rate': 0.04,'model__subsample': 0.6}
