import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.calibration import CalibratedClassifierCV
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
import joblib
from feature_extraction import extract_features, get_feature_names
from ucimlrepo import fetch_ucirepo 

MODEL_PATH = 'model.pkl'

def train():
    print("Fetching PhiUSIIL Phishing URL Dataset from UCI Repo...")

    try:
        dataset = fetch_ucirepo(id=967)

        X_uci = dataset.data.features
        y_uci = dataset.data.targets

        df = pd.concat([X_uci, y_uci], axis=1)

        url_col = next(col for col in df.columns if 'url' in col.lower())
        label_col = df.columns[-1]

        print(f"URL column: {url_col}")
        print(f"Label column: {label_col}")
        print(f"Label distribution:\n{df[label_col].value_counts()}")

        positive_names = {'phishing', 'phish', '1', 'true', 'yes', 'malicious', 'unsafe', 'suspicious', 'bad'}

        def is_positive(x):
            try:
                sx = str(x).strip().lower()
            except Exception:
                return 0
            if sx in positive_names:
                return 1
            try:
                if float(sx) == 1.0:
                    return 1
            except Exception:
                pass
            return 0

        df['label_bin'] = df[label_col].apply(is_positive)
        print(f"Binary label distribution:\n{df['label_bin'].value_counts()}")
        label_col = 'label_bin'

        initial_count = len(df)
        df = df.drop_duplicates(subset=[url_col])
        print(f"Removed {initial_count - len(df)} duplicate URLs")

        train_df, test_df = train_test_split(
            df,
            test_size=0.2,
            random_state=42,
            stratify=df[label_col]
        )

        print(f"Training samples: {len(train_df)}")
        print(f"Testing samples: {len(test_df)}")

        print("Extracting features...")
        X_train = pd.DataFrame(
            train_df[url_col].astype(str).apply(extract_features).tolist(),
            columns=get_feature_names()
        )
        y_train = train_df[label_col].tolist()

        X_test = pd.DataFrame(
            test_df[url_col].astype(str).apply(extract_features).tolist(),
            columns=get_feature_names()
        )
        y_test = test_df[label_col].tolist()

        print(f"Features used ({len(get_feature_names())}):")
        print(get_feature_names())

        base_clf = RandomForestClassifier(
            n_estimators=300,
            max_depth=20,
            min_samples_split=5,
            class_weight="balanced",
            random_state=42,
            n_jobs=-1
        )

        print("\nRunning cross-validation on base estimator...")
        cv_scores = cross_val_score(base_clf, X_train, y_train, cv=5, scoring="f1")
        print(f"CV F1-score: {cv_scores.mean():.4f} ± {cv_scores.std():.4f}")

        print("\nTraining final base model...")
        base_clf.fit(X_train, y_train)

        print("\nCalibrating probabilities (CalibratedClassifierCV)...")
        calib_clf = CalibratedClassifierCV(estimator=RandomForestClassifier(
            n_estimators=300,
            max_depth=20,
            min_samples_split=5,
            class_weight="balanced",
            random_state=42,
            n_jobs=-1
        ), cv=5, method='sigmoid')
        calib_clf.fit(X_train, y_train)

        print("\nEvaluating on test set...")
        y_pred = calib_clf.predict(X_test)

        print(f"Accuracy: {accuracy_score(y_test, y_pred):.4f}")
        print("\nClassification Report:")
        print(classification_report(y_test, y_pred))

        print("Confusion Matrix:")
        print(confusion_matrix(y_test, y_pred))

        print("\nFeature Importances (base estimator):")
        for name, importance in sorted(
            zip(get_feature_names(), base_clf.feature_importances_),
            key=lambda x: -x[1]
        ):
            print(f"  {name}: {importance:.4f}")

        print(f"\nSaving calibrated model to {MODEL_PATH}")
        joblib.dump(calib_clf, MODEL_PATH)

        print("Training complete.")

    except Exception as e:
        print("Training failed:")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    train()
