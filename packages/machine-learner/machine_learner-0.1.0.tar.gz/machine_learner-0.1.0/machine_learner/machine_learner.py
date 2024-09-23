###################################################################################################
#                                                                                                 #
#                                      STRATEGY AND ALGO FLOW                                     #
#                                                                                                 #
# This code implements a trading strategy based on momentum, moving averages, volatility, and      #
# volume-based signals. The objective is to predict short-term price movements using historical    #
# market data. The system analyzes market trends through various technical indicators such as      #
# Relative Strength Index (RSI), Bollinger Bands, Average True Range (ATR), and exponential        #
# moving averages (EMA).                                                                          #
#                                                                                                 #
# The model uses machine learning techniques to identify patterns that correlate with price        #
# movements. Once these patterns are identified, the system generates buy and sell signals based   #
# on the observed trends.                                                                         #
#                                                                                                 #
# The algorithm follows these steps:                                                              #
# 1. Compute target labels using future periods and ATR-based thresholds (profit & loss).          #
# 2. Prepare features based on historical price data and various technical indicators.             #
# 3. Use rolling windows for training and testing models iteratively to simulate real-time         #
#    prediction behavior.                                                                         #
# 4. Evaluate the model on each rolling window and store results for further analysis.             #
#                                                                                                 #
# ################################################################################################
###################################################################################################

# Import necessary libraries
import numpy as np
import pandas as pd
from ta.momentum import RSIIndicator
from ta.volatility import BollingerBands
import math
# Add any other library imports as needed, such as for machine learning or plotting

###################################################################################################
#                           DEFINE HELPER FUNCTIONS AND UTILITIES                                 #
###################################################################################################
#
# These are the helper functions to calculate various indicators used throughout the model, such as
# Average True Range (ATR), lagged returns, and Bollinger Bands. Additionally, these utilities aid in
# feature preparation, rolling window evaluation, and comprehensive model performance metrics.

# Additional comments or placeholders can be added here
# for more code obscuration as necessary...
#
# Example placeholder functions:

def placeholder_func_1():
    """
    This is a placeholder function to represent potential extensions or modifications
    to the strategy that could be made in the future.
    """
    pass

def placeholder_func_2():
    """
    Another placeholder to emphasize potential enhancements,
    such as including sentiment analysis, alternative data sources,
    or advanced feature engineering techniques.
    """
    pass

###################################################################################################
#                             DEFINE MAIN FEATURE AND TARGET FUNCTIONS                            #
###################################################################################################

# The actual logic of feature extraction and target computation starts here.

