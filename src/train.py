import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
import joblib
from feature_extraction import extract_features, get_feature_names
from ucimlrepo import fetch_ucirepo 

MODEL_PATH = 'model.pkl'
SCALER_PATH = 'scaler.pkl'

def train():
    print("Fetching PhiUSIIL Phishing URL Dataset from UCI Repo...")

    try:
        phiusiil_phishing_url_website = fetch_ucirepo(id=967) 
        
        X_uci = phiusiil_phishing_url_website.data.features
        y_uci = phiusiil_phishing_url_website.data.targets
        
        df = pd.concat([X_uci, y_uci], axis=1)
        url_col = None
        for col in df.columns:
            if 'url' in col.lower():
                url_col = col
                break
        
        if not url_col:
            print("Error: Could not find URL column in UCI dataset.")
            return

        print(f"Dataset URL column: {url_col}")
        
        label_col = df.columns[-1]
        print(f"Label column: {label_col}")
        print(f"Label distribution:\n{df[label_col].value_counts()}")
        
        initial_count = len(df)
        df_clean = df.drop_duplicates(subset=[url_col], keep='first')
        print(f"Removed {initial_count - len(df_clean)} duplicate URLs. Total unique: {len(df_clean)}")
        
        train_df, test_df = train_test_split(df_clean, test_size=0.2, random_state=42, stratify=df_clean[label_col])
        
        print(f"Training set: {len(train_df)}, Test set: {len(test_df)}")

        print("Extracting features for Training set...")
        X_train_list = train_df[url_col].astype(str).apply(extract_features).tolist()
        y_train = train_df[label_col].tolist()

        print("Extracting features for Test set...")
        X_test_list = test_df[url_col].astype(str).apply(extract_features).tolist()
        y_test = test_df[label_col].tolist()
        
        X_train = pd.DataFrame(X_train_list, columns=get_feature_names())
        X_test = pd.DataFrame(X_test_list, columns=get_feature_names())

        print(f"Features used: {list(X_train.columns)}")
        
        print("Scaling features...")
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        
        print("\nFeature statistics (Training set):")
        for i, name in enumerate(get_feature_names()):
            print(f"  {name}: mean={X_train_scaled[:,i].mean():.3f}, std={X_train_scaled[:,i].std():.3f}")

        print("\nTraining Random Forest model (n_estimators=200)...")
        clf = RandomForestClassifier(
            n_estimators=200, 
            random_state=42, 
            n_jobs=-1,
            max_depth=20,
            min_samples_split=5,
            class_weight='balanced'
        )
        
        cv_scores = cross_val_score(clf, X_train_scaled, y_train, cv=5)
        print(f"Cross-Validation Accuracy (Train): {cv_scores.mean():.4f} (+/- {cv_scores.std() * 2:.4f})")
        
        clf.fit(X_train_scaled, y_train)

        print("\n--- Final Evaluation on Test Set ---")
        y_pred = clf.predict(X_test_scaled)
        acc = accuracy_score(y_test, y_pred)
        print(f"Test Accuracy: {acc:.4f}")
        print("\nClassification Report:")
        print(classification_report(y_test, y_pred))

        print("Confusion Matrix:")
        print(confusion_matrix(y_test, y_pred))
        
        print("\nFeature Importance:")
        importances = clf.feature_importances_
        for name, imp in sorted(zip(get_feature_names(), importances), key=lambda x: -x[1]):
            print(f"  {name}: {imp:.4f}")

        print(f"\nSaving model to {MODEL_PATH}...")
        joblib.dump(clf, MODEL_PATH)
        
        print(f"Saving scaler to {SCALER_PATH}...")
        joblib.dump(scaler, SCALER_PATH)
        
        print("Done!")

    except Exception as e:
        print("Training failed:")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    train()
