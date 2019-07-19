from django.shortcuts import render
import pandas as pd

def fun(search_topic):
    #print(search_topic)
    f=pd.read_csv(r"/home/spielerr/django_try/customer/buckets/All_Data.csv")

    ambience=f[f['Bucket']=='ambience']
    ambience=ambience[ambience['Hotel Name']==search_topic]['Review'].head().tolist()

    food=f[f['Bucket']=='food']
    food=food[food['Hotel Name']==search_topic]['Review'].head().tolist()

    price=f[f['Bucket']=='price']
    price=price[price['Hotel Name']==search_topic]['Review'].head().tolist()
     
    amenities=f[f['Bucket']=='amenities']
    amenities=amenities[amenities['Hotel Name']==search_topic]['Review'].head().tolist()
     
    facility=f[f['Bucket']=='facility']
    facility=facility[facility['Hotel Name']==search_topic]['Review'].head().tolist()
     
    cleanliness=f[f['Bucket']=='cleanliness']
    cleanliness=cleanliness[cleanliness['Hotel Name']==search_topic]['Review'].head().tolist()
     
    staff=f[f['Bucket']=='staff']
    staff=staff[staff['Hotel Name']==search_topic]['Review'].head().tolist()

    buckets={'name':search_topic,'ambience':ambience,'food':food,'staff':staff,'amenities':amenities,'cleanliness':cleanliness,'facility':facility,'price':price}
    #print(buckets)
    return buckets


def categories(request, hotelname):
	context = dict()
	context = {
		'buc' : fun(str(hotelname))
		}
	return render(request, 'buckets/index.html', context)
	