# %%
from typing import Dict

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from catboost import CatBoostClassifier, Pool

# base metric in this competition is roc_auc
from sklearn.metrics import (
    PrecisionRecallDisplay,
    RocCurveDisplay,
    classification_report,
    precision_recall_curve,
    roc_auc_score,
    roc_curve,
)

# scikit-learn base he-he
from sklearn.model_selection import GridSearchCV, StratifiedKFold, train_test_split

# %%
# set seaborn settings
sns.set_style("darkgrid")

# %%
RANDOM_SEED = 42


# %%
def get_importance(model: CatBoostClassifier, X: pd.DataFrame):
    """Fucntion to print model feature importance

    Parameters
    ----------
    model : CatBoostClassifier
        Model ML
    X : pd.DataFrame
        Data with columns to check
    """
    for col, imp in sorted(
        zip(model.get_feature_importance(), X.columns.values),
        key=lambda item: item[0],
        reverse=True,
    ):
        print(col, imp)


# %%
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
        base_metric = roc_auc_score(y_true, y_pred, average="weighted")
        print(f"ROC-AUC score is {base_metric}")
        display = RocCurveDisplay(fpr=fpr, tpr=tpr, roc_auc=base_metric)
        display.plot()


# %%
class ModelValidator:
    def grid_validate(
        self,
        X: pd.DataFrame,
        y: pd.Series,
        model: CatBoostClassifier,
        param_grid: Dict,
        scoring: str,
    ):
        """Method to process cross-validation

        Parameters
        ----------
        X: pd.DataFrame
            Data for train and validate the model

        y: pd.Series
            Target data

        model: CatBoostClassifier
            Machine learning pipeline

        param_grid: Dict
            Grid with model parameters

        scoring: str
            Name of metric
        """

        gsv = GridSearchCV(
            estimator=model,
            param_grid=param_grid,
            scoring=scoring,
            verbose=3,
            cv=StratifiedKFold(4, shuffle=True, random_state=RANDOM_SEED),
            return_train_score=True,
        )
        gsv.fit(X, y)

        return gsv


# %%
data = pd.read_csv("/kaggle/input/hack-test-new/calculated_features.csv", index_col=0)

# %%
data.columns

# %%
TARGET = "SentOption"
ONE_WAY_COLS = [
    "TravellerGrade",
    "SegmentCount",
    "Amount",
    "class",
    "IsBaggage",
    "isRefundPermitted",
    "isExchangePermitted",
    "isDiscount",
    "InTravelPolicy",
    "forw_hours",
    "forw_hours_diff_min",
    "forw_hours_diff_mean",
    "req_dep_hours_diff",
    "price_diff_min_perc",
    "price_diff_mean_perc",
    "is_direct",
    "SentOption",
]

TWO_WAY_COLS = [
    "TravellerGrade",
    "SegmentCount",
    "Amount",
    "class",
    "IsBaggage",
    "isRefundPermitted",
    "isExchangePermitted",
    "isDiscount",
    "InTravelPolicy",
    "forw_hours",
    "back_hours",
    "total_hours",
    "forw_hours_diff_min",
    "forw_hours_diff_mean",
    "back_hours_diff_min",
    "back_hours_diff_mean",
    "req_dep_hours_diff",
    "req_ret_hours_diff",
    "price_diff_min_perc",
    "price_diff_mean_perc",
    "is_direct",
    "SentOption",
]

# %%
one_way_df = data[data.back_hours.isna()][ONE_WAY_COLS]
two_way_df = data[~data.back_hours.isna()][TWO_WAY_COLS]

# %%
X_one, y_one = one_way_df.drop(columns=[TARGET]), one_way_df[TARGET]
X_two, y_two = two_way_df.drop(columns=[TARGET]), two_way_df[TARGET]

# %%
X_train_one, X_test_one, y_train_one, y_test_one = train_test_split(
    X_one, y_one, shuffle=True, stratify=y_one, test_size=0.2, random_state=RANDOM_SEED
)

X_train_two, X_test_two, y_train_two, y_test_two = train_test_split(
    X_two, y_two, shuffle=True, stratify=y_two, test_size=0.2, random_state=RANDOM_SEED
)

# %%
cat_features_one = X_one.select_dtypes(include="object").columns.values
cat_features_two = X_two.select_dtypes(include="object").columns.values

# %%
train_dataset_one = Pool(
    data=X_train_one, label=y_train_one, cat_features=cat_features_one
)

