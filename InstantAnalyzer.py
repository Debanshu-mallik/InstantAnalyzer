import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the read-only "../input/" directory
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
import sys
import json
#for dirname, _, filenames in os.walk('/kaggle/input'):
    #for filename in filenames:
        #print(os.path.join(dirname, filename))


# Load the dataset
df = pd.read_csv('post_data.csv', parse_dates=['Post Timestamp'])

# Specify the username of the user you want to extract data for
request_body = sys.stdin.read()
data = json.loads(request_body)
username_to_extract = data.get('username')


# Filter the DataFrame to get data for the specified user
data = df[df['Username'] == username_to_extract]

# Print the extracted data
print(data)

import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
import pandas as pd

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('vader_lexicon')

def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    tokens = word_tokenize(text)
    stop_words = set(stopwords.words('english'))
    tokens = [word for word in tokens if word not in stop_words]
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(word) for word in tokens]
    preprocessed_text = ' '.join(tokens)
    return preprocessed_text

sid = SentimentIntensityAnalyzer()

def analyze_sentiment(text):
    scores = sid.polarity_scores(text)
    if scores['compound'] >= 0.05:
        return 'Positive'
    elif scores['compound'] <= -0.05:
        return 'Negative'
    else:
        return 'Neutral'

data['sentiment'] = data['Post Content'].astype(str).apply(analyze_sentiment)

def preprocess_text(text):
    # Lowercasing
    text = text.lower()
    # Tokenization
    tokens = word_tokenize(text)
    # Removing punctuation
    tokens = [word for word in tokens if word not in string.punctuation]
    # Removing stopwords
    stop_words = set(stopwords.words('english'))
    tokens = [word for word in tokens if word not in stop_words]
    # Lemmatization
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(word) for word in tokens]
    # Joining tokens back into text
    preprocessed_text = ' '.join(tokens)
    return preprocessed_text

data['sentiment'] = data['Post Content'].astype(str).apply(analyze_sentiment)

from nltk.sentiment.vader import SentimentIntensityAnalyzer

# Initialize the VADER sentiment analyzer
sid = SentimentIntensityAnalyzer()

# Function to analyze sentiment
def analyze_sentiment(text):
    # Check if the input is a string
    if isinstance(text, str):
        scores = sid.polarity_scores(text)
        if scores['compound'] >= 0.05:
            return 'Positive'
        elif scores['compound'] <= -0.05:
            return 'Negative'
        else:
            return 'Neutral'
    else:
        return 'Neutral'

# Apply sentiment analysis to the 'caption' column
data['sentiment'] = data['Post Content'].apply(analyze_sentiment)

def preprocess_text(text):
    if isinstance(text, str):
        # Remove punctuation
        text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
        # Remove emojis
        text = text.encode('ascii', 'ignore').decode('ascii')
        # Convert text to lowercase
        text = text.lower()
        # Remove extra whitespaces
        text = re.sub('\s+', ' ', text).strip()
    return text

import re
import string

# Function to preprocess text
def preprocess_text(text):
    # Remove punctuation
    text = re.sub('[%s]' % re.escape(string.punctuation), '', str(text))
    # Remove emojis
    text = text.encode('ascii', 'ignore').decode('ascii')
    # Convert text to lowercase
    text = text.lower()
    return text

# Apply preprocessing to the 'caption' column
data['clean_caption'] = data['Post Content'].apply(preprocess_text)

from nltk.sentiment.vader import SentimentIntensityAnalyzer

# Function to analyze sentiment
def analyze_sentiment(text):
    sid = SentimentIntensityAnalyzer()
    scores = sid.polarity_scores(text)
    if scores['compound'] >= 0.05:
        return 'Positive'
    elif scores['compound'] <= -0.05:
        return 'Negative'
    else:
        return 'Neutral'

# Apply sentiment analysis to the 'clean_caption' column
data['sentiment'] = data['clean_caption'].apply(analyze_sentiment)

import matplotlib.pyplot as plt
import base64
from io import BytesIO

# Count the number of captions for each sentiment category
sentiment_counts = data['sentiment'].value_counts()

# Plot the pie chart
plt.figure(figsize=(8, 6))
plt.pie(sentiment_counts, labels=sentiment_counts.index, autopct='%1.1f%%', startangle=140)
plt.title('Sentiment Distribution of Instagram Captions')
plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
# Create a buffer to save image
buf = BytesIO()
plt.savefig(buf, format='png')
# Encode the image in base64 to embed in JSON
image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
buf.close()

"""Sentiment across different categories"""

import pandas as pd
import plotly.express as px
import plotly.io as pio

# Assuming your timestamp column is named 'created_at'
data['created_at'] = pd.to_datetime(data['Post Timestamp'])  # Convert timestamp to datetime

# Group the data by day and calculate sentiment distribution
data['date'] = data['created_at'].dt.date  # Extract date from datetime
sentiment_by_date = data.groupby(['date', 'sentiment']).size().unstack(fill_value=0)

# Convert sentiment_by_date DataFrame to long format for Plotly
sentiment_by_date_long = sentiment_by_date.reset_index().melt(id_vars='date', var_name='sentiment', value_name='count')

# Create an interactive line plot using Plotly
fig = px.line(sentiment_by_date_long, x='date', y='count', color='sentiment', title='Sentiment Trends Over Time',
              labels={'count': 'Number of Captions'})
# Convert plot to JSON
fig_json = pio.to_json(fig)

"""Reason for the sentiment"""

import pandas as pd
import plotly.express as px
import plotly.io as pio

# Assuming your timestamp column is named 'created_at'
data['created_at'] = pd.to_datetime(data['Post Timestamp'], unit='s')  # Convert timestamp to datetime

# Group the data by day and calculate sentiment distribution
data['date'] = data['created_at'].dt.date  # Extract date from datetime
sentiment_by_date = data.groupby(['date', 'sentiment']).size().unstack(fill_value=0)

# Convert sentiment_by_date DataFrame to long format for Plotly
sentiment_by_date_long_r = sentiment_by_date.reset_index().melt(id_vars='date', var_name='sentiment', value_name='count')

# Merge the caption text based on date and sentiment
sentiment_by_date_long_r = sentiment_by_date_long.merge(data[['date', 'sentiment', 'Post Content']], on=['date', 'sentiment'], how='left')

# Create hover text including caption text
sentiment_by_date_long_r['hover_text'] = sentiment_by_date_long_r.apply(lambda x: f"Date: {x['date']}<br>" \
                                                                        f"Sentiment: {x['sentiment']}<br>" \
                                                                        f"Count: {x['count']}<br>" \
                                                                        f"Caption: {x['Post Content']}",
                                                                    axis=1)

# Create an interactive line plot using Plotly
fig = px.line(sentiment_by_date_long_r, x='date', y='count', color='sentiment', title='Sentiment Trends Over Time',
              labels={'count': 'Number of Captions'}, hover_name='sentiment', hover_data={'hover_text'})
fig.update_traces(mode='markers+lines', hoverinfo='text')
# Convert plot to JSON
fig_json_2 = pio.to_json(fig)