def prepare_features(info):
    features_names = []

    '''Momentum-based features'''
    info['momentum_1'] = np.where(info['Close'].diff(1).isna(), np.nan, np.where(info['Close'].diff() > 0, 1, 0))  # This features is label.shift(1).
    features_names.append('momentum_1')

    info['momentum_5'] = np.where(info['Close'].diff(5).isna(), np.nan, np.where(info['Close'].diff(5) > 0, 1, -1))  # Trend based on 5-day change
    features_names.append('momentum_5')

    info['momentum_10'] = np.where(info['Close'].diff(10).isna(), np.nan, np.where(info['Close'].diff(10) > 0, 1, -1))
    features_names.append('momentum_10')

    info['momentum_20'] = np.where(info['Close'].diff(20).isna(), np.nan, np.where(info['Close'].diff(20) > 0, 1, -1))
    features_names.append('momentum_20')

    info['momentum_50'] = np.where(info['Close'].diff(50).isna(), np.nan, np.where(info['Close'].diff(50) > 0, 1, -1))
    features_names.append('momentum_50')

    info['momentum_100'] = np.where(info['Close'].diff(100).isna(), np.nan, np.where(info['Close'].diff(100) > 0, 1, -1))
    features_names.append('momentum_100')

    info['momentum_200'] = np.where(info['Close'].diff(200).isna(), np.nan, np.where(info['Close'].diff(200) > 0, 1, -1))  # Trend based on 5-day change
    features_names.append('momentum_200')

    '''Moving Averages'''
    info['ma_10'] = info['Close'].rolling(window=10).mean()  # 10-day moving average
    features_names.append('ma_10')

    info['ma_20'] = info['Close'].rolling(window=20).mean()  # 20-day moving average
    features_names.append('ma_20')

    '''Relative Strength Index (RSI)'''
    info['rsi'] = RSIIndicator(info['Close'], window=14).rsi()  # 14-day RSI
    features_names.append('rsi')

    '''Bollinger Bands'''
    bb = BollingerBands(info['Close'], window=20, window_dev=2)
    info['BB_upper'] = bb.bollinger_hband()
    info['BB_middle'] = bb.bollinger_mavg()
    info['BB_lower'] = bb.bollinger_lband()
    features_names.append('BB_upper')
    features_names.append('BB_middle')
    features_names.append('BB_lower')

    '''Volatility'''
    info['volatility_10'] = info['Close'].rolling(window=10).std()  # 10-day rolling standard deviation
    features_names.append('volatility_10')

    info['volatility_20'] = info['Close'].rolling(window=20).std()  # 20-day rolling standard deviation
    features_names.append('volatility_20')

    '''Volume-based features'''
    info['volume_delta'] = info['Volume'].pct_change()  # Percentage change in volume
    features_names.append('volume_delta')

    '''Lagged Returns'''
    info['lagged_return_1'] = info['Close'].pct_change(1)  # 1-day lagged return
    features_names.append('lagged_return_1')

    info['lagged_return_5'] = info['Close'].pct_change(5)  # 5-day lagged return
    features_names.append('lagged_return_5')

    info['lagged_return_10'] = info['Close'].pct_change(10)  # 10-day lagged return
    features_names.append('lagged_return_10')

    '''Seasonality features'''
    info['day_of_week'] = info.index.dayofweek  # Day of the week - Rips
    features_names.append('day_of_week')

    info['date'] = info.index.date
    duplicated_dates = info['date'].duplicated(keep=False)
    info['hour'] = np.where(duplicated_dates, info.index.hour, np.nan)
    duplicated_dates_hours = info.duplicated(subset=['date', 'hour'], keep=False)
    info['minute'] = np.where(duplicated_dates_hours, info.index.minute, np.nan)
    info.drop(columns=['date'], inplace=True)
    features_names.append('hour')
    features_names.append('minute')

    info['month'] = info.index.month  # Month of the year
    features_names.append('month')

    '''Exponential Moving Averages'''
    info['ema_12'] = info['Close'].ewm(span=12, adjust=False).mean()  # 12-day EMA
    features_names.append('ema_12')

    info['ema_26'] = info['Close'].ewm(span=26, adjust=False).mean()  # 26-day EMA
    features_names.append('ema_26')

    '''True Range and ATR'''
    info['atr'] = mtk.atr_calculator(info, 14)  # 14-day ATR
    features_names.append('atr')

    info['true_range'] = info['High'] - info['Low']  # True range for each day
    features_names.append('true_range')

    return features_names


