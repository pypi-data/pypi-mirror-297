## Table of Contents

Introduction

Installation

Code Example: Feature Engineering

Code Example: Target Computation

Full Example with Model Training

Contributions

License

## Introduction
This Python module provides a set of functions to streamline feature engineering, target generation, rolling window model training, and model evaluation for time-series data. It is particularly designed for financial data like stock prices, allowing the user to create momentum-based features, moving averages, seasonality features, and more. This tool also provides feature selection utilities and model evaluation metrics like accuracy, precision, recall, and F1 score.

## Installation

Before running the code, make sure the following libraries are installed:

```bash
pip install numpy pandas ta-lib scikit-learn statsmodels matplotlib seaborn
```

## Usage/Examples

### Code Example: Feature Engineering

The function prepare_features generates technical indicators based on stock price data, including momentum, moving averages, Bollinger Bands, and more.

```python
import numpy as np
import pandas as pd
from ta.momentum import RSIIndicator
from ta.volatility import BollingerBands

# Sample input dataframe
data = pd.DataFrame({
    'Close': [100, 102, 101, 105, 107, 109, 108, 110, 111, 113],
    'Volume': [2000, 2100, 2050, 2200, 2300, 2250, 2400, 2500, 2450, 2600]
}, index=pd.date_range('2023-01-01', periods=10))

# Call the feature engineering function
feature_names = prepare_features(data)

print(data[feature_names].head())
```

### Code Example: Target Computation

```python
# Generate target for the given dataframe
target = compute_target(data, SL=1, TP=3, future_periods=3)

print(target)
```

### Full Example with Model Training

```python
# Feature engineering on full dataset
x_train, y_train = feature_engineering(data, 'train', future_periods=3)

# Train a random forest model
rf_model = RandomForestClassifier()
rf_model.fit(x_train, y_train)

# Make predictions
y_pred = rf_model.predict(x_train)

# Evaluate the model
evaluation = model_evaluation(
    labels=y_train,
    predictions=y_pred,
    model=rf_model,
    x=x_train,
    y=y_train
)

print(evaluation)
```

## Contributions

If you'd like to contribute to this project, feel free to submit a pull request or open an issue for any bugs or feature requests.


## License

This is free and unencumbered software released into the public domain.

Anyone is free to copy, modify, publish, use, compile, sell, or
distribute this software, either in source code form or as a compiled
binary, for any purpose, commercial or non-commercial, and by any
means.

In jurisdictions that recognize copyright laws, the author or authors
of this software dedicate any and all copyright interest in the
software to the public domain. We make this dedication for the benefit
of the public at large and to the detriment of our heirs and
successors. We intend this dedication to be an overt act of
relinquishment in perpetuity of all present and future rights to this
software under copyright law.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.

For more information, please refer to <https://unlicense.org>






