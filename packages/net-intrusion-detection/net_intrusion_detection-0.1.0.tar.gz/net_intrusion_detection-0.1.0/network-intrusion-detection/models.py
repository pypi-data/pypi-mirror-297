import tensorflow as tf
import pandas as pd
import numpy as np

def load_model(model_path):
    """
    Load the pre-trained CNN-LSTM model from the specified path.

    Parameters:
    model_path (str): Path to the model file (.h5 format).

    Returns:
    tf.keras.Model: Loaded TensorFlow model.
    """
    try:
        model = tf.keras.models.load_model(model_path)
        print(f"Model loaded successfully from {model_path}")
        return model
    except Exception as e:
        print(f"Error loading model: {str(e)}")
        return None

def preprocess_data(data_path):
    """
    Load and preprocess network traffic data from a CSV file.

    Parameters:
    data_path (str): Path to the CSV file containing network traffic data.

    Returns:
    np.ndarray: Preprocessed data ready for model prediction.
    """
    try:
        # Load data from the CSV file
        df = pd.read_csv(data_path)
        
        # Drop unnecessary columns (e.g., labels or non-numeric data)
        if 'label' in df.columns:
            df = df.drop(columns=['label'])
        
        # Normalize the data (z-score normalization)
        normalized_data = (df - df.mean()) / df.std()
        
        # Convert the DataFrame to a NumPy array for TensorFlow model input
        return normalized_data.values
    except Exception as e:
        print(f"Error preprocessing data: {str(e)}")
        return None

def predict_traffic(model, data):
    """
    Use the loaded model to predict whether network traffic is benign or malicious.

    Parameters:
    model (tf.keras.Model): The loaded CNN-LSTM model.
    data (np.ndarray): Preprocessed network traffic data.

    Returns:
    np.ndarray: Predictions (0 = benign, 1 = malicious).
    """
    try:
        # Ensure the data is in the correct shape for the model
        predictions = model.predict(data)
        
        # Apply a threshold to classify benign (0) vs malicious (1)
        predicted_labels = np.argmax(predictions, axis=1)
        return predicted_labels
    except Exception as e:
        print(f"Error making predictions: {str(e)}")
        return None
