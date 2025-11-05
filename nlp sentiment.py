import pandas as pd
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import re

# Function for text cleaning
def clean_text(text):
    # Remove URLs, mentions, hashtags, and special characters
    text = re.sub(r'http\S+', '', text)  # Remove URLs
    text = re.sub(r'@\S+', '', text)    # Remove mentions
    text = re.sub(r'#\S+', '', text)    # Remove hashtags
    text = re.sub(r'[^A-Za-z0-9\s]', '', text)  # Remove special characters
    return text

# Initialize VADER sentiment analyzer
analyzer = SentimentIntensityAnalyzer()

# Load the Excel file
def analyze_sentiment(file_path):
    df = pd.read_excel(file_path)
    
    # Function to analyze sentiment with VADER
    def get_sentiment_vader(review):
        review = clean_text(review)  # Clean the review text
        sentiment_score = analyzer.polarity_scores(review)
        
        # Return sentiment based on VADER's compound score
        if sentiment_score['compound'] > 0.05:
            return 'Positive'
        elif sentiment_score['compound'] < -0.05:
            return 'Negative'
        else:
            return 'Neutral'

    # Apply sentiment analysis to "Post Review" column
    df['Sentiment'] = df['Post Review'].apply(get_sentiment_vader)
    
    # Save the results to a new file
    output_file = file_path.replace('.xlsx', '_with_sentiment_vader.xlsx')
    df.to_excel(output_file, index=False)
    return output_file

file_path = 'Social Media Engagement Report.xlsx'
output_file = analyze_sentiment(file_path)
print(f"Sentiment analysis completed. Results saved to {output_file}")
