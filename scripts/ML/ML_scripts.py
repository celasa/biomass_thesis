import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


from sklearn.ensemble import RandomForestClassifier
from sklearn.inspection import permutation_importance
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import (
    StratifiedKFold,
    RandomizedSearchCV,
    GridSearchCV,
    learning_curve,
    train_test_split,
    cross_validate,
)
from sklearn.metrics import (
    confusion_matrix,
    ConfusionMatrixDisplay,
    classification_report,
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    matthews_corrcoef,
    roc_curve,
    precision_recall_curve,
    auc,
    make_scorer,
    roc_auc_score,
)

from xgboost import XGBClassifier


def evaluate_predictions(y_true, y_pred, name):
    print(f"\n=== {name} ===")
    print("Accuracy :", accuracy_score(y_true, y_pred))
    print("Precision:", precision_score(y_true, y_pred, average="macro", zero_division=0))
    print("Recall   :", recall_score(y_true, y_pred, average="macro", zero_division=0))
    print("F1       :", f1_score(y_true, y_pred, average="macro", zero_division=0))
    print("MCC      :", matthews_corrcoef(y_true, y_pred))

    print("\nClassification report:")
    print(classification_report(y_true, y_pred, zero_division=0))


def make_prediction(X, binary_clf, carbon_clf, nitrogen_clf, le_type, le_carbon, le_nitrogen):
    binary_pred = binary_clf.predict(X)

    carbon_label   = le_type.transform(["carbon"])[0]
    nitrogen_label = le_type.transform(["nitrogen"])[0]

    carbon_idx   = np.where(binary_pred == carbon_label)[0]
    nitrogen_idx = np.where(binary_pred == nitrogen_label)[0]

    source_pred = np.empty(len(X), dtype=object)

    if len(carbon_idx) > 0:
        source_pred[carbon_idx] = le_carbon.inverse_transform(
            carbon_clf.predict(X.iloc[carbon_idx])
        )
    if len(nitrogen_idx) > 0:
        source_pred[nitrogen_idx] = le_nitrogen.inverse_transform(
            nitrogen_clf.predict(X.iloc[nitrogen_idx])
        )

    return binary_pred, source_pred

def make_prediction_proba(X, binary_clf, carbon_clf, nitrogen_clf, le_type, le_source, le_carbon, le_nitrogen):
    binary_pred = binary_clf.predict(X).ravel()

    carbon_label = le_type.transform(["carbon"])[0]
    nitrogen_label = le_type.transform(["nitrogen"])[0]

    carbon_idx = np.where(binary_pred == carbon_label)[0]
    nitrogen_idx = np.where(binary_pred == nitrogen_label)[0]
    source_proba = np.zeros((len(X), len(le_source.classes_)))

    if len(carbon_idx) > 0:
        carbon_proba = carbon_clf.predict_proba(X.iloc[carbon_idx])
        carbon_global_idx = le_source.transform(le_carbon.classes_)

        source_proba[np.ix_(carbon_idx, carbon_global_idx)] = carbon_proba

    if len(nitrogen_idx) > 0:
        nitrogen_proba = nitrogen_clf.predict_proba(X.iloc[nitrogen_idx])
        nitrogen_global_idx = le_source.transform(le_nitrogen.classes_)

        source_proba[np.ix_(nitrogen_idx, nitrogen_global_idx)] = nitrogen_proba

    return source_proba



def tune_model(model, param_grid, X, y, model_name, stage_name, refit_score="f1_macro"):
    search = GridSearchCV(
        estimator=model,
        param_grid=param_grid,
        scoring=scoring,
        refit=refit_score,  
        cv=cv,
        n_jobs=3,
        return_train_score=False
    )

    search.fit(X, y)

    i = search.best_index_

    result = {
        "stage": stage_name,
        "model": model_name,
        "best_params": search.best_params_,
        "accuracy": search.cv_results_["mean_test_accuracy"][i],
        "precision_macro": search.cv_results_["mean_test_precision_macro"][i],
        "recall_macro": search.cv_results_["mean_test_recall_macro"][i],
        "f1_macro": search.cv_results_["mean_test_f1_macro"][i],
        "mcc": search.cv_results_["mean_test_mcc"][i],
        "best_estimator": search.best_estimator_
    }

    return result


def plot_binary_eval_curves(y_true, y_score, figsize=(18, 5), model=None):
    """
    Plot three binary-classification evaluation curves side by side:
    1) Precision-Recall curve
    2) Precision and Recall vs Decision Threshold
    3) ROC curve

    Parameters
    ----------
    y_true : array-like
        True binary labels (0/1 or False/True).
    y_score : array-like
        Predicted scores or probabilities for the positive class.
    figsize : tuple, optional
        Figure size for the subplot layout.
    """

    precision, recall, pr_thresholds = precision_recall_curve(y_true, y_score)
    fpr, tpr, roc_thresholds = roc_curve(y_true, y_score)
    roc_auc = auc(fpr, tpr)

    fig, axes = plt.subplots(1, 3, figsize=figsize)

    axes[0].plot(recall, precision, "b-", alpha=0.5)
    axes[0].set_xlabel("Recall", fontsize=12)
    axes[0].set_ylabel("Precision", fontsize=12)
    # axes[0].set_title("Precision–Recall Curve", fontsize=10)

    axes[1].plot(pr_thresholds, precision[:-1], "b--", label="Precision")
    axes[1].plot(pr_thresholds, recall[:-1], "-", label="Recall")
    axes[1].set_xlabel("Decision Threshold")
    axes[1].set_ylabel("Score")
    axes[1].set_title("Score vs Decision Threshold", fontsize=10)
    axes[1].legend()

    axes[2].plot(fpr, tpr, "-", color='orange', label=f"AUC = {roc_auc:.3f}")
    axes[2].plot([0, 1], [0, 1], "k--")
    axes[2].set_xlabel("False Positive Rate")
    axes[2].set_ylabel("True Positive Rate")
    axes[2].set_title("ROC Curve", fontsize=10)
    axes[2].legend()

    plt.suptitle(model, fontsize=15)

    plt.tight_layout()
    plt.show()

