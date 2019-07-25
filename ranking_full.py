import nltk
import pandas as pd
import numpy as np
import nltk
import math
import time
import itertools
import operator
import re
#import MHR as mhr
import networkx as nx
from nltk import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from datetime import date
from nltk.corpus import brown, stopwords

def zeroFun(x): return 0

def compute_sentences_graph(sentences):
    tfidf = TfidfVectorizer().fit_transform(sentences)
    matrix_sentences = (tfidf * tfidf.T).A
    return 1 - matrix_sentences

def diff_date(d):
    today=date.today()
    di={"Jan":1,"Feb":2,"Mar":3,"Apr":4,"May":5,"Jun":6,"Jul":7,"Aug":8,"Sep":9,"Oct":10,"Nov":11,"Dec":12}
    li=d.split("-")
    that_day=date(2000+int(li[1]),di[li[0]],1)
    #print(today,that_day)
    diff=today-that_day
    return diff

def virtual_core(reviewsDf, external_freq, c, m):
    
    texts = [nltk.word_tokenize(text) for text in reviewsDf.Review]
    tokens = list(itertools.chain(*texts))
    reviews_freq = nltk.FreqDist(tokens)

    dominance = dict([])
    
    for word in dict(reviews_freq):
        if external_freq[word] > 0 and math.log(external_freq[word],2) > 0 and (word.lower() not in stopwords.words('english')) and (len(word) > 2):
            dominance[word] = reviews_freq[word] * c * ( 1 / math.log(external_freq[word],2) )
    
    
    return sorted(dominance.items(), key=operator.itemgetter(1), reverse=True)[:m]

def review_score(text, core, mean):
    core_dict = dict(core)
    review_vector = nltk.FreqDist(nltk.word_tokenize(text))
    length = len(nltk.word_tokenize(text))
    score = 0

    for word in review_vector:
        if word in core_dict:
            score += review_vector[word]

    p = 1 #punishment score
    if length < mean:
        p = 20
            
    return ((float(1) / p) * (float(score) / length)) #returns ranking score

def zeroFun(x): return 0

def rank_mrr_hotels(data):
        
    dfProducts = pd.read_csv(data)
    dfProducts['MHRs']=dfProducts.apply(zeroFun,axis=1)
    dfProducts['Index'] = range(0, len(dfProducts))
    name2="output"
    min_comments=0
    min_votes=0
    print("Ranking Issues.....")
    grouped=dfProducts.groupby('Hotel Name')
    total = len(grouped)
    run = 1
    for name, group in grouped:
        dffiltro = dfProducts['Hotel Name']==name #& (dfProducts['tot'].astype(int)>min_votes)
        comments_count = [0]*10
        #print("Run %d size %d for %d" % (run, len(comments_count), total))
        
        if ( (len(comments_count)>min_comments) ):
            sentences=[]
            
            #print ("computing")        
            for t in dfProducts[dffiltro].T.to_dict().values():
                for s in nltk.sent_tokenize(t['Review']):
                    sentences.append(s)   
                    
            sentences_graph = compute_sentences_graph(sentences)
            nx_graph = nx.from_numpy_matrix(sentences_graph)
            pg_sentences = nx.pagerank_numpy(nx_graph)
            #print(pg_sentences)
            count=0
            for t in dfProducts[dffiltro].T.to_dict().values():
                for s in nltk.sent_tokenize(t['Review']):
                    #print(t.values())
                    dfProducts.loc[list(t.values())[-1],'MHRs'] += float(pg_sentences[count])
                    count += 1

            
            #break
        run += 1

    dfProducts2 = dfProducts[(dfProducts['Sentiment']<0)]
    dfProducts2["abs_Sentiment"]=abs(dfProducts2["Sentiment"])
    dfProducts2["new_MHR"]=dfProducts2["MHRs"]/max(dfProducts2["MHRs"])

    try:
        dfProducts2["User Contribution"]=dfProducts2["User Contribution"].str.replace(",","")
    except:
        pass
    dfProducts2=dfProducts2.fillna(0)
    m=max([int(i) for i in dfProducts2["User Contribution"]])
    try:
        dfProducts2["Normalized_User_Contribution"]=[int(i)/m for i in dfProducts2["User Contribution"]]
    except:
        pass


    #print(dfProducts2["Recency"])
    dfProducts2["Recency_new"]=[diff_date(i) for i in dfProducts2["Recency"]]
    old=max(dfProducts2["Recency_new"])


    dfProducts2["Score"]=(2*dfProducts2["new_MHR"]+2*dfProducts2["sadness"]+2*dfProducts2["fear"]+3*dfProducts2["anger"]+2*dfProducts2["disgust"]+2*dfProducts2["Normalized_User_Contribution"]+0.2*(old-dfProducts2["Recency_new"])/old)
    dfProducts2.sort_values(["Hotel Name","Score"],axis=0,ascending=False,inplace=True)
    dfProducts2.to_csv(name2+".csv")
    
