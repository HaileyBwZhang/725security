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
apps_xais = ['google', 'amazon', 'samsung']

results = {}
# 'Privacy', 'Security', 'Authentication', 'Vulnerability', 'Updates'
# Assume you have separate CSV files or DataFrames for each app
for app in apps:
    # You need to load each app's respective data here
    cleaned_file_path = os.path.join('dataclean', f"{app}_google_play_reviews_cleaned.csv")
    df = pd.read_csv(cleaned_file_path)  # Replace with the actual files
    results[app] = {
        'Privacy': aggregate_aspect(df, 'Privacy'),
        'Security': aggregate_aspect(df, 'Security'),
        'Authentication': aggregate_aspect(df, 'Authentication'),
        'Vulnerability': aggregate_aspect(df, 'Vulnerability'),
        'Updates': aggregate_aspect(df, 'Updates')

    }

# Now let's visualize these results
soft_colors = {
    'Positive': '#8FB9A8',  # Soft green
    'Negative': '#FF6F61',  # Soft red
}

# Create subplots (1 row, 5 columns) for UI, Integration, and Control
fig, axes = plt.subplots(1, 5, figsize=(18, 6))

bar_width = 0.3
index = np.arange(len(apps))

# Extracting the data for each aspect  'Privacy', 'Security', 'Authentication', 'Vulnerability', 'Updates'
ui_positive = [results[app]['Privacy'][0] for app in apps]
ui_negative = [results[app]['Privacy'][1] for app in apps]
integration_positive = [results[app]['Security'][0] for app in apps]
integration_negative = [results[app]['Security'][1] for app in apps]
control_positive = [results[app]['Authentication'][0] for app in apps]
control_negative = [results[app]['Authentication'][1] for app in apps]
vulner_positive = [results[app]['Vulnerability'][0] for app in apps]
vulner_negative = [results[app]['Vulnerability'][1] for app in apps]
update_positive = [results[app]['Updates'][0] for app in apps]
update_negative = [results[app]['Updates'][1] for app in apps]

# Plot for UI
axes[0].bar(index, ui_positive, bar_width, label='Positive Privacy', color=soft_colors['Positive'])
axes[0].bar(index + bar_width, ui_negative, bar_width, label='Negative Privacy', color=soft_colors['Negative'])
axes[0].set_title('Privacy Aspect Comparison')
axes[0].set_ylabel('Number of Reviews')
axes[0].set_xticks(index + bar_width / 2)
axes[0].set_xticklabels(apps_xais)
axes[0].legend()

# Plot for Integration
axes[1].bar(index, integration_positive, bar_width, label='Positive Security', color=soft_colors['Positive'])
axes[1].bar(index + bar_width, integration_negative, bar_width, label='Negative Security', color=soft_colors['Negative'])
axes[1].set_title('Security Aspect Comparison')
axes[1].set_ylabel('Number of Reviews')
axes[1].set_xticks(index + bar_width / 2)
axes[1].set_xticklabels(apps_xais)
axes[1].legend()

# Plot for Control
axes[2].bar(index, control_positive, bar_width, label='Positive Authentication', color=soft_colors['Positive'])
axes[2].bar(index + bar_width, control_negative, bar_width, label='Negative Authentication', color=soft_colors['Negative'])
axes[2].set_title('Authentication Aspect Comparison')
axes[2].set_ylabel('Number of Reviews')
axes[2].set_xticks(index + bar_width / 2)
axes[2].set_xticklabels(apps_xais)
axes[2].legend()

axes[3].bar(index, vulner_positive, bar_width, label='Positive Vulnerability', color=soft_colors['Positive'])
axes[3].bar(index + bar_width, vulner_negative, bar_width, label='Negative Vulnerability', color=soft_colors['Negative'])
axes[3].set_title('Vulnerability Aspect Comparison')
axes[3].set_ylabel('Number of Reviews')
axes[3].set_xticks(index + bar_width / 2)
axes[3].set_xticklabels(apps_xais)
axes[3].legend()

axes[4].bar(index, update_positive, bar_width, label='Positive Updates', color=soft_colors['Positive'])
axes[4].bar(index + bar_width, update_negative, bar_width, label='Negative Updates', color=soft_colors['Negative'])
axes[4].set_title('Updates Aspect Comparison')
axes[4].set_ylabel('Number of Reviews')
axes[4].set_xticks(index + bar_width / 2)
axes[4].set_xticklabels(apps_xais)
axes[4].legend()
# Adjust layout
plt.tight_layout()

plt.savefig('plots/concern detail plot.png')  # Save CDF plot

# Show the plot
plt.show()

