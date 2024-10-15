import pandas as pd
import matplotlib.pyplot as plt
import os

# Group data by sentiment and categorize based on the UI, Integration, and Control aspects
def aggregate_aspect(df, aspect_column):
    positive_reviews = df[(df[aspect_column] == True) & (df['sentiment'] == 'Positive')].shape[0]
    negative_reviews = df[(df[aspect_column] == True) & (df['sentiment'] == 'Negative')].shape[0]
    return positive_reviews + negative_reviews  # Total reviews (positive + negative)

apps = ['google_home', 'amazon_alexa', 'samsung_smartthings']
results = {}

# separate CSV files or DataFrames for each app
for app in apps:
    cleaned_file_path = os.path.join('dataclean', f"{app}_google_play_reviews_cleaned.csv")
    df = pd.read_csv(cleaned_file_path)  # Replace with the actual files
    results[app] = {
        'UI': aggregate_aspect(df, 'UI'),
        'Integration': aggregate_aspect(df, 'Integration'),
        'Control': aggregate_aspect(df, 'Control')
    }

# Create the line plot
fig, ax = plt.subplots(figsize=(10, 6))
categories = ['UI', 'Integration', 'Control']

# Plotting each application's aspect data
for app in apps:
    aspect_counts = [results[app][aspect] for aspect in categories]
    ax.plot(categories, aspect_counts, marker='o', label=app)

# Customize plot
plt.xlabel('Ease of Use Aspects')
plt.ylabel('Frequency')
plt.title('Frequency of Ease of Use Aspects Across Applications')
plt.legend(title="Applications")
plt.grid(True)
plt.savefig('plots/ease_of_use_frequency_plot.png')  # Save plot
plt.show()