def rank_revrank_airlines(filename):
    MyReviews=pd.read_csv(filename)
    with open('airline_corpus.txt', 'rt') as sourceFile:
        content = sourceFile.read()
    brown_freq = nltk.FreqDist(word_tokenize(content)) #example doc for external freq
    #print(brown_freq)
    my_grouped = MyReviews.groupby('Airline')
    # evaluate virtual core function
    for name, group in my_grouped:
        ProductReview = MyReviews[MyReviews['Airline']==name]    
        review_core = virtual_core(ProductReview, brown_freq, 3, 200)
        break
    MyReviews.sort_values(["Airline", "category"], ascending=[True, True], inplace=True)
    word_c2 = []
    for i in range(MyReviews.shape[0]):
        word_c2.append(len(re.findall(r'\w+',str(MyReviews.Review[i]))))
    MyReviews["word_count"] = word_c2 
    word_c1 = []
    for i in range(ProductReview.shape[0]):
        word_c1.append(len(re.findall(r'\w+',str(ProductReview.Review[i]))))
    ProductReview["word_count"] = word_c1
    mean = ProductReview.word_count.mean()
    #print(mean)
    #print(ProductReview.Review[6])
    review_s = review_score(ProductReview.Review[6], review_core, mean)
    #print("score:",review_s)    


    total = len(my_grouped)
    run = 1
    performance=[]

    for name, group in my_grouped:
        ProductReview = MyReviews[MyReviews['Airline']==name] 
        run += 1     
        if ( len(ProductReview)>min_comments ):
        
            ProductReview['revRank'] = ProductReview.apply(zeroFun,axis=1)

            start = time.time()
            
            review_core = virtual_core(ProductReview, brown_freq, 3, 200)
            mean = ProductReview.word_count.mean()

            for t in ProductReview.T.to_dict().values():
                review_s = review_score(t['Review'], review_core, mean)
                MyReviews.loc[list(t.values())[0],'revRank'] = review_s

            end = time.time()
            elapsed = (end - start)
                
            tempo={}
            tempo['airline']=name
            tempo['no_of_reviews']= len(ProductReview)
            tempo['time']=elapsed
            performance.append(tempo)
                
            #print("Run %d size %d for %d" % (run, len(ProductReview), total))
    days = []
    for date in MyReviews['Recency_new']:
        days.append(int(date[:date.index(' ')]))
    MyReviews['days'] = days
    MyReviews['final'] = -3*MyReviews['joy'] + 1*MyReviews['sadness'] + 1*MyReviews['fear'] + 2*MyReviews['disgust'] + 2*MyReviews['anger'] + 2*MyReviews['Normalized_User_Contribution'] - 0.5*MyReviews['days']/max(MyReviews['days']) + 5*MyReviews['revRank']
    MyReviews.sort_values(["Airline", "category","final"], ascending=[True, True, False], inplace=True)
    MyReviews.to_csv('output_ranked.csv')

def rank_revrank_hotels(filename):
    MyReviews=pd.read_csv(filename)
    with open('.txt', 'rt') as sourceFile:
        content = sourceFile.read()
    brown_freq = nltk.FreqDist(word_tokenize(content)) #example doc for external freq
    my_grouped = MyReviews.groupby('Hotel Name')
    # evaluate virtual core function
    for name, group in my_grouped:
        ProductReview = MyReviews[MyReviews['Hotel Name']==name]    
        review_core = virtual_core(ProductReview, brown_freq, 3, 200)
        break
    MyReviews.sort_values(["Hotel Name", "category"], ascending=[True, True], inplace=True) 
    word_c2 = []
    for i in range(MyReviews.shape[0]):
        word_c2.append(len(re.findall(r'\w+',str(MyReviews.Review[i]))))
    MyReviews["word_count"] = word_c2
    word_c1 = []
    for i in range(ProductReview.shape[0]):
        word_c1.append(len(re.findall(r'\w+',str(ProductReview.Review[i]))))
    ProductReview["word_count"] = word_c1
    mean = ProductReview.word_count.mean()
    MyReviews['index_col'] = MyReviews.index
    total = len(my_grouped)
    run = 1
    performance=[]

    for name, group in my_grouped:
        ProductReview = MyReviews[MyReviews['Hotel Name']==name] 
        run += 1     
        if ( len(ProductReview)>min_comments ):
        
            ProductReview['revRank'] = ProductReview.apply(zeroFun,axis=1)

            start = time.time()
            
            review_core = virtual_core(ProductReview, brown_freq, 3, 200)
            mean = ProductReview.word_count.mean()

            for t in ProductReview.T.to_dict().values():
                review_s = review_score(t['Review'], review_core, mean)
                MyReviews.loc[list(t.values())[0],'revRank'] = review_s

            end = time.time()
            elapsed = (end - start)
                
            tempo={}
            tempo['hotel']=name
            tempo['no_of_reviews']= len(ProductReview)
            tempo['time']=elapsed
            performance.append(tempo)
                
    days = []
    for date in MyReviews['Recency_new']:
        days.append(int(date[:date.index(' ')]))
    MyReviews['days'] = days
    MyReviews['final'] = -3*MyReviews['joy'] + 1*MyReviews['sadness'] + 1*MyReviews['fear'] + 2*MyReviews['disgust'] + 2*MyReviews['anger'] + 2*MyReviews['Normalized_User_Contribution'] - 0.5*MyReviews['days']/max(MyReviews['days']) + 5*MyReviews['revRank']
    MyReviews.sort_values(["Hotel Name", "category","final"], ascending=[True, True, False], inplace=True) 
    MyReviews.to_csv('output_ranked.csv')    