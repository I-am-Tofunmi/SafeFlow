import pickle
import os
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

# Ensure the folder exists
if not os.path.exists("ml"):
    os.makedirs("ml")

# 1. Dummy Data (The "School Books" for the AI)
sms_data = [
    "Urgent! You won 5000N. Click link to claim", 
    "Your OTP is 4455. Do not share.",
    "Hey, how are you doing today?",
    "Bank Alert: 5000N debited from your account.",
    "Click this link to update your BVN immediately",
    "Hello my friend, long time no see",
    "Your account has been blocked. Call this number",
    "Transaction successful. 2000 sent to Mama."
]
# 1 = Scam, 0 = Safe
labels = [1, 1, 0, 0, 1, 0, 1, 0] 

print("🧠 Training AI Model...")

# 2. Train Model
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(sms_data)
clf = MultinomialNB()
clf.fit(X, labels)

# 3. Save the "Brain" to files
with open("ml/sms_spam_model.pkl", "wb") as f:
    pickle.dump(clf, f)
    
with open("ml/vectorizer.pkl", "wb") as f:
    pickle.dump(vectorizer, f)

print("✅ Model trained and saved to ml/ folder!")