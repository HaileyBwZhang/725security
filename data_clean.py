import os
import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from textblob import TextBlob  # For sentiment analysis
import matplotlib.pyplot as plt
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import seaborn as sns

# Download stopwords if you haven't already
nltk.download('stopwords')
nltk.download('punkt')


# Define stopwords
stop_words = set(stopwords.words('english'))

# Define a function to remove emojis
def remove_emoji(text):
    # This pattern matches emojis and other special characters
    emoji_pattern = re.compile(
        "["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"\U00002702-\U000027B0"  # dingbats
        u"\U000024C2-\U0001F251"  # enclosed characters
        "]+", flags=re.UNICODE
    )
    return emoji_pattern.sub(r'', text)

# Define a cleaning function
def clean_review(review):
    if isinstance(review, str):  # Check if the review is a string
        # Remove emojis first
        review = remove_emoji(review)
        # Remove special characters and numbers (keep only letters and spaces)
        review = re.sub(r'[^a-zA-Z\s]', '', review)
        # Convert to lowercase
        review = review.lower()
        # Remove stop words
        review = ' '.join([word for word in review.split() if word not in stop_words])
    else:
        # If the content is not a string, return an empty string
        review = ''
    return review

# Define keywords for each category ['interface', 'design', 'layout', 'navigation']

ui_keywords = ['interface', 'design', 'layout', 'navigation', 'appearance', 'look']
integration_keywords = ['integration','compatible','devices','sync','connect','interoperability']
control_keywords = ['control','responsive','interaction','commands','manage','operate','setting']
# Define keywords for each security category
privacy_keywords = [
    'privacy', 'data', 'information', 'share', 'leak',
    'confidential', 'access', 'personal', 'sensitive', 
    'tracking', 'consent', 'GDPR', 'policy'
]
security_features_keywords = [
    'secure', 'encryption', 'protection', 'safeguard', 
    'safety', 'firewall', 'antivirus', 'security measures', 
    'risk management', 'compliance', 'breach prevention'
]
authentication_keywords = [
    'password', 'login', 'biometrics', 'two-factor', 
    'authentication', 'access control', 'security questions', 
    'account verification', 'identity verification'
]
vulnerability_keywords = [
    'hack', 'breach', 'exploit', 'risk', 'attack', 
    'vulnerability', 'phishing', 'malware', 'security flaw', 
    'loophole', 'weakness', 'threat'
]
updates_keywords = [
    'update', 'patch', 'improve', 'fix', 'version', 
    'release', 'maintenance', 'upgrade', 
    'security enhancement', 'timely updates', 'regular updates'
]


# Function to check if a review mentions any of the keywords
def categorize_review(review, keywords):
    for word in keywords:
        if word in review:
            return True
    return False

# Define sentiment categories based on score
def categorize_sentiment(score):
    if score >= 0.05:
        return 'Positive'
    elif score <= -0.05:
        return 'Negative'
    else:
        return 'Neutral'


analyzer = SentimentIntensityAnalyzer()

def get_sentiment_score(review):
    score = analyzer.polarity_scores(review)
    return score['compound']  # We use the compound score which gives an overall sentiment


# Function to clean the dataset
def clean_data(file_path, save_dir):
    # Read the CSV file
    df = pd.read_csv(file_path)

    # Apply cleaning to the 'content' column
    df['cleaned_content'] = df['content'].apply(clean_review)

    # Apply the function to categorize the reviews by various aspects
    df['UI'] = df['cleaned_content'].apply(lambda x: categorize_review(x, ui_keywords))
    df['Integration'] = df['cleaned_content'].apply(lambda x: categorize_review(x, integration_keywords))
    df['Control'] = df['cleaned_content'].apply(lambda x: categorize_review(x, control_keywords))
    df['Privacy'] = df['cleaned_content'].apply(lambda x: categorize_review(x, privacy_keywords))
    df['Security'] = df['cleaned_content'].apply(lambda x: categorize_review(x, security_features_keywords))
    df['Authentication'] = df['cleaned_content'].apply(lambda x: categorize_review(x, authentication_keywords))
    df['Vulnerability'] = df['cleaned_content'].apply(lambda x: categorize_review(x, vulnerability_keywords))
    df['Updates'] = df['cleaned_content'].apply(lambda x: categorize_review(x, updates_keywords))

    # Analyze sentiment for each review
    # Apply the sentiment analysis function
    df['sentiment_score'] = df['cleaned_content'].apply(get_sentiment_score)
    df['sentiment'] = df['sentiment_score'].apply(categorize_sentiment)

    # Create the save directory if it doesn't exist
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    # Save the cleaned data to a new CSV file in the 'dataclean' folder
    app_name = os.path.basename(file_path).replace('.csv', '')
    cleaned_file_path = os.path.join(save_dir, f"{app_name}_cleaned.csv")
    df.to_csv(cleaned_file_path, index=False)

    print(f"Cleaned data saved to {cleaned_file_path}")

app_files = ['data/amazon_alexa_google_play_reviews.csv', 'data/google_home_google_play_reviews.csv'
             , 'data/samsung_smartthings_google_play_reviews.csv']  
save_dir = 'dataclean'

for app_file in app_files:
    clean_data(app_file, save_dir)
