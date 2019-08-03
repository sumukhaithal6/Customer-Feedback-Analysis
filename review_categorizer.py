from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_watson.natural_language_understanding_v1 import KeywordsOptions, Features, EmotionOptions
import spacy
import pandas as pd
import json
from concurrent.futures import ThreadPoolExecutor
from spacy.lemmatizer import Lemmatizer
from spacy.lang.en import LEMMA_INDEX, LEMMA_EXC, LEMMA_RULES


def which_bucket(sentence, nlp, domain):
    # SENTENCE BY SENTENCE
    if domain == 'airlines':
        buckets = {"Food": "food  drinks  meal  menu  snack ", "Price": "Expensive costly cheap money", "Cleanliness": "dirt dust stink trash cockroach maintenance", "Checkin": "Checkin  luggage  baggage  delay  boarding checkout",
                   "Service": "staff  service  lazy  air hostess  pilot  management  crew", "Flight Ambience": "Seat  legroom  noise  cooling turbulence", "Amenities": "TV  Wifi  Movie  Film  AC entertainment"}
    else:
        buckets = {"Food": "menu food dining taste lunch snack", "Staff": "service management reception staff attitude housekeeping", "Price": "costly expensive cheap money affordable price", "Cleanliness": "clean stink dirty cockroach maintenance tear tidy",
                   "Ambience": "luxury atmosphere environment ambience noise nature", "Amenities": "amenity television pool parking game entertainment furniture", "Facility": "light fan water electricity safety furniture bed"}
    max_sim = 0
    for bucket in buckets:
        sim = nlp(sentence).similarity(nlp(buckets[bucket]))
        if sim > 0.6 and sim > max_sim:
            max_sim = sim
            category = bucket
    if max_sim:
        return category
    else:
        return None


def lemmatize(sent, nlp):
    lemmatized = []
    lemmatizer = Lemmatizer(LEMMA_INDEX, LEMMA_EXC, LEMMA_RULES)
    doc = nlp(str(sent))
    for token in doc:
        i = lemmatizer(str(token), token.pos_)
        # print(i)
        lemmatized.append(i[0])
    return ' '.join(lemmatized)


def review_categorizer(filename, domain):

    nlp = spacy.load("en_core_web_lg")

    bucket = {'Cleanliness': [], 'Amenities': [], 'Facility': [],
              'Food': [], 'Staff': [], 'Ambience': [], 'Price': []}
    df1 = df2 = df3 = df4 = df5 = df6 = df7 = pd.DataFrame(
        columns=["Hotel Name", "Review", "Review_Lemma", "Keyword", "Sentiment", "User Contribution", "Recency", "joy", "sadness", "fear", "disgust", "anger"])
    connection = {'Cleanliness': df1, 'Amenities': df2, 'Facility': df3,
                  'Food': df4, 'Staff': df5, 'Ambience': df6, 'Price': df7}

    natural_language_understanding = NaturalLanguageUnderstandingV1(
        version='2018-11-16',
        iam_apikey='<enter your api key here>',
        url='https://gateway-lon.watsonplatform.net/natural-language-understanding/api')

    df = pd.read_csv(filename, encoding="ISO-8859-1")

    def extract(filename, row):
        reviews = row["Review"]
        user_contrib = row["Contribution"]
        hotel_name = row["Hotel Name"]
        recency = row["Recency"]
        for sent in nlp(str(reviews)).sents:
            sent_lemma = lemmatize(sent, nlp)
            try:
                response = natural_language_understanding.analyze(
                    text=str(sent_lemma),
                    features=Features(keywords=KeywordsOptions(sentiment=True, limit=10))).get_result()
            except Exception as e:
                # print(e,sent_lemma)
                continue
            for i in response["keywords"]:
                keyword = i["text"]
                sentiment = i["sentiment"]["score"]
                if sentiment >= 0:  # Skip sentences which have positive sentiment
                    continue
                category = which_bucket(keyword, nlp, domain)
                # and (not connection[category]["Review"].str.contains(sent).any()):
                if category:
                    response_emo = natural_language_understanding.analyze(
                        text=str(sent_lemma),
                        features=Features(emotion=EmotionOptions(targets=[keyword]))).get_result()
                    joy = response_emo["emotion"]["targets"][0]["emotion"]["joy"]
                    sadness = response_emo["emotion"]["targets"][0]["emotion"]["sadness"]
                    anger = response_emo["emotion"]["targets"][0]["emotion"]["anger"]
                    disgust = response_emo["emotion"]["targets"][0]["emotion"]["disgust"]
                    fear = response_emo["emotion"]["targets"][0]["emotion"]["fear"]
                    try:
                        connection[category] = connection[category].append({"Hotel Name": hotel_name, "Review": str(sent), "Review_Lemma": sent_lemma, "Keyword": keyword, "Sentiment": sentiment,
                                                                            "User Contribution": user_contrib, "Recency": recency, "joy": joy, "sadness": sadness, "anger": anger, "disgust": disgust, "fear": fear}, ignore_index=True)
                    except:
                        # print("Error")
                        pass

    # Multi-Threading to make it faster
    with ThreadPoolExecutor(max_workers=12) as executor:
        for index, row in df.iterrows():
            executor.submit(extract, filename, row)

    for con in connection:
        connection[con].drop_duplicates(subset="Review_Lemma",
                                        keep='first', inplace=True)
        connection[con].to_csv(str(con)+".csv")


