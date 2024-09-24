import logging
import joblib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import optuna  # Added for Bayesian optimization

from typing import Any, Callable, Dict, List, Optional, Tuple

from sklearn.base import BaseEstimator
from sklearn.ensemble import (
    RandomForestRegressor,
    GradientBoostingRegressor,
    AdaBoostRegressor,
    StackingRegressor,  # Added for stacking
    BaggingRegressor,
    VotingRegressor
)
from sklearn.linear_model import (
    LinearRegression,
    Ridge,
    Lasso,
    ElasticNet,
)
from sklearn.metrics import (
    mean_absolute_error,
    mean_absolute_percentage_error,
    mean_squared_error,
    median_absolute_error,
    r2_score,
    explained_variance_score,
)
from sklearn.model_selection import (
    GridSearchCV,
    RandomizedSearchCV,
    KFold,
    cross_val_score,
    learning_curve,
    train_test_split,
)
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVR
from sklearn.tree import DecisionTreeRegressor
from xgboost import XGBRegressor
from lightgbm import LGBMRegressor
from catboost import CatBoostRegressor


class RegressionSolver:
    """
    A comprehensive class for solving regression problems using various machine learning models.
    Includes methods for data preprocessing, model training, evaluation, hyperparameter tuning,
    cross-validation, model merging, and model persistence.
    """

    def __init__(
        self, models: Optional[Dict[str, BaseEstimator]] = None, random_state: int = 42
    ) -> None:
        """
        Initializes the RegressionSolver with a dictionary of models to use.

        Args:
            models (Optional[Dict[str, BaseEstimator]]): A dictionary mapping model names to model instances.
            random_state (int): Random seed for reproducibility.
        """
        self.logger = self._setup_logger()
        self.random_state = random_state
        self.models = models or self._default_models()
        self.tuned_models: Dict[str, BaseEstimator] = {}

    def _default_models(self) -> Dict[str, BaseEstimator]:
        """
        Provides default models for regression tasks.

        Returns:
            Dict[str, BaseEstimator]: A dictionary of default models.
        """
        return {
            "Linear Regression": LinearRegression(),
            "Ridge Regression": Ridge(random_state=self.random_state),
            "Lasso Regression": Lasso(random_state=self.random_state),
            "ElasticNet Regression": ElasticNet(random_state=self.random_state),
            "Decision Tree": DecisionTreeRegressor(random_state=self.random_state),
            "Random Forest": RandomForestRegressor(random_state=self.random_state),
            "Gradient Boosting": GradientBoostingRegressor(random_state=self.random_state),
            "AdaBoost": AdaBoostRegressor(random_state=self.random_state),
            "Support Vector Regressor": SVR(),
            "XGBoost": XGBRegressor(
                random_state=self.random_state,
                objective="reg:squarederror",
                use_label_encoder=False,  # Added to suppress warnings
                eval_metric='rmse'  # Added for clarity
            ),
            "LightGBM": LGBMRegressor(random_state=self.random_state),
            "CatBoost": CatBoostRegressor(
                verbose=0, random_state=self.random_state
            ),
        }

    def _default_param_grids(self) -> Dict[str, Dict[str, List[Any]]]:
        """
        Provides default hyperparameter grids for common regression models.

        Returns:
            Dict[str, Dict[str, List[Any]]]: A dictionary of hyperparameter grids.
        """
        return {
            "Ridge Regression": {
                "alpha": [0.1, 1.0, 10.0, 100.0],
                "solver": ["auto", "svd", "cholesky", "lsqr", "sparse_cg", "sag", "saga"],
            },
            "Lasso Regression": {
                "alpha": [0.001, 0.01, 0.1, 1.0],
                "selection": ["cyclic", "random"],
            },
            "ElasticNet Regression": {
                "alpha": [0.001, 0.01, 0.1, 1.0],
                "l1_ratio": [0.1, 0.5, 0.7, 0.9],
            },
            "Decision Tree": {
                "max_depth": [None, 5, 10, 20, 30],
                "min_samples_split": [2, 5, 10],
                "min_samples_leaf": [1, 2, 4],
                "criterion": ["squared_error", "friedman_mse", "absolute_error", "poisson"],
            },
            "Random Forest": {
                "n_estimators": [50, 100, 200],
                "max_depth": [None, 5, 10, 20, 30],
                "min_samples_split": [2, 5, 10],
                "min_samples_leaf": [1, 2, 4],
                "bootstrap": [True, False],
            },
            "Gradient Boosting": {
                "n_estimators": [50, 100, 200],
                "learning_rate": [0.01, 0.05, 0.1, 0.2],
                "max_depth": [3, 5, 7],
                "subsample": [0.6, 0.8, 1.0],
            },
            "AdaBoost": {
                "n_estimators": [50, 100, 200],
                "learning_rate": [0.01, 0.05, 0.1, 0.2, 1.0],
                "loss": ["linear", "square", "exponential"],
            },
            "Support Vector Regressor": {
                "C": [0.1, 1, 10],
                "kernel": ["linear", "rbf", "poly", "sigmoid"],
                "gamma": ["scale", "auto"],
                "epsilon": [0.1, 0.2, 0.5],
            },
            "XGBoost": {
                "n_estimators": [50, 100, 200],
                "learning_rate": [0.01, 0.05, 0.1],
                "max_depth": [3, 5, 7],
                "subsample": [0.6, 0.8, 1.0],
                "colsample_bytree": [0.6, 0.8, 1.0],
            },
            "LightGBM": {
                "n_estimators": [50, 100, 200],
                "learning_rate": [0.01, 0.05, 0.1],
                "num_leaves": [31, 50, 100],
                "max_depth": [-1, 5, 10],
            },
            "CatBoost": {
                "iterations": [100, 200, 500],
                "learning_rate": [0.01, 0.05, 0.1],
                "depth": [3, 5, 7],
            },
        }

    @staticmethod
    def _setup_logger() -> logging.Logger:
        """
        Sets up a logger for tracking model training and evaluation.

        Returns:
            logging.Logger: Configured logger instance.
        """
        logger = logging.getLogger("RegressionSolver")
        if not logger.handlers:
            logger.setLevel(logging.INFO)
            ch = logging.StreamHandler()
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            ch.setFormatter(formatter)
            logger.addHandler(ch)
        return logger

    def split_data(
        self,
        X: pd.DataFrame,
        y: pd.Series,
        test_size: float = 0.2,
        random_state: Optional[int] = None,
    ) -> Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
        """
        Splits the data into training and testing sets.

        Args:
            X (pd.DataFrame): Feature matrix.
            y (pd.Series): Target variable.
            test_size (float): Proportion of the dataset to include in the test split.
            random_state (Optional[int]): Random seed.

        Returns:
            Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]: Training and testing sets for features and target.
        """
        random_state = random_state or self.random_state
        self.logger.info("Splitting data into training and testing sets...")
        return train_test_split(  # type: ignore
            X, y, test_size=test_size, random_state=random_state
        )

    def train_model(
        self,
        model_name: str,
        X_train: pd.DataFrame,
        y_train: pd.Series,
        use_pipeline: bool = False,
    ) -> BaseEstimator:
        """
        Trains a given regression model.

        Args:
            model_name (str): The name of the model to train.
            X_train (pd.DataFrame): Training features.
            y_train (pd.Series): Training target.
            use_pipeline (bool): Whether to use a pipeline with scaling.

        Returns:
            BaseEstimator: The trained model.
        """
        if model_name in self.tuned_models:
            model = self.tuned_models[model_name]
            self.logger.info(f"Using tuned model: {model_name}")
        else:
            model = self.models[model_name]
            self.logger.info(f"Training model: {model_name}")

        if use_pipeline:
            self.logger.info("Using pipeline with StandardScaler.")
            pipeline = Pipeline(
                [("scaler", StandardScaler()), ("model", model)]
            )
            pipeline.fit(X_train, y_train)
            return pipeline
        else:
            model.fit(X_train, y_train)
            return model

    def evaluate_model(
        self,
        model: BaseEstimator,
        X_test: pd.DataFrame,
        y_test: pd.Series,
    ) -> Dict[str, Any]:
        """
        Evaluates the regression model on test data.

        Args:
            model (BaseEstimator): The trained model.
            X_test (pd.DataFrame): Testing features.
            y_test (pd.Series): Testing target.

        Returns:
            Dict[str, Any]: A dictionary containing evaluation metrics.
        """
        self.logger.info("Evaluating model performance...")
        predictions = model.predict(X_test)
        metrics = self._get_evaluation_metrics(y_test, predictions)
        return metrics

    def _get_evaluation_metrics(
        self,
        y_true: pd.Series,
        y_pred: np.ndarray,
    ) -> Dict[str, Any]:
        """
        Computes evaluation metrics for the regression model.

        Args:
            y_true (pd.Series): True values.
            y_pred (np.ndarray): Predicted values.

        Returns:
            Dict[str, Any]: Dictionary of evaluation metrics.
        """
        self.logger.info("Computing evaluation metrics...")
        mse = mean_squared_error(y_true, y_pred)
        mae = mean_absolute_error(y_true, y_pred)
        rmse = np.sqrt(mse)
        r2 = r2_score(y_true, y_pred)
        explained_var = explained_variance_score(y_true, y_pred)
        mape = mean_absolute_percentage_error(y_true, y_pred)
        median_ae = median_absolute_error(y_true, y_pred)

        metrics = {
            "mean_squared_error": mse,
            "root_mean_squared_error": rmse,
            "mean_absolute_error": mae,
            "median_absolute_error": median_ae,
            "mean_absolute_percentage_error": mape,
            "r2_score": r2,
            "explained_variance_score": explained_var,
        }
        return metrics

    def hyperparameter_tuning(
        self,
        model_name: str,
        X_train: pd.DataFrame,
        y_train: pd.Series,
        param_grid: Optional[Dict[str, List[Any]]] = None,
        cv: int = 5,
        search_type: str = "grid",
        n_iter: int = 50,
        scoring: str = "neg_mean_squared_error",
    ) -> None:
        """
        Performs hyperparameter tuning using GridSearchCV, RandomizedSearchCV, or Bayesian Optimization for one or all models and stores the best models.

        Args:
            model_name (str): The name of the model to tune. If 'all', tunes all models in self.models.
            X_train (pd.DataFrame): Training features.
            y_train (pd.Series): Training target.
            param_grid (Optional[Dict[str, List[Any]]]): Parameter grid for hyperparameter tuning. If None, uses default.
            cv (int): Number of cross-validation folds.
            search_type (str): Type of search ('grid', 'random', or 'bayesian').
            n_iter (int): Number of iterations for RandomizedSearchCV or Bayesian Optimization.
            scoring (str): Scoring metric for evaluation.

        Returns:
            None: The best models are stored in self.tuned_models.
        """
        if model_name == "all":
            self.logger.info("Performing hyperparameter tuning for all models...")
            for name in self.models:
                self._tune_single_model(
                    name, X_train, y_train, param_grid, cv, search_type, n_iter, scoring
                )
        else:
            self._tune_single_model(
                model_name,
                X_train,
                y_train,
                param_grid,
                cv,
                search_type,
                n_iter,
                scoring,
            )

    def _tune_single_model(
        self,
        model_name: str,
        X_train: pd.DataFrame,
        y_train: pd.Series,
        param_grid: Optional[Dict[str, List[Any]]],
        cv: int,
        search_type: str,
        n_iter: int,
        scoring: str,
    ) -> None:
        """
        Helper method to perform hyperparameter tuning for a single model.

        Args:
            model_name (str): The name of the model to tune.
            X_train (pd.DataFrame): Training features.
            y_train (pd.Series): Training target.
            param_grid (Optional[Dict[str, List[Any]]]): Parameter grid for hyperparameter tuning. If None, uses default.
            cv (int): Number of cross-validation folds.
            search_type (str): Type of search ('grid', 'random', or 'bayesian').
            n_iter (int): Number of iterations for RandomizedSearchCV or Bayesian Optimization.
            scoring (str): Scoring metric for evaluation.

        Returns:
            None: The best model is stored in self.tuned_models.
        """
        model = self.models[model_name]
        self.logger.info(f"Performing hyperparameter tuning for {model_name}...")

        if param_grid is None:
            param_grid = self._default_param_grids().get(model_name, {})
            if not param_grid:
                self.logger.warning(
                    f"No parameter grid available for {model_name}. Skipping tuning."
                )
                return

        if search_type == "grid":
            search = GridSearchCV(
                model,
                param_grid,
                cv=cv,
                scoring=scoring,
                n_jobs=-1,
                verbose=1,
            )
            search.fit(X_train, y_train)
            self.logger.info(
                f"Best parameters found for {model_name}: {search.best_params_}"
            )
            # Store the tuned model for future use
            self.tuned_models[model_name] = search.best_estimator_
        elif search_type == "random":
            search = RandomizedSearchCV(
                model,
                param_grid,
                n_iter=n_iter,
                cv=cv,
                scoring=scoring,
                n_jobs=-1,
                verbose=1,
                random_state=self.random_state,
            )
            search.fit(X_train, y_train)
            self.logger.info(
                f"Best parameters found for {model_name}: {search.best_params_}"
            )
            # Store the tuned model for future use
            self.tuned_models[model_name] = search.best_estimator_
        elif search_type == "bayesian":  # Added Bayesian optimization
            self.logger.info(f"Using Bayesian Optimization for {model_name}...")
            study = optuna.create_study(direction="maximize")
            func = self._create_objective(model, param_grid, X_train, y_train, cv, scoring)
            study.optimize(func, n_trials=n_iter)
            best_params = study.best_params
            self.logger.info(f"Best parameters found for {model_name}: {best_params}")
            model.set_params(**best_params)
            model.fit(X_train, y_train)
            self.tuned_models[model_name] = model
        else:
            raise ValueError("search_type must be either 'grid', 'random', or 'bayesian'.")

    def _create_objective(
        self,
        model: BaseEstimator,
        param_grid: Dict[str, List[Any]],
        X: pd.DataFrame,
        y: pd.Series,
        cv: int,
        scoring: str,
    ) -> Callable[[optuna.trial.Trial], float]:
        """
        Creates an objective function for Optuna to optimize model hyperparameters.

        Args:
            model (BaseEstimator): The machine learning model to be optimized.
            param_grid (Dict[str, List[Any]]): The grid of hyperparameters to search over.
            X (pd.DataFrame): Training data for features.
            y (pd.Series): Target labels for training data.
            cv (int): The number of cross-validation folds.
            scoring (str): The scoring metric to evaluate model performance.

        Returns:
            Callable[[optuna.trial.Trial], float]: The objective function to be minimized or maximized by Optuna.
        """

        def objective(trial: optuna.trial.Trial) -> Any:
            """
            The actual objective function used by Optuna to evaluate a set of hyperparameters.

            Args:
                trial (optuna.trial.Trial): A single trial instance that suggests hyperparameters.

            Returns:
                float: The mean cross-validated score for the suggested hyperparameter set.
            """
            params = {}
            for param, values in param_grid.items():
                if isinstance(values, list):
                    # Categorical or discrete parameters
                    params[param] = trial.suggest_categorical(param, values)
                elif isinstance(values, np.ndarray):
                    # Continuous parameters
                    params[param] = trial.suggest_float(param, float(values.min()), float(values.max()))
                else:
                    # Handle float or integer ranges
                    params[param] = trial.suggest_float(param, float(min(values)), float(max(values)))

            model.set_params(**params)

            # Define cross-validation strategy
            if isinstance(cv, int):
                cv_strategy = KFold(n_splits=cv, shuffle=True, random_state=self.random_state)
            else:
                cv_strategy = cv

            # Perform cross-validation
            score = cross_val_score(
                model, X, y, cv=cv_strategy, scoring=scoring, n_jobs=-1
            ).mean()

            return score

        return objective

    def auto_select_best_model(
        self, X_train: pd.DataFrame, y_train: pd.Series, cv: int = 5, scoring: str = "neg_mean_squared_error"
    ) -> Tuple[str, float]:
        """
        Automatically selects the best model based on cross-validated score.
        It checks if a hyperparameter-tuned version of the model is available and uses it if present.

        Args:
            X_train (pd.DataFrame): Training features.
            y_train (pd.Series): Training target.
            cv (int): Number of cross-validation folds (default: 5).
            scoring (str): Scoring metric for evaluation.

        Returns:
            Tuple[str, float]: The name of the best performing model and its score based on cross-validation.
        """
        self.logger.info(
            "Automatically selecting the best model based on cross-validated score..."
        )
        best_score = float('-inf')  # Initialize to negative infinity
        best_model_name = ""

        for model_name in self.models:
            self.logger.info(f"Evaluating model: {model_name}")

            # Use the tuned model if available
            model = self.tuned_models.get(model_name, self.models[model_name])

            # Perform cross-validation
            cv_strategy = KFold(n_splits=cv, shuffle=True, random_state=self.random_state)
            scores = cross_val_score(
                model, X_train, y_train, cv=cv_strategy, scoring=scoring, n_jobs=-1
            )
            mean_score = scores.mean()
            std_score = scores.std()

            self.logger.info(
                f"{model_name} - Mean Score: {mean_score:.4f}, Std: {std_score:.4f}"
            )

            # For scoring metrics where higher is better (e.g., neg_mean_squared_error)
            if mean_score > best_score:
                best_score = mean_score
                best_model_name = model_name

        self.logger.info(
            f"Best model selected: {best_model_name} with cross-validated score: {best_score:.4f}"
        )
        return best_model_name, best_score

    def compare_models(
        self, X_train: pd.DataFrame, y_train: pd.Series, cv: int = 5, scoring: str = "neg_mean_squared_error"
    ) -> pd.DataFrame:
        """
        Compares multiple models based on cross-validation scores.

        Args:
            X_train (pd.DataFrame): Training features.
            y_train (pd.Series): Training target.
            cv (int): Number of cross-validation folds.
            scoring (str): Scoring metric for evaluation.

        Returns:
            pd.DataFrame: DataFrame containing models and their scores.
        """
        self.logger.info("Comparing models...")
        results = []
        cv_strategy = KFold(n_splits=cv, shuffle=True, random_state=self.random_state)

        for model_name in self.models:
            self.logger.info(f"Evaluating model: {model_name}")
            model = self.tuned_models.get(model_name, self.models[model_name])
            scores = cross_val_score(
                model, X_train, y_train, cv=cv_strategy, scoring=scoring, n_jobs=-1
            )
            results.append(
                {
                    "Model": model_name,
                    "Mean Score": scores.mean(),
                    "Std Score": scores.std(),
                }
            )
        results_df = pd.DataFrame(results)
        results_df.sort_values(by="Mean Score", ascending=False, inplace=True)
        self.logger.info("Model comparison results:\n" + results_df.to_string(index=False))
        return results_df

    def plot_residuals(
        self, model: BaseEstimator, X_test: pd.DataFrame, y_test: pd.Series
    ) -> None:
        """
        Plots residuals of the regression model.

        Args:
            model (BaseEstimator): The trained model.
            X_test (pd.DataFrame): Testing features.
            y_test (pd.Series): Testing target.
        """
        predictions = model.predict(X_test)
        residuals = y_test - predictions

        plt.figure(figsize=(10, 6))
        sns.residplot(x=predictions, y=residuals, lowess=True, color="g")
        plt.title("Residual Plot")
        plt.xlabel("Predicted Values")
        plt.ylabel("Residuals")
        plt.show()

    def plot_residual_distribution(
        self, model: BaseEstimator, X_test: pd.DataFrame, y_test: pd.Series
    ) -> None:
        """
        Plots the distribution of residuals (prediction errors).

        Args:
            model (BaseEstimator): The trained model.
            X_test (pd.DataFrame): Testing features.
            y_test (pd.Series): Testing target.
        """
        predictions = model.predict(X_test)
        residuals = y_test - predictions
        plt.figure(figsize=(10, 6))
        sns.histplot(residuals, kde=True, color="blue")
        plt.title("Residual Distribution")
        plt.xlabel("Residuals")
        plt.ylabel("Frequency")
        plt.show()

    def plot_feature_importance(
        self, model: BaseEstimator, feature_names: List[str]
    ) -> None:
        """
        Plots feature importance for models that support it.

        Args:
            model (BaseEstimator): The trained model.
            feature_names (List[str]): List of feature names.
        """
        if hasattr(model, "feature_importances_"):
            importances = model.feature_importances_
            indices = np.argsort(importances)[::-1]
            plt.figure(figsize=(12, 6))
            plt.title("Feature Importance")
            plt.bar(
                range(len(importances)),
                importances[indices],
                align="center",
                color="skyblue",
            )
            plt.xticks(
                range(len(importances)),
                [feature_names[i] for i in indices],
                rotation=90,
            )
            plt.tight_layout()
            plt.show()
        elif hasattr(model, "coef_"):
            if isinstance(model.coef_, np.ndarray):
                importances = np.abs(model.coef_)
                if importances.ndim > 1:
                    importances = importances.ravel()
                indices = np.argsort(importances)[::-1]
                plt.figure(figsize=(12, 6))
                plt.title("Feature Importance")
                plt.bar(
                    range(len(importances)),
                    importances[indices],
                    align="center",
                    color="skyblue",
                )
                plt.xticks(
                    range(len(importances)),
                    [feature_names[i] for i in indices],
                    rotation=90,
                )
                plt.tight_layout()
                plt.show()
            else:
                self.logger.warning(f"Model {model.__class__.__name__} has non-array coefficients.")
        else:
            self.logger.warning(f"Model {model.__class__.__name__} does not support feature importances.")

    def plot_learning_curve(
        self,
        model: BaseEstimator,
        X_train: pd.DataFrame,
        y_train: pd.Series,
        cv: int = 5,
        scoring: str = "neg_mean_squared_error",
    ) -> None:
        """
        Plots the learning curve of the model.

        Args:
            model (BaseEstimator): The model to plot learning curve for.
            X_train (pd.DataFrame): Feature matrix.
            y_train (pd.Series): Target variable.
            cv (int): Number of cross-validation folds.
            scoring (str): Scoring metric.

        """
        self.logger.info("Plotting learning curve...")
        train_sizes, train_scores, test_scores = learning_curve(
            model,
            X_train,
            y_train,
            cv=cv,
            scoring=scoring,
            n_jobs=-1,
            train_sizes=np.linspace(0.1, 1.0, 5),
            random_state=self.random_state,
        )
        # For negative scoring metrics, convert to positive
        train_scores_mean = -np.mean(train_scores, axis=1)
        test_scores_mean = -np.mean(test_scores, axis=1)

        plt.figure(figsize=(10, 6))
        plt.plot(
            train_sizes,
            train_scores_mean,
            "o-",
            color="r",
            label="Training error",
        )
        plt.plot(
            train_sizes,
            test_scores_mean,
            "o-",
            color="g",
            label="Cross-validation error",
        )
        plt.title("Learning Curve")
        plt.xlabel("Training Examples")
        plt.ylabel("Error")
        plt.legend(loc="best")
        plt.grid()
        plt.show()

    def save_model(self, model: BaseEstimator, filename: str) -> None:
        """
        Saves the trained model to disk.

        Args:
            model (BaseEstimator): The trained model.
            filename (str): The path and filename to save the model.
        """
        joblib.dump(model, filename)
        self.logger.info(f"Model saved to {filename}")

    def load_model(self, filename: str) -> BaseEstimator:
        """
        Loads a trained model from disk.

        Args:
            filename (str): The path and filename to load the model from.

        Returns:
            BaseEstimator: The loaded model.
        """
        model = joblib.load(filename)
        self.logger.info(f"Model loaded from {filename}")
        return model

    def model_merging(
        self,
        base_models: List[str],
        X_train: pd.DataFrame,
        y_train: pd.Series,
        method: str = "stacking",  # New argument to select the ensemble method
        final_estimator: Optional[BaseEstimator] = None,
        passthrough: bool = False,
        cv: int = 5,
        n_estimators: int = 10  # For bagging and boosting
    ) -> BaseEstimator:
        """
        Creates an ensemble model by merging multiple base models using different ensemble techniques.
        Supports stacking, bagging, boosting, and voting.

        Args:
            base_models (List[str]): List of model names to be used as base models.
            X_train (pd.DataFrame): Training features.
            y_train (pd.Series): Training target.
            method (str): The ensemble method to use ('stacking', 'bagging', 'boosting', or 'voting').
            final_estimator (Optional[BaseEstimator]): The final estimator to combine base models for stacking. Defaults to Ridge.
            passthrough (bool): If True, pass the original features to the final estimator (only for stacking).
            cv (int): Number of cross-validation folds for stacking.
            n_estimators (int): Number of estimators for bagging or boosting.

        Returns:
            BaseEstimator: The ensemble model.
        """
        self.logger.info(f"Creating {method.capitalize()} Regressor for model merging...")

        # Collect base models
        estimators = []
        for model_name in base_models:
            if model_name in self.tuned_models:
                model = self.tuned_models[model_name]
                self.logger.info(f"Using tuned model: {model_name} for {method}.")
            else:
                model = self.models.get(model_name)
                if model is None:
                    self.logger.warning(f"Model {model_name} not found. Skipping.")
                    continue
                self.logger.info(f"Using default model: {model_name} for {method}.")
            estimators.append((model_name, model))

        if not estimators:
            self.logger.error(f"No valid base models provided for {method}.")
            raise ValueError(f"No valid base models provided for {method}.")

        # Define the final estimator for stacking
        if final_estimator is None and method == "stacking":
            final_estimator = Ridge(random_state=self.random_state)

        # Ensemble Methods
        if method == "stacking":
            # Stacking Regressor
            ensemble_model = StackingRegressor(
                estimators=estimators,
                final_estimator=final_estimator,
                passthrough=passthrough,
                cv=cv,
                n_jobs=-1,
            )

        elif method == "bagging":
            # Bagging Regressor
            base_estimator = estimators[0][1] if len(estimators) == 1 else RandomForestRegressor(random_state=self.random_state)
            ensemble_model = BaggingRegressor(
                base_estimator=base_estimator,
                n_estimators=n_estimators,
                random_state=self.random_state,
                n_jobs=-1,
            )

        elif method == "boosting":
            # Boosting Regressor (Gradient Boosting or AdaBoost)
            if "Gradient Boosting" in base_models:
                ensemble_model = GradientBoostingRegressor(
                    n_estimators=n_estimators,
                    random_state=self.random_state,
                )
            else:
                # Default to AdaBoost if Gradient Boosting is not in base models
                ensemble_model = AdaBoostRegressor(
                    base_estimator=estimators[0][1] if len(estimators) == 1 else DecisionTreeRegressor(random_state=self.random_state),
                    n_estimators=n_estimators,
                    random_state=self.random_state,
                )

        elif method == "voting":
            # Voting Regressor
            ensemble_model = VotingRegressor(estimators=estimators, n_jobs=-1)

        else:
            self.logger.error(f"Unknown ensemble method: {method}")
            raise ValueError(f"Unknown ensemble method: {method}")

        # Fit the ensemble model
        self.logger.info(f"Training {method.capitalize()} Regressor...")
        ensemble_model.fit(X_train, y_train)

        # Store the ensemble model in tuned_models for future use
        self.tuned_models[f"{method.capitalize()} Regressor"] = ensemble_model

        return ensemble_model
