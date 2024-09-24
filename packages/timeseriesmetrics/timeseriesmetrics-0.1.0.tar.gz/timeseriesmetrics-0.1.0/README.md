# Timeseries Metrics

This package provides several metrics used to evaluate the performance of predictive models in time series.

## Installation

You can install the package using `pip`:

```bash
pip install timeseriesmetrics
```

## Usage

The package can be used as follows:

```python
from timeseriesmetrics import *

y_true = [1, 2, 3, 4, 5]
y_pred = [3, 4, 3, 4, 5]

theil(y_true, y_pred)
```

Where `y_true` represents the real values ​​and `y_pred` the predicted values.

## Definitions

- $ N $: number of observations.
- $ u_{t} $: real values.
- $ \widehat{u}_{t} $: predicted values.
- $ \overline{u}_{t} $: mean of the real values.

## Available Metrics

### MAPE

MAPE (Mean Absolute Percentage Error) measures the accuracy of the model, presenting a relative value:

$$
MAPE = \frac{100}{N} \sum_{t=1}^{N} \left| \frac{u_{t} - \widehat{u}_{t}}{u_{t}} \right| $$

### ARV

ARV (Average Relative Variance) compares the predictor's performance with the simple average of past values ​​in the series:

$$
ARV = \frac{\sum_{t=1}^{N} \left( u_{t} - \widehat{u}_{t} \right)^{2}}{\sum_{t=1}^{N} \left( \widehat{u}_{t} - \overline{u}_{t} \right)^{2}}
$$

### ID

ID (Index of Disagreement) disregards the unit of measurement, presenting values ​​in the interval [0, 1]:

$$
ID = \frac{\sum_{t=1}^{N} \left( \widehat{u}_{t} - u_{t} \right)^{2}}{\sum_{t=1}^{N} \left( \left| \widehat{u}_{t} - \overline{u}_{t} \right| + \left| u_{t} - \overline{u}_{t} \right| \right)^{2}} $$ 

### Theil'U 
Theil'U compares prediction performance to the Random Walk model (in which $ u_{t} $ is inferred by $ u_{t-1} $), where `Theil< 1` indicates a better prediction than the Random Walk model:

$$ Theil = \frac{\sum_{t=2}^{N} \left( u_{t} - \widehat{u}_{t} \right)^{2}}{\sum_{t=2}^{N} \left( u_{t} - u_{t-1} \right)^{2}} $$ 

### WPOCID 
WPOCID measures how well the model predicts the trend of the target time series: 

$$
\left.\begin{aligned}
& WPOCID = 1 - \frac{\sum_{t=2}^{N} D_{t}}{N-1}, \\
& D_{t} = \left\{ 
\begin{array}{l}
1, \text{ se } \left( u_{t} - u_{t-1} \right) \left( \widehat{u}_{t} - \widehat{u}_{t-1} \right) \geq 0 \\
0, \text{ se } \left( u_{t} - u_{t-1} \right) \left( \widehat{u}_{t} - \widehat{u}_{t-1} \right) < 0
\end{array}
\right.
\end{aligned}\right.
$$


## References

More details on the metrics discussed can be found in the article [A non-central beta model to forecast and evaluate pandemics time series](https://www.sciencedirect.com/science/article/pii/S096007792030607X).