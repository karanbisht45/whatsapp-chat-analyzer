from urlextract import URLExtract
#from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import re
import emoji

extract = URLExtract()


def fetch_stats(selected_user,df):
    if selected_user == 'overall':
        # fetching number of messages
        num_messages = df.shape[0]

        #fetching words
        words = []
        for message in df['message']:
            words.extend(message.split())

        #fetching media
        #na=False ensures that NaN values in the column are ignored, avoiding potential errors if there are any missing messages.
        num_media = df[df['message'].str.contains('<Media omitted>', na=False)].shape[0]

        #fetching links
        links = []
        for message in df['message']:
            links.extend(extract.find_urls(message))

        return num_messages,len(words),num_media,len(links)
    else:
        new_df = df[df['user']==selected_user]
        num_messages = new_df.shape[0]

        words = []
        for message in new_df['message']:
            words.extend(message.split())

        num_media = new_df[new_df['message'].str.contains('<Media omitted>', na=False)].shape[0]

        links = []
        for message in new_df['message']:
            links.extend(extract.find_urls(message))

        return num_messages, len(words), num_media, len(links)

def monthly_timeline(selected_user,df):
    if selected_user != 'overall':
       df = df[df['user']==selected_user]

    timeline = df.groupby(['year','month_num','month']).count()['message'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))

    timeline['time'] = time

    return timeline

def daily_timeline(selected_user,df):
    if selected_user != 'overall':
       df = df[df['user']==selected_user]

    daily_timeline = df.groupby('only_date').count()['message'].reset_index()

    return daily_timeline

def week_activity_map(selected_user,df):
    if selected_user != 'overall':
       df = df[df['user']==selected_user]

    return df['day_name'].value_counts()

def month_activity_map(selected_user,df):
    if selected_user != 'overall':
        df = df[df['user'] == selected_user]

    return df['month'].value_counts()

def most_busy_users(df):
    x=df['user'].value_counts().head()
    df=round((df['user'].value_counts()/df.shape[0])*100,2).reset_index().rename(columns={'count':'percent','user':'name'})
    return x,df

#def create_wordcloud(selected_user,df):
    #if selected_user != 'overall':
       #df = df[df['user']==selected_user]

    #wc = WordCloud(width=500, height=500, min_font_size=10,background_color='white')
    #df_wc = wc.generate(df['message'].str.cat(sep=" "))
    #return df_wc


def most_common_words(selected_user, df):
    with open('stop_hinglish.txt', 'r') as f:
        stop_words = f.read().splitlines()

    if selected_user != 'overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[~temp['message'].str.contains('<Media omitted>')]

    words = []

    # Emoji pattern to remove emojis
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               u"\U00002702-\U000027B0"
                               u"\U000024C2-\U0001F251"
                               "]+", flags=re.UNICODE)

    for message in temp['message']:
        # Remove emojis from message
        message = emoji_pattern.sub(r'', message)

        # Split words and filter out stop words
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    return pd.DataFrame(Counter(words).most_common(20))

def emoji_helper(selected_user, df):
    if selected_user != 'overall':
        df = df[df['user'] == selected_user]

    emojis = []

    for message in df['message']:
        emojis.extend([c for c in message if emoji.is_emoji(c)])

    emoji_counts = Counter(emojis)
    emoji_df = pd.DataFrame(emoji_counts.most_common(), columns=['emoji', 'count'])

    return emoji_df


