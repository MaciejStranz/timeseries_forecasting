# 🧠⛅ Weather Forecasting using Sequential Models

## 📌 Project Overview

This project aims to develop and compare models for forecasting weather conditions using various sequential modeling techniques. The goal is to predict weather features like temperature, humidity, and wind speed based on historical data. The models are tested over different prediction horizons (1h, 6h, 12h, 24h), and evaluated both quantitatively (via metrics) and qualitatively (via visualization).

## ✅ Assumptions

- **Input Data**: Weather data from reliable sources such as meteorological stations or public APIs. Variables include temperature, humidity, wind speed, pressure, and visibility.
- **Data Preprocessing**: All input data is cleaned (missing values and outliers), normalized, and scaled for modeling.
- **Data Splitting**: 80% training, 10% validation, 10% test.
- **Reproducibility**: Full documentation ensures the experiments are reproducible.

## 🔍 Models Used

- **LSTM (Long Short-Term Memory)**  
  A type of RNN designed to learn long-term dependencies, ideal for time series data.

- **Custom Transformer-based Architecture**  
  Inspired by the original Transformer model with encoder-decoder structure, positional encoding, and teacher forcing.

## 📊 Datasets

- [Weather History Dataset (Kaggle)](https://www.kaggle.com/datasets/muthuj7/weather-dataset)  
  Weather data over 10 years from one location.

- [Jena Climate Dataset](https://www.kaggle.com/datasets/mnassrib/jena-climate)  
  Data collected at the Max Planck Institute for Biogeochemistry in Jena, Germany.

## 🧪 Experiments

- Forecasting temperature and humidity.
- Four prediction horizons: **6h, 8h, 12h, 24h**.
- Comparison between LSTM and Transformer models.
- Evaluation on two datasets.

## 📈 Evaluation Metrics

- **RMSE** (Root Mean Squared Error)  
- **MAE** (Mean Absolute Error)

## 🛠️ Tools & Technologies

- `PyTorch`, `TensorFlow` — for model development  
- `NumPy`, `pandas` — for data processing  
- `matplotlib` — for visualization  
- `Google Colab` — runtime environment

## 🎯 Expected Results

- Implementation and training of multiple forecasting models.
- Visual comparison of predictions and ground truth.
- Model performance analysis over various prediction horizons.
- Cross-reference with academic research:
  - [Springer AI Forecasting Paper](https://link.springer.com/article/10.1007/s10489-023-04824-w)  
  - [Nature Weather Prediction Study](https://www.nature.com/articles/s41586-023-06185-3)

## 🏗️ Implementation Summary

- Two models: `LSTM`, and a **custom Transformer** with 3 encoders and 3 decoders.
- Positional encoding (sinusoidal) was applied for cyclic time patterns.
- Teacher forcing was used to improve training convergence.
- Each feature (temperature, humidity) trained in separate models.
- Models trained for up to 1000 epochs depending on horizon length.

## 📊 Key Findings

### LSTM on Jena Dataset
- Performs well on **temperature**.
- Maintains bounds in predictions and follows overall shape.
- Less accurate on **humidity**, with tighter and less variable predictions.

### LSTM on Weather History Dataset
- Better at **humidity** than temperature.
- Predictions are conservative and smoother than real values.
- Shorter horizons yield better accuracy.

### Transformer on Jena Dataset
- Weaker performance than LSTM.
- Captures **trend direction**, but struggles with exact values—especially at longer horizons.

### Transformer on Weather History Dataset
- Similar behavior as with Jena dataset.
- Performs better on **temperature** than **humidity**.

## 📌 Conclusions

- LSTM outperforms the custom Transformer for this task in most cases.
- Both models capture general trends, but accuracy drops with longer prediction windows.
- Predictions often fail to reflect extreme values.
- Results align with findings in academic literature—accurate short-term forecasts, with degradation in longer-term horizons.

---

