import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np

# Group data by sentiment and categorize based on the UI, Integration, and Control aspects
def aggregate_aspect(df, aspect_column):
    positive_reviews = df[(df[aspect_column] == True) & (df['sentiment'] == 'Positive')].shape[0]
    negative_reviews = df[(df[aspect_column] == True) & (df['sentiment'] == 'Negative')].shape[0]
    return positive_reviews, negative_reviews

# Example aggregation for one application, repeated for others
apps = ['google_home', 'amazon_alexa', 'samsung_smartthings']
results = {}

# Assume you have separate CSV files or DataFrames for each app
for app in apps:
    # You need to load each app's respective data here
    cleaned_file_path = os.path.join('dataclean', f"{app}_google_play_reviews_cleaned.csv")
    df = pd.read_csv(cleaned_file_path)  # Replace with the actual files
    results[app] = {
        'UI': aggregate_aspect(df, 'UI'),
        'Integration': aggregate_aspect(df, 'Integration'),
        'Control': aggregate_aspect(df, 'Control')
    }

# Now let's visualize these results
soft_colors = {
    'Positive': '#8FB9A8',  # Soft green
    'Negative': '#FF6F61',  # Soft red
}

# Create subplots (1 row, 3 columns) for UI, Integration, and Control
fig, axes = plt.subplots(1, 3, figsize=(18, 6))

bar_width = 0.3
index = np.arange(len(apps))

# Extracting the data for each aspect
ui_positive = [results[app]['UI'][0] for app in apps]
ui_negative = [results[app]['UI'][1] for app in apps]
integration_positive = [results[app]['Integration'][0] for app in apps]
integration_negative = [results[app]['Integration'][1] for app in apps]
control_positive = [results[app]['Control'][0] for app in apps]
control_negative = [results[app]['Control'][1] for app in apps]

# Plot for UI
axes[0].bar(index, ui_positive, bar_width, label='Positive UI', color=soft_colors['Positive'])
axes[0].bar(index + bar_width, ui_negative, bar_width, label='Negative UI', color=soft_colors['Negative'])
axes[0].set_title('UI Aspect Comparison')
axes[0].set_ylabel('Number of Reviews')
axes[0].set_xticks(index + bar_width / 2)
axes[0].set_xticklabels(apps)
axes[0].legend()

# Plot for Integration
axes[1].bar(index, integration_positive, bar_width, label='Positive Integration', color=soft_colors['Positive'])
axes[1].bar(index + bar_width, integration_negative, bar_width, label='Negative Integration', color=soft_colors['Negative'])
axes[1].set_title('Integration Aspect Comparison')
axes[1].set_ylabel('Number of Reviews')
axes[1].set_xticks(index + bar_width / 2)
axes[1].set_xticklabels(apps)
axes[1].legend()

# Plot for Control
axes[2].bar(index, control_positive, bar_width, label='Positive Control', color=soft_colors['Positive'])
axes[2].bar(index + bar_width, control_negative, bar_width, label='Negative Control', color=soft_colors['Negative'])
axes[2].set_title('Control Aspect Comparison')
axes[2].set_ylabel('Number of Reviews')
axes[2].set_xticks(index + bar_width / 2)
axes[2].set_xticklabels(apps)
axes[2].legend()


# Adjust layout
plt.tight_layout()

plt.savefig('plots/use detail plot.png')  # Save CDF plot

# Show the plot
plt.show()