eval_dataset_one = Pool(
    data=X_test_one, label=y_test_one, cat_features=cat_features_one
)

train_dataset_two = Pool(
    data=X_train_two, label=y_train_two, cat_features=cat_features_two
)
eval_dataset_two = Pool(
    data=X_test_two, label=y_test_two, cat_features=cat_features_two
)

# %%
model_one_params = {
    "depth": 4,
    "iterations": 200,
    "l2_leaf_reg": 5,
    "learning_rate": 0.1,
    "subsample": 0.6,
    "loss_function": "Logloss",
    "cat_features": cat_features_one,
    "task_type": "CPU",
    "bootstrap_type": "Bernoulli",
    "random_seed": 7575,
    "auto_class_weights": "SqrtBalanced",
    "verbose": False,
    "eval_metric": "PRAUC:type=Classic;use_weights=False",
    "border_count": 254,
}

model_two_params = {
    "depth": 4,
    "iterations": 160,
    "l2_leaf_reg": 7,
    "learning_rate": 0.1,
    "subsample": 0.6,
    "loss_function": "Logloss",
    "cat_features": cat_features_one,
    "task_type": "CPU",
    "bootstrap_type": "Bernoulli",
    "random_seed": 7575,
    "auto_class_weights": "SqrtBalanced",
    "verbose": False,
    "eval_metric": "PRAUC:type=Classic;use_weights=False",
    "border_count": 254,
}


# %%
# fit params
model_one_way = CatBoostClassifier(**model_one_params)
model_two_way = CatBoostClassifier(**model_two_params)

# %%
validator = ModelValidator()

# %%
param_distribution = {
    "iterations": [150, 200, 300],
    "learning_rate": [0.01, 0.1, 0.3],
    "l2_leaf_reg": [5, 7],
    "depth": [4, 5, 6],
    "subsample": [0.4, 0.6, 1.0],
}

# %%
res_val = validator.grid_validate(
    X_train_one, y_train_one, model_one_way, param_distribution, "average_precision"
)

# %%
res_val = validator.grid_validate(
    X_train_two, y_train_two, model_two_way, param_distribution, "average_precision"
)

# %%
res_cv_df = pd.DataFrame(res_val.cv_results_)

# %%
res_cv_df[
    abs(res_cv_df.mean_test_score - res_cv_df.mean_train_score) < 0.025
].sort_values(by="mean_test_score", ascending=False).iloc[0].params

# %%
randomized_search_result = model_one_way.grid_search(
    param_distribution, train_dataset_one, cv=StratifiedKFold(4)
)

# %%
model_one_way.fit(
    train_dataset_one, eval_set=eval_dataset_one, use_best_model=True, verbose=20
)

# %%
model_two_way.fit(
    train_dataset_two, eval_set=eval_dataset_two, use_best_model=True, verbose=20
)

# %%
y_one_test_probas_pred = model_one_way.predict_proba(X_test_one)[:, 1]
y_one_test_pred = model_one_way.predict(X_test_one)

y_two_test_probas_pred = model_two_way.predict_proba(X_test_two)[:, 1]
y_two_test_pred = model_two_way.predict(X_test_two)

# %%
precision, recall, thresholds = precision_recall_curve(
    y_test_one, y_one_test_probas_pred
)
thresholds = [0] + thresholds.tolist()
sns.scatterplot(x=thresholds, y=precision, label="precision", markers="+", s=5)
ax = sns.scatterplot(x=thresholds, y=recall, label="recall", markers="+", s=5)
ax.set(xlabel="Threshold", ylabel="Precision & Recall")
plt.savefig("test_2.png")

# %%
PrecisionRecallDisplay.from_predictions(y_test_one, y_one_test_probas_pred)

# %%
print(classification_report(y_test_one, y_one_test_probas_pred > 0.69))

# %%
precision, recall, thresholds = precision_recall_curve(
    y_test_two, y_two_test_probas_pred
)
thresholds = [0] + thresholds.tolist()
sns.scatterplot(x=thresholds, y=precision, label="precision", markers="+", s=5)
sns.scatterplot(x=thresholds, y=recall, label="recall", markers="+", s=5)

# %%
PrecisionRecallDisplay.from_predictions(y_test_two, y_two_test_probas_pred)

# %%
print(classification_report(y_test_two, y_two_test_probas_pred > 0.81))

# %%
get_importance(model_one_way, X_train_one)

# %%
get_importance(model_two_way, X_train_two)

# %%
model_one_way.save_model("model_one_way")

# %%
model_two_way.save_model("model_two_way")
