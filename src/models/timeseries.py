from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_squared_error

class ARIMAForecaster:
    def __init__(self, order=(1,1,1)):
        self.order = order
        self.model = None

    def fit(self, data):
        self.model = ARIMA(data, order=self.order)
        self.model_fit = self.model.fit()
        return self.model_fit.summary()

    def predict(self, steps=5):
        if not self.model:
            raise ValueError("Model not trained")
        return self.model_fit.forecast(steps=steps)
