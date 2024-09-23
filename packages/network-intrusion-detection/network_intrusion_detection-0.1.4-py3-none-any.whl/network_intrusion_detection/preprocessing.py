import pandas as pd
from sklearn.preprocessing import StandardScaler
from imblearn.over_sampling import SMOTE

def preprocess_data(csv_file):
    """Preprocess the input CSV file and return features and target."""
    df = pd.read_csv(csv_file)
    # Handle null values
    df = df.dropna()
    # Drop duplicate rows
    df = df.drop_duplicates()
    # Encode target column
    df['Label'] = df['Label'].apply(lambda x: 0 if x == 'Benign' else 1)
    # Normalize numerical columns
    scaler = StandardScaler()
    numerical_cols = df.select_dtypes(include=['float64', 'int64']).columns
    df[numerical_cols] = scaler.fit_transform(df[numerical_cols])
    # Separate features and target
    X = df.drop('Label', axis=1)
    y = df['Label']
    # Apply SMOTE
    smote = SMOTE()
    X_resampled, y_resampled = smote.fit_resample(X, y)
    return X_resampled, y_resampled