def evaluate_predictions(y_true, y_pred, name):
    print(f"\n=== {name} ===")
    print("Accuracy :", accuracy_score(y_true, y_pred))
    print("Precision:", precision_score(y_true, y_pred, average="macro", zero_division=0))
    print("Recall   :", recall_score(y_true, y_pred, average="macro", zero_division=0))
    print("F1       :", f1_score(y_true, y_pred, average="macro", zero_division=0))
    print("MCC      :", matthews_corrcoef(y_true, y_pred))

    print("\nClassification report:")
    print(classification_report(y_true, y_pred, zero_division=0))


def evaluate_stage2_predictions(y_true, y_pred, name, label_encoder):
    print(f"\n=== {name} ===")
    print("Accuracy :", accuracy_score(y_true, y_pred))
    print(
        "Precision:",
        precision_score(
            y_true,
            y_pred,
            average="macro",
            zero_division=0
        )
    )

    print(
        "Recall   :",
        recall_score(
            y_true,
            y_pred,
            average="macro",
            zero_division=0
        )
    )

    print(
        "F1       :",
        f1_score(
            y_true,
            y_pred,
            average="macro",
            zero_division=0
        )
    )

    print(
        "MCC      :",
        matthews_corrcoef(y_true, y_pred)
    )

    print("\nClassification report:")

    print(
        classification_report(
            y_true,
            y_pred,
            target_names=label_encoder.classes_,
            zero_division=0
        )
    )

import matplotlib.ticker as mticker

def get_permutation_importance(model, X_val, y_val, feature_names, model_name, stage_name,
                                n_repeats=30, random_state=42, scoring="f1_macro"):
    result = permutation_importance(
        model, X_val, y_val,
        n_repeats=n_repeats,
        random_state=random_state,
        n_jobs=-1,
        scoring=scoring
    )
    return pd.DataFrame({
        "feature":    feature_names,
        "importance": result.importances_mean,
        "std":        result.importances_std,
        "scores":     list(result.importances),
        "model":      model_name,
        "stage":      stage_name
    }).sort_values("importance", ascending=False)


import matplotlib.ticker as mticker

def get_permutation_importance(model, X_val, y_val, feature_names, model_name, stage_name,
                                n_repeats=30, random_state=42, scoring="f1_macro"):
    result = permutation_importance(
        model, X_val, y_val,
        n_repeats=n_repeats,
        random_state=random_state,
        n_jobs=-1,
        scoring=scoring
    )
    return pd.DataFrame({
        "feature":    feature_names,
        "importance": result.importances_mean,
        "std":        result.importances_std,
        "scores":     list(result.importances),
        "model":      model_name,
        "stage":      stage_name
    }).sort_values("importance", ascending=False)


def format_feature_label(name):
    return name.replace("_biomass_to_biomass", "")

def plot_permutation_importance(fi_df, title=None, palette="crest",
                                style="bar", scoring="f1_macro"):
    plot_df = (fi_df
               .sort_values("importance", ascending=True)
               .reset_index(drop=True))

    plot_df["feature"] = plot_df["feature"].apply(format_feature_label)

    n = len(plot_df)
    # fig, ax = plt.subplots(figsize=(12, 6))

    if style == "box":
        box_data = list(plot_df["scores"])
        bp = ax.boxplot(
            box_data,
            vert=False,
            patch_artist=True,
            labels=plot_df["feature"],
            medianprops=dict(linewidth=1.5), 
            whiskerprops=dict(linewidth=0.8),
            capprops=dict(linewidth=0.8),
            flierprops=dict(marker="o", markersize=5, alpha=0.8),
            widths=0.8
        )
        cmap = sns.color_palette(palette, as_cmap=True)
        for i, patch in enumerate(bp["boxes"]):
            patch.set_facecolor(cmap(i / (n - 1)))
            patch.set_alpha(0.8)
            patch.set_linewidth(0.6)

    else:  # bar (default)
        cmap = sns.color_palette(palette, as_cmap=True)
        colors = [cmap(i / (n - 1)) for i in range(n)]
        bars = ax.barh(
            plot_df["feature"],
            plot_df["importance"],
            xerr=plot_df["std"],
            color=colors,
            error_kw=dict(ecolor="#555555", elinewidth=0.8, capsize=3, capthick=0.8),
            height=0.65,
        )
        for bar, val in zip(bars, plot_df["importance"]):
            if val < 0:
                bar.set_facecolor("#d9534f")
                bar.set_alpha(0.6)

    ax.axvline(0, color="k", linewidth=0.8, linestyle="--")

    if scoring != "f1_macro":
        ax.set_xlabel(f"Decrease in MCC score", fontsize=13)
    else:
        ax.set_xlabel(f"Decrease in F1 Score (macro)", fontsize=13)
    ax.set_title(title or f"{fi_df['model'].iloc[0]} ({fi_df['stage'].iloc[0]})",
                 fontsize=15, pad=12)


    ax.xaxis.set_major_formatter(mticker.FormatStrFormatter("%.2f"))
    ax.tick_params(axis="y", labelsize=12)
    ax.tick_params(axis="x", labelsize=10)
    # ax.spines[["top", "right"]].set_visible(False)
    # ax.spines[["left", "bottom"]].set_linewidth(0.6)
    ax.grid(axis="x", linewidth=0.8, linestyle=":", color="#aaaaaa")

    plt.tight_layout()
    plt.show()
