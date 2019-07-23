from django.shortcuts import render
import pandas as pd

df=pd.read_csv("file:///home/spielerr/Spielerr/MIL%2019/code/Customer-Feedback-Analysis/customer/buckets/New_Data.csv")
def fun(search_topic):
    #print(search_topic)
    
    df_temp=df[df['Hotel Name']==search_topic]

    buckets={'ambience':[],'amenities':[],'cleanliness':[],'facility':[],'food':[],'price':[],'staff':[], 'name':search_topic, 'image': 'img/analysis/' + search_topic + '.jpg'}
    for bucket in buckets:
    #print(bucket)
        df_bucket=df_temp[df_temp['Bucket']==bucket]
    #print(len(df_bucket))
        ctr=1
        for index,row in df_bucket.iterrows():
            if len(buckets[bucket])>4:
                break
            buckets[bucket].append((ctr,row['Review'],row['Recency']))
            ctr+=1
    
    #buckets={'name':search_topic,'ambience':[ambience,amb_date], 'food':[food,food_date], 'staff':[staff,staff_date], 'amenities':[amenities,amen_date], 'cleanliness':[cleanliness,clean_date], 'facility':[facility,fac_date], 'price':[price, price_date]}
    return buckets


def categories(request, hotelname):
	context = dict()
	context = {
		'buc' : fun(str(hotelname))
		}
	return render(request, 'buckets/index.html', context)
	