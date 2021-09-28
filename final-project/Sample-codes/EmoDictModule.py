def create_emoj_dict(pd, defaultdict):
    # emoj_dict is a dictionary, emoji as key, array as values contains [unicode of emoji, sentiment score of emoji, description of emoji]
    emoj_dict = defaultdict(float)
    emoji_data = pd.read_csv('./data/dataset/emoji_data_1.csv')
    for i in range(len(emoji_data)):
        values = []
        unicode = emoji_data["Unicode codepoint"][i]
        sentiment_score = emoji_data["Sentiment score [-1...+1]"][i]
        description = emoji_data["Unicode name"][i]
        values.extend((unicode, sentiment_score, description))
        emoj_dict[emoji_data["Emoji"][i]] = values
    return emoj_dict

def create_emoticon_dict(pd, defaultdict):
    emoticon_dict = defaultdict(float)
    emoticon_data = pd.read_csv('./data/dataset/emoticon-emoji-mapping.csv')
    emoticon_data.drop('Unnamed: 3', inplace=True, axis=1)
    emoticon_data.drop('Unnamed: 4', inplace=True, axis=1)

    for i in range(len(emoticon_data)):
        values = []
        emoji = emoticon_data["emoji"][i]
        sentiment_score = emoticon_data["sentiment score"][i]
        values.extend((emoji, sentiment_score))
        emoticon_data["emoticon"][i] = emoticon_data["emoticon"][i].strip()
        emoticon_dict[emoticon_data["emoticon"][i]] = values
    return emoticon_dict

# return array with tweets
def change_emo_to_descrip(only_tweet_data, tokenizer, emoj_dict, emoticon_dict):
    result = []
    for tweet in only_tweet_data:
        tokens = tokenizer.tokenize(tweet)
        temp = []
        for token in tokens:
            token = emo_to_descrip(token, emoj_dict, emoticon_dict)
            temp.append(token)
        new_tweet = ' '.join(temp)
        result.append(new_tweet)
    return result

def emo_to_descrip(token, emoj_dict, emoticon_dict):
    score = 0
    if isinstance(emoj_dict[token], list):
        token = emoj_dict[token][2].lower()
    if isinstance(emoticon_dict[token], list): 
        token = emoj_dict[emoticon_dict[token][0]][2].lower()
    return token