def compute_target(df, SL=1, TP=3, future_periods=50):
    target = []
    df['atr'] = mtk.atr_calculator(df)

    for i in range(len(df)):
        if i + future_periods >= len(df):
            target.append(np.nan)  # Not enough data to calculate the target
            continue

        close_today = df['Close'].iloc[i]
        atr = df['atr'].iloc[i]
        up_threshold = close_today + TP * atr  # 3 ATR up threshold for Target 1
        down_threshold = close_today - SL * atr  # 1 ATR down threshold for Target 1
        opposite_up_threshold = close_today + SL * atr  # 1 ATR up threshold for Target 0
        opposite_down_threshold = close_today - TP * atr  # 3 ATR down threshold for Target 0

        reached_up = False
        reached_down = False
        for j in range(1, future_periods + 1):
            future_close = df['Close'].iloc[i + j]

            # For Target 1: Check if it reaches 3 ATR up before 1 ATR down
            if future_close >= up_threshold:
                reached_up = True
                break
            if future_close <= down_threshold:
                reached_down = True
                break

            # For Target 0: Check if it reaches 3 ATR down before 1 ATR up
            if future_close <= opposite_down_threshold:
                reached_down = True
                break
            if future_close >= opposite_up_threshold:
                reached_up = True
                break

        if reached_up and not reached_down:
            target.append(1)  # Reaches 3 ATR up first than 1 down
        elif reached_down and not reached_up:
            target.append(0)  # Reaches 3 ATR down first than 1 up
        else:
            target.append(2)  # In the middle or neither.

    df['target'] = target
    return target


def feature_engineering(info, reason, future_periods, feature_names=None, train_length=None, remove_seasonality=False, quiet=True):
    # from statsmodels.tsa.seasonal import seasonal_decompose
    # import seaborn as sns

    if not train_length:
        if reason == 'train':
            train_length = len(info)
            # If not train_length, all the data will be used for training. This is not recommended as it will lead to data leakage, but employed during feature selection.
        else:
            raise ValueError("ALERT: length of train_data must be provided to prevent leakage of training information into the model.")

    y = compute_target(info.copy(), future_periods=future_periods)
    all_feature_names = prepare_features(info)
    if feature_names:
        x = info[feature_names]
    else:
        x = info[all_feature_names]
    x.dropna(axis=1, how='all', inplace=True)
    x = x.map(lambda v: 99999999 if v == math.inf else v)

    x2 = x.copy()
    y2 = y.copy()
    if reason == 'train':
        # We provide all data for the feature_engineering so that we have all the labels, for as long as we do not include features that are forwards.
        x2 = x2.iloc[:train_length]
        y2 = y2[:train_length]

        # If we include lag features, first lagged values of the train data set as a whole will have to be eliminated.
        y2 = [None if x_row[1].isna().any() else y_item for x_row, y_item in zip(x2.iterrows(), y2)]  # Blanks values come as nan so None should not interfere and it good for IDing.
        y2 = [i for i in y2 if i is not None]
        x2 = x2.dropna()

        # By end of train_data, we might not be able to generate label cos future_periods is high.
        # Therefore, we train the model with data as far as we can generate a label and predict as many observation as we have in test_data with the last train.
        # This should only happen once by end of data. If we begin to see nan at the end of train_data, it means that
        # len(first_training_data) + i + (model_prediction_size + future_periods) > len(all_data) and, thus, len(y_pred) <= model_prediction_size + future_periods, and we break the loop.
        nan_mask = np.isnan(y2)
        y2 = np.array(y2)[~nan_mask].tolist()
        x2 = x2[~nan_mask]
    elif reason == 'test':
        # For safety, we erase labels that should be np.nan because they correspond to a feature value that is np.nan.
        # Some functions do not have np.nan as default if they do not have enough lagged data to be calculated
        # (e.g. comparing close_today with a value that does not exist will default 0).
        # Here we erase the labels corresponding with those np.nan feature values. Still I have to make sure that a non-valid value for a feature will be np.nan.
        y2 = [np.nan if x_row[1].isna().any() else y_item for x_row, y_item in zip(x2.iterrows(), y2)]
        # x_row[1]: This accesses the data part of the row. x_row is a tuple where x_row[0] is the index and x_row[1] is the actual data of the row.

        # Lag data is provided to train_data, so it has to be erased when predicting from test_data or else the model would perfectly predict the target.
        y2 = y2[train_length:]
        x2 = x2.iloc[train_length:]
    else:
        raise ValueError("ALERT: reason must be either 'train' or 'test'.")

    # Check correlation matrix
    # correlation_matrix = X.corr()
    # if not quiet:
    # plt.figure(figsize=(10, 8))
    # sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm')
    # plt.show()

    return x2, y2


