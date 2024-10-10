import pandas as pd
import matplotlib.pyplot as plt
from textblob import TextBlob

# Load your DataFrames for each application
df_google = pd.read_csv('dataclean/google_home_google_play_reviews_cleaned.csv')
df_amazon = pd.read_csv('dataclean/amazon_alexa_google_play_reviews_cleaned.csv')
df_samsung = pd.read_csv('dataclean/samsung_smartthings_google_play_reviews_cleaned.csv')

# List of DataFrames for easy iteration
dataframes = {
    'Google Home': df_google,
    'Amazon Alexa': df_amazon,
    'Samsung SmartThings': df_samsung,
}

# Initialize a dictionary to store results
security_analysis_results = {}
security_counts_dict = {}

for app_name, df in dataframes.items():
    # Calculate the frequency of security concerns for each application
    security_counts = df[['Privacy', 'Security', 'Authentication', 'Vulnerability', 'Updates']].sum()
    security_counts_dict[app_name] = security_counts

    # Check if 'cleaned_content' exists and handle sentiment calculation
    if 'cleaned_content' in df.columns:
        # Calculate sentiment scores, ensuring only strings are processed
        # df['sentiment_score'] = df['cleaned_content'].apply(lambda x: TextBlob(x).sentiment.polarity if isinstance(x, str) else None)

        # Average sentiment for security concerns
        avg_sentiment_by_security = df[['Privacy', 'Security', 'Authentication', 'Vulnerability', 'Updates']].copy()
        avg_sentiment_by_security['sentiment_score'] = df['sentiment_score']

        # Calculate average sentiment score for each category
        avg_sentiment_results = avg_sentiment_by_security.groupby(['Privacy', 'Security', 'Authentication', 'Vulnerability', 'Updates'])['sentiment_score'].mean()
        
        # Store the results in the dictionary
        security_analysis_results[app_name] = {
            'security_counts': security_counts,
            'avg_sentiment_results': avg_sentiment_results,
        }

# Convert the security counts dictionary to a DataFrame for plotting
security_counts_df = pd.DataFrame(security_counts_dict).T
security_counts_df = security_counts_df.fillna(0)  # Fill NaN with 0 if no counts

plt.figure(figsize=(12, 6))
for app_name in security_counts_df.index:
    plt.plot(security_counts_df.columns, security_counts_df.loc[app_name], marker='o', label=app_name)

plt.title('Frequency of Security Concerns Across Applications')
plt.xlabel('Security Concerns')
plt.ylabel('Frequency')
plt.xticks(rotation=45)
plt.legend(title='Applications')
plt.grid()
plt.tight_layout()  # Adjust layout
plt.savefig(f'plots/frequency of security.png')  # Save CDF plot
plt.show()

# Optionally, visualize average sentiment results for security concerns
# for app_name, results in security_analysis_results.items():
#     avg_sentiment = results['avg_sentiment_results']
    
#     plt.figure(figsize=(10, 6))
#     avg_sentiment.plot(kind='bar', color='lightgreen')
#     plt.title(f'Average Sentiment for Security Concerns - {app_name}')
#     plt.xlabel('Security Category')
#     plt.ylabel('Average Sentiment Score')
#     plt.xticks(rotation=45)
#     plt.grid(axis='y')
#     plt.show()

