import matplotlib.pyplot as plt
import pandas as pd

# Function to count positive and negative reviews per security concern
def count_reviews(df):
    security_concerns = ['Privacy', 'Security', 'Authentication', 'Vulnerability', 'Updates']
    
    combined_data = {
        'Concern': [],
        'Aspect': [],
        'Positive Count': [],
        'Negative Count': []
    }
    
    for aspect in ['UI', 'Integration', 'Control']:
        for concern in security_concerns:
            positive_count = df[(df[aspect] == True) & (df[concern] == True) & (df['sentiment'] == 'Positive')].shape[0]
            negative_count = df[(df[aspect] == True) & (df[concern] == True) & (df['sentiment'] == 'Negative')].shape[0]
            
            combined_data['Concern'].append(concern)
            combined_data['Aspect'].append(aspect)
            combined_data['Positive Count'].append(positive_count)
            combined_data['Negative Count'].append(negative_count)
    
    return pd.DataFrame(combined_data)

# Assuming you have three dataframes: df_app1, df_app2, df_app3
df_google = pd.read_csv('dataclean/google_home_google_play_reviews_cleaned.csv')
df_amazon = pd.read_csv('dataclean/amazon_alexa_google_play_reviews_cleaned.csv')
df_samsung = pd.read_csv('dataclean/samsung_smartthings_google_play_reviews_cleaned.csv')

# Combine the results
combined_df_app1 = count_reviews(df_google)
combined_df_app2 = count_reviews(df_amazon)
combined_df_app3 = count_reviews(df_samsung)

# Combine all applications into one DataFrame
combined_df = pd.concat([combined_df_app1.assign(Application='Google'),
                         combined_df_app2.assign(Application='Amazon'),
                         combined_df_app3.assign(Application='Samsung')])

# Plotting
fig, axes = plt.subplots(1, 3, figsize=(24, 8), sharey=True)

for ax, aspect in zip(axes, ['UI', 'Integration', 'Control']):
    subset = combined_df[combined_df['Aspect'] == aspect]
    width = 0.35  # Bar width

    # Create a bar plot for positive and negative counts
    for i, app in enumerate(['Google', 'Amazon', 'Samsung']):
        data = subset[subset['Application'] == app]
        ax.bar(data['Concern'] + f' ({app})', data['Positive Count'], width, label=f'{app} Positive', alpha=0.7)
        ax.bar(data['Concern'] + f' ({app})', -data['Negative Count'], width, label=f'{app} Negative', alpha=0.7)

    ax.set_title(aspect)
    ax.set_ylabel('Count')
    ax.set_xticklabels(subset['Concern'], rotation=45)
    ax.axhline(0, color='black', linewidth=0.8)  # Add a line at y=0

# Set x-ticks
#ax.set_xticklabels(subset['Concern'], rotation=45)
ax.legend(loc='upper right')

plt.tight_layout()
plt.savefig('plots/aspects vs concerns.png')  # Save CDF plot
plt.show()