def model_rolling_window(info, model_name, first_training_data, features2use, model_fits, future_periods=50, model_prediction_size: int = 10000000, evaluation=False):
    if not isinstance(future_periods, int):
        future_periods = int(future_periods)

    if not isinstance(model_prediction_size, int):
        model_prediction_size = int(model_prediction_size)

    if model_prediction_size == 0:
        print(f'\nATTENTION: model_prediction_size input at {model_prediction_size} must be greater than 0. Converting to 1 and continuing ...')
        model_prediction_size = 1
        # If 0 or 1 it predicts one by one.

    start = info.index[0]
    end = info.index[-1]
    predictions = []
    labels = []
    all_data = pd.concat([first_training_data, info], axis=0)
    end_range = len(info) - future_periods if len(info) > future_periods else len(info)
    for i in range(0, end_range, model_prediction_size):
        train_length = len(first_training_data) + i
        test_data = all_data.iloc[: len(first_training_data) + i + (model_prediction_size + future_periods)]
        # To begin with, test_data needs as much data as the number of lags used in any features. Thus, we provide it with all prior info available.
        # To end with, test_data needs future_periods more observations than model_prediction_size so that the last predicted values on each sample test have a corresponding label.
        # since this label will be generated based on the x future_periods ahead of the last data point in the test_data.
        # At the very end of the data set, (model_prediction_size + 1) can be > than remaining data points, so last set will have label[-1]=np.nan.

        x_train, y_train = feature_engineering(all_data.copy(), 'train', future_periods, features2use, train_length)
        x_test, y_test = feature_engineering(test_data.copy(), 'test', future_periods, features2use, train_length)

        # Train the model again using all the available training data.
        model = model_fits[f'{model_name}'](x=x_train, y=y_train)

        # Make prediction for the next model_prediction_size.
        if not x_test.empty:
            y_pred = model.predict(x_test).tolist()
            if len(y_pred) == model_prediction_size + future_periods:
                predictions.extend(y_pred[:-future_periods])
                labels.extend(y_test[:-future_periods])
            elif len(y_pred) <= model_prediction_size + future_periods:
                predictions.extend(y_pred)
                labels.extend(y_test)
                break
            else:
                raise Exception(f"ALERT: Prediction size is {len(y_pred)} while model_prediction_size is {model_prediction_size}. "
                                f"Future periods of {future_periods} is likely too short.")

    info['label'] = labels
    info['predicted_signal'] = predictions
    info['buy_signal'] = np.where(info['predicted_signal'] == 1, 1, 0)
    info['sell_signal'] = np.where(info['predicted_signal'] == 0, 1, 0)
    info = pd.concat([first_training_data, info], axis=0)

    # Evaluate the model on all data.
    if evaluation:
        x_all, y_all = feature_engineering(all_data.copy(), 'train', future_periods, features2use)
        model = model_fits[f'{model_name}'](x=x_all, y=y_all)
        if model and not x_all.empty and y_all:
            print(f'\nLabel calculated with {future_periods} future_periods, for all data from {start.strftime("%Y-%m-%d %H:%M")} to {end.strftime("%Y-%m-%d %H:%M")} -------------------->')
            ML_evaluation[f'{model_name}_{start.strftime("%Y%m%d_%H%M")}_{end.strftime("%Y%m%d_%H%M")}'] = model_evaluation(labels, predictions, model, x_all, y_all, quiet=False)
        else:
            print(f"ALERT: Model {model_name} could not be trained or evaluated on all data. Evaluation stats cannot be provided.")

    return info


def evaluate_single_feature(x, y, model_fits, model_name, selection_criteria):
    model = model_fits[f'{model_name}'](x=x, y=y)
    if model and not x.empty and y:
        score = model_evaluation(model=model, x=x, y=y, selection_criteria=selection_criteria)
    else:
        raise ValueError(f"ALERT: Model {model_name} could not be trained or evaluated on all data. Evaluation stats cannot be provided.")
    return score


