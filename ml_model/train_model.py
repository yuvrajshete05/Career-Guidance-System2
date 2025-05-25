from sklearn.ensemble import RandomForestClassifier
import joblib
import os

# Example training data
X_train = [[21, 8.5], [22, 7.0], [20, 9.1]]  # features like age, CGPA, etc.
y_train = ['Data Scientist', 'Web Developer', 'AI Researcher']  # career labels

# Train model
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Save the trained model
os.makedirs('ml_model', exist_ok=True)  # Create folder if not exists
joblib.dump(model, 'ml_model/predictcareer.pkl')