def review_categorizer_airline(filename, domain):

    nlp = spacy.load("en_core_web_lg")
    print("Categorising reviews....")
    bucket = {'Cleanliness': [], 'Amenities': [], 'Checkin': [],
              'Food': [], 'Service': [], 'Flight Ambience': [], 'Price': []}
    df1 = df2 = df3 = df4 = df5 = df6 = df7 = pd.DataFrame(columns=["Airline", "Review", "From", "To", "Area", "Class",
                                                                    "Review_Lemma", "Keyword", "Sentiment", "User Contribution", "Recency", "joy", "sadness", "fear", "disgust", "anger"])
    connection = {'Cleanliness': df1, 'Amenities': df2, 'Checkin': df3,
                  'Food': df4, 'Service': df5, 'Flight Ambience': df6, 'Price': df7}
    natural_language_understanding = NaturalLanguageUnderstandingV1(
        version='2018-11-16',
        iam_apikey='<enter your api key here>',
        url='https://gateway-lon.watsonplatform.net/natural-language-understanding/api')

    df = pd.read_csv(filename, encoding="ISO-8859-1")

    def extract(filename, row):
        reviews = row["Review"]
        user_contrib = row["User Contribution"]
        airline_name = row["Airline"]
        recency = row["Recency"]
        for sent in nlp(str(reviews)).sents:
            sent_lemma = lemmatize(sent, nlp)
            try:
                response = natural_language_understanding.analyze(
                    text=str(sent_lemma),
                    features=Features(keywords=KeywordsOptions(sentiment=True, limit=10))).get_result()
            except Exception as e:
                # print(e,sent_lemma)
                continue
            for i in response["keywords"]:
                keyword = i["text"]
                sentiment = i["sentiment"]["score"]
                if sentiment >= 0:  # Skip sentences which have positive sentiment
                    continue
                category = which_bucket(keyword, nlp, domain)
                # and (not connection[category]["Review"].str.contains(sent).any()):
                if category:
                    response_emo = natural_language_understanding.analyze(
                        text=str(sent_lemma),
                        features=Features(emotion=EmotionOptions(targets=[keyword]))).get_result()
                    joy = response_emo["emotion"]["targets"][0]["emotion"]["joy"]
                    sadness = response_emo["emotion"]["targets"][0]["emotion"]["sadness"]
                    anger = response_emo["emotion"]["targets"][0]["emotion"]["anger"]
                    disgust = response_emo["emotion"]["targets"][0]["emotion"]["disgust"]
                    fear = response_emo["emotion"]["targets"][0]["emotion"]["fear"]
                    try:
                        connection[category] = connection[category].append({"Airline": airline_name, "Review": str(sent), "From": from_, "To": to, "Area": area, "Class": class_, "Review_Lemma": sent_lemma, "Keyword": keyword,
                                                                            "Sentiment": sentiment, "User Contribution": user_contrib, "Recency": recency, "joy": joy, "sadness": sadness, "anger": anger, "disgust": disgust, "fear": fear}, ignore_index=True)
                    except:
                        # print("Error")
                        pass

    # Multi-Threading to make it faster
    with ThreadPoolExecutor(max_workers=12) as executor:
        for index, row in df.iterrows():
            executor.submit(extract, filename, row)

    for con in connection:
        connection[con].drop_duplicates(subset="Review_Lemma",
                                        keep='first', inplace=True)
        connection[con].to_csv(str(con)+".csv")
# review_categorizer_airline("airlines.csv")