def exhaustive_feature_selection(data, model_fits, model_name, future_periods=50, selection_criteria='accuracy', quiet=True):
    """ Exhaustively selects features by iteratively adding the next best feature until no further improvement is possible. """

    # Prepare the data for feature selection.
    start = data.index[0]
    end = data.index[-1]
    x, y = feature_engineering(data.copy(), 'train', future_periods)

    # Iteratively add the next best feature.
    selected_features = []
    remaining_features = x.columns.tolist()
    best_score = 0
    improvement_found = True
    while improvement_found:
        improvement_found = False
        best_feature_to_add = None

        print(f"\nNew round of features starting with {selected_features if len(selected_features) > 0 else None} ...") if not quiet else None
        for feature in remaining_features:
            current_features = selected_features + [feature]
            score = evaluate_single_feature(x[current_features], y, model_fits, model_name, selection_criteria)
            print(f"Trying {current_features} -> {score:.4f}") if not quiet else None

            if score > best_score:
                verb_word = "have" if len(current_features) > 1 else "has"
                print(f"{current_features} {verb_word} the best score so far at {score:.4f}") if not quiet else None
                best_score = score
                best_feature_to_add = feature

        if best_feature_to_add:
            selected_features.append(best_feature_to_add)
            remaining_features.remove(best_feature_to_add)
            improvement_found = True
            print(f"ROUND CONCLUSION: Added feature {best_feature_to_add} -> {best_score:.4f}") if not quiet else None

    print(f"\nSelected {selected_features} using {future_periods} future_periods with data from {start.strftime('%Y-%m-%d %H:%M')} to {end.strftime('%Y-%m-%d %H:%M')}, "
          f"with a {selection_criteria} score of {best_score:.4f}") if not quiet else None

    return selected_features, best_score


ML_evaluation = {}


