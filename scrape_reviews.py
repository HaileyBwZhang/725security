from google_play_scraper import Sort, reviews
import pandas as pd

# Define the app package name from Google Play
app_packages = {
    "google_home": "com.google.android.apps.chromecast.app",
    "amazon_alexa": "com.amazon.dee.app",
    "samsung_smartthings": "com.samsung.android.oneconnect",
    # Add more apps as needed
}

# Function to scrape reviews
def scrape_google_play_reviews(app_package, num_reviews=3000):
    all_reviews = []
    result, continuation_token = reviews(
        app_package,
        lang='en',  # Language of the reviews
        country='us',  # Country of the reviews
        sort=Sort.NEWEST,  # Sort by newest
        count=num_reviews,  # Number of reviews to scrape
    )
    all_reviews.extend(result)
    
    # Convert to DataFrame
    df = pd.DataFrame(all_reviews)
    df = df[['content', 'score', 'thumbsUpCount', 'at', 'replyContent']]  # Selecting important fields
    return df

# Scraping Google Play reviews for each app
for app, package in app_packages.items():
    print(f"Scraping reviews for {app}...")
    df_reviews = scrape_google_play_reviews(package)
    df_reviews.to_csv(f"{app}_google_play_reviews.csv", index=False)  # Save reviews to CSV
    print(f"Saved {len(df_reviews)} reviews for {app}.")
