import pandas as pd
import matplotlib.pyplot as plt
import os

# Group data by sentiment and categorize based on the UI, Integration, and Control aspects
def aggregate_aspect(df, aspect_column):
    positive_reviews = df[(df[aspect_column] == True) & (df['sentiment'] == 'Positive')].shape[0]
    negative_reviews = df[(df[aspect_column] == True) & (df['sentiment'] == 'Negative')].shape[0]
    return positive_reviews, negative_reviews

apps = ['google_home', 'amazon_alexa', 'samsung_smartthings']
results = {}

# separate CSV files or DataFrames for each app
for app in apps:
    # You need to load each app's respective data here
    cleaned_file_path = os.path.join('dataclean', f"{app}_google_play_reviews_cleaned.csv")
    df = pd.read_csv(cleaned_file_path)  # Replace with the actual files
    results[app] = {
        'UI': aggregate_aspect(df, 'UI'),
        'Integration': aggregate_aspect(df, 'Integration'),
        'Control': aggregate_aspect(df, 'Control'),
        'Overall Positive': df[df['sentiment'] == 'Positive'].shape[0],
        'Overall Negative': df[df['sentiment'] == 'Negative'].shape[0]
    }


# 1. **Overall Experience Chart**
fig, ax = plt.subplots(figsize=(10, 6))
bar_width = 0.35
index = range(len(apps))

# Extracting the data for overall sentiment
overall_positive = [results[app]['Overall Positive'] for app in apps]
overall_negative = [results[app]['Overall Negative'] for app in apps]

# Plotting overall experience
plt.bar(index, overall_positive, bar_width, label='Positive Reviews', color='#8FB9A8')
plt.bar([i + bar_width for i in index], overall_negative, bar_width, label='Negative Reviews', color='#FF6F61')

plt.xlabel('Applications')
plt.ylabel('Number of Reviews')
plt.title('Overall Experience Comparison')
plt.xticks([i + bar_width/2 for i in index], apps)
plt.legend()
plt.savefig('plots/overall use plot.png')  # Save CDF plot
plt.show()

# 2. **Ease of Use frequency by aspects**
