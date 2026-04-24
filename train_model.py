import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
from feature_extractor import extract_features

data = {
    "url": [
        "https://google.com",
        "https://github.com",
        "https://youtube.com",
        "https://openai.com",
        "https://microsoft.com",
        "https://www.wikipedia.org",
        "https://www.amazon.com",
        "https://stackoverflow.com",
        "https://www.netflix.com",
        "https://www.linkedin.com",

        "http://secure-login-bank.com",
        "http://verify-paypal-account.com",
        "http://free-gift-login.com",
        "http://192.168.1.1/login",
        "http://update-your-bank-info.com",
        "http://paypal-account-confirm.com",
        "http://login-secure-update.com",
        "http://bank-verification-alert.com",
        "http://account-security-check.com",
        "http://free-prize-confirm.com"
    ],
    "label": [
        0,0,0,0,0,0,0,0,0,0,
        1,1,1,1,1,1,1,1,1,1
    ]
}

df = pd.DataFrame(data)

X = df["url"].apply(extract_features).tolist()
y = df["label"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42
)

model = RandomForestClassifier(
    n_estimators=150,
    random_state=42
)

model.fit(X_train, y_train)

y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)

print("Modelo entrenado correctamente")
print(f"Accuracy: {accuracy:.2f}")
print(classification_report(y_test, y_pred))

joblib.dump(model, "model.pkl")