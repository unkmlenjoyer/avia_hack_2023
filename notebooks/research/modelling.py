# %%
import numpy as np
import pandas as pd
import seaborn as sns
from catboost import CatBoostClassifier, Pool

# base metric in this competition is roc_auc
from sklearn.metrics import RocCurveDisplay, roc_auc_score, roc_curve

# scikit-learn base he-he
from sklearn.model_selection import GridSearchCV, StratifiedKFold, train_test_split

# %%
sns.set_style("darkgrid")


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
RANDOM_SEED = 42
data = pd.read_csv("../../data/processed/calculated_features.csv", index_col=0)

# %%
TARGET = "SentOption"
ONE_WAY_COLS = [
    "TravellerGrade",
    "SegmentCount",
    # "Amount",
    "class",
    "IsBaggage",
    "isRefundPermitted",
    "isExchangePermitted",
    "isDiscount",
    "InTravelPolicy",
    "forw_hours",
    # "back_hours",
    "forw_hours_diff_min",
    # "back_hours_diff_min",
    # "total_hours",
    "price_diff_min_perc",
    "req_dep_hours_diff",
    # "req_ret_hours_diff",
    "SentOption",
]

TWO_WAY_COLS = [
    "TravellerGrade",
    "SegmentCount",
    # "Amount",
    "class",
    "IsBaggage",
    "isRefundPermitted",
    "isExchangePermitted",
    "isDiscount",
    "InTravelPolicy",
    "forw_hours",
    "back_hours",
    "forw_hours_diff_min",
    "back_hours_diff_min",
    "total_hours",
    "price_diff_min_perc",
    "req_dep_hours_diff",
    "req_ret_hours_diff",
    "SentOption",
]

# %%
one_way_df = data[data.back_hours.isna()][ONE_WAY_COLS]
two_way_df = data[~data.back_hours.isna()][TWO_WAY_COLS]


# %%
X_one, y_one = one_way_df.drop(columns=[TARGET]), one_way_df[TARGET]
X_two, y_two = two_way_df.drop(columns=[TARGET]), two_way_df[TARGET]

# %%
cat_features_one = X_one.select_dtypes(include="object").columns.values
cat_features_two = X_two.select_dtypes(include="object").columns.values

# %%
X_train_one, X_test_one, y_train_one, y_test_one = train_test_split(
    X_one, y_one, shuffle=True, stratify=y_one, test_size=0.2, random_state=RANDOM_SEED
)

X_train_two, X_test_two, y_train_two, y_test_two = train_test_split(
    X_two, y_two, shuffle=True, stratify=y_two, test_size=0.2, random_state=RANDOM_SEED
)

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
model_one_way = CatBoostClassifier(
    depth=4,
    iterations=200,
    learning_rate=0.35,
    loss_function="Logloss",  # MultiLogloss
    eval_metric="PRAUC:type=Classic;use_weights=True",
    custom_metric=["PRAUC:type=Classic;use_weights=True"],
    # Главная фишка катбуста - работа с категориальными признаками
    cat_features=cat_features_one,
    # ignored_features = ignored_features,
    # Регуляризация и ускорение
    colsample_bylevel=0.098,
    subsample=0.8,
    l2_leaf_reg=5,
    min_data_in_leaf=243,
    max_bin=187,
    random_strength=1,
    # Параметры скорения
    task_type="CPU",
    thread_count=-1,
    bootstrap_type="Bernoulli",
    # Важное!
    random_seed=7575,
    auto_class_weights="SqrtBalanced",
    early_stopping_rounds=50,
)

model_two_way = CatBoostClassifier(
    depth=4,
    iterations=200,
    learning_rate=0.35,
    loss_function="Logloss",  # MultiLogloss
    eval_metric="PRAUC:type=Classic;use_weights=True",
    custom_metric=["PRAUC:type=Classic;use_weights=True"],
    # Главная фишка катбуста - работа с категориальными признаками
    cat_features=cat_features_two,
    # ignored_features = ignored_features,
    # Регуляризация и ускорение
    colsample_bylevel=0.098,
    subsample=0.8,
    l2_leaf_reg=5,
    min_data_in_leaf=243,
    max_bin=187,
    random_strength=1,
    # Параметры скорения
    task_type="CPU",
    thread_count=-1,
    bootstrap_type="Bernoulli",
    # Важное!
    random_seed=7575,
    auto_class_weights="SqrtBalanced",
    early_stopping_rounds=50,
)

# param_distribution = {
#     "learning_rate": [0.03, 0.1, 0.3],
#     "l2_leaf_reg": [2, 5, 7],
#     "depth": [3, 4, 6],
# }
# randomized_search_result = model.randomized_search(param_distribution, X_train, y_train)
# model.best_score_

# %%
model_one_way.fit(train_dataset_one, eval_set=eval_dataset_one)
model_two_way.fit(train_dataset_two, eval_set=eval_dataset_two)
import matplotlib.pyplot as plt

# %%
from sklearn.metrics import classification_report, f1_score, precision_recall_curve

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
sns.scatterplot(x=thresholds, y=recall, label="recall", markers="+", s=5)

# %%
print(classification_report(y_test_one, (y_one_test_probas_pred > 0.75).astype(int)))