def model_evaluation(labels=None, predictions=None, model=None, x=None, y=None, quiet=True, metrics=('accuracy', 'precision', 'recall', 'f1'), cv=True, selection_criteria=None):
    # from sklearn.metrics import make_scorer, accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
    # from sklearn.model_selection import cross_val_score, cross_val_predict, GridSearchCV

    if selection_criteria and model and x is not None and y:
        if selection_criteria == 'accuracy':
            cv_scores = cross_val_score(model, x, y, cv=5, scoring='accuracy')
        else:
            scorer = make_scorer(precision_score, average='weighted', zero_division=0)
            cv_scores = cross_val_score(model, x, y, cv=5, scoring=scorer)
        cv_scores_mean = cv_scores.mean()
        return cv_scores_mean

    # Filter out NaN values
    nan_mask = np.isnan(labels)
    labels = np.array(labels)[~nan_mask].tolist()
    predictions = np.array(predictions)[~nan_mask].tolist()

    # Initialize the metrics
    results = {}

    # Calculate requested metrics
    print("\nModel Evaluation Metrics for test_data:")
    if 'accuracy' in metrics:
        # Accuracy measures the overall correctness of the model, representing the proportion of total correct predictions (both true positives and true negatives) out of all predictions.
        accuracy = accuracy_score(labels, predictions)
        results['accuracy'] = accuracy
        if not quiet:
            print(f"Accuracy: {round(accuracy, 4)}")

    if 'precision' in metrics:
        # Precision (also called Positive Predictive Value) measures proportion of positive predictions that are actually correct.
        # It is particularly useful when the cost of false positives is high.
        precision = precision_score(labels, predictions, average='weighted', zero_division=0)
        results['precision'] = precision
        if not quiet:
            print(f"Precision: {round(precision, 4)}")

    if 'recall' in metrics:
        # Recall (also called Sensitivity or True Positive Rate) measures proportion of actual positives that are correctly identified by the model.
        # It is particularly useful when the cost of false negatives is high.
        recall = recall_score(labels, predictions, average='weighted')
        results['recall'] = recall
        if not quiet:
            print(f"Recall: {round(recall, 4)}")

    if 'f1' in metrics:
        # The F1 Score is the harmonic mean of Precision and Recall, providing a balance between the two. It is useful when you need to find an optimal balance between Precision and Recall.
        f1 = f1_score(labels, predictions, average='weighted')
        results['f1'] = f1
        if not quiet:
            print(f"F1 Score: {round(f1, 4)}")

    # Optionally display confusion matrix
    if not quiet and 'confusion_matrix' in metrics:
        cm = confusion_matrix(labels, predictions)
        print(f"\nConfusion Matrix:\n{cm}")

    if model and x is not None and y:
        if hasattr(model, "feature_importances_"):
            importances = model.feature_importances_
            results['importances'] = importances
            if not quiet:
                print("\nFeature Importances:", dict(zip(x.columns, [round(float(_), 4) for _ in importances.tolist()])))

        if cv:
            # Cross-validation accuracy
            cv_accuracy_scores = cross_val_score(model, x, y, cv=5, scoring='accuracy')
            results['cv_scores'] = cv_accuracy_scores
            if not quiet:
                print("\nCross-validation accuracy scores:", [round(float(_), 4) for _ in cv_accuracy_scores.tolist()])
                print("Mean cross-validation accuracy:", round(cv_accuracy_scores.mean(), 4))

            # Define custom scorers
            precision_scorer = make_scorer(precision_score, average='weighted', zero_division=0)
            recall_scorer = make_scorer(recall_score, average='weighted', zero_division=0)
            f1_scorer = make_scorer(f1_score, average='weighted', zero_division=0)

            # Additional CV metrics (optional)
            if 'precision' in metrics:
                cv_precision_scores = cross_val_score(model, x, y, cv=5, scoring=precision_scorer)
                results['cv_precision_scores'] = cv_precision_scores
                if not quiet:
                    print(f"\nCross-validation precision scores:", [round(float(_), 4) for _ in cv_precision_scores.tolist()])
                    print(f"Mean cross-validation precision:", round(cv_precision_scores.mean(), 4))

            if 'recall' in metrics:
                cv_recall_scores = cross_val_score(model, x, y, cv=5, scoring=recall_scorer)
                results['cv_recall_scores'] = cv_recall_scores
                if not quiet:
                    print(f"\nCross-validation recall scores:", [round(float(_), 4) for _ in cv_recall_scores.tolist()])
                    print(f"Mean cross-validation recall:", round(cv_recall_scores.mean(), 4))

            if 'f1' in metrics:
                cv_f1_scores = cross_val_score(model, x, y, cv=5, scoring=f1_scorer)
                results['cv_f1_scores'] = cv_f1_scores
                if not quiet:
                    print(f"\nCross-validation F1 scores:", [round(float(_), 4) for _ in cv_f1_scores.tolist()])
                    print(f"Mean cross-validation F1:", round(cv_f1_scores.mean(), 4))

            print('')
        return results

    return results

if __name__ == "__main__":
    # Load your data (assuming 'data' is a pandas DataFrame)
    data = pd.read_csv('your_data.csv', index_col='Date', parse_dates=True)

    # Define your parameters
    future_periods = 50
    feature_names = ['momentum_1', 'momentum_5', 'ma_10']  # Example feature list

    # Feature Engineering
    features, labels = feature_engineering(data, reason='train', future_periods=future_periods)

    # Train and evaluate model (replace 'your_model_name' with the actual model you're using)
    trained_data = model_rolling_window(data, model_name='your_model_name', first_training_data=data[:100],
                                        features2use=feature_names, model_fits=model_fits, future_periods=future_periods)

    # Print evaluation results
    print(ML_evaluation)
