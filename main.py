import argparse
import pandas as pd
import sys

from web_scraping import scrape
from review_categorizer import review_categorizer, review_categorizer_airline
from ranking_full import rank_revrank_airlines, rank_revrank_hotels


def capture_stdout(path='debug.log'):
    sys.stdout = open(path, 'a')


def display(name, domain):
    if domain == "hotels":
        df = pd.read_csv('All_data_b.csv')
        df_temp = df[df['Hotel Name'] == name]
        buckets = {'ambience': [], 'amenities': [], 'cleanliness': [],
                   'facility': [], 'food': [], 'price': [], 'staff': []}
    else:
        df = pd.read_csv('final_airline.csv')
        df_temp = df[df['Airline'] == name]
        buckets = {'ambience': [], 'amenities': [], 'cleanliness': [],
                   'checkin': [], 'food': [], 'price': [], 'service': []}

    for bucket in buckets:
        df_bucket = df_temp[df_temp['category'] == bucket]
        for index, row in df_bucket.iterrows():
            if len(buckets[bucket]) > 4:
                break
            buckets[bucket].append((row['Review'], row['Recency']))
    return buckets


def main():
    parser = argparse.ArgumentParser(description='Customer Feedback Model')
    parser.add_argument('--domain',
                        default="hotels", help='Domain : hotels or airlines')
    parser.add_argument('--url', required=False,
                        default=None, help='URL of site to be scraped')
    parser.add_argument('--hotel_name', default=None, help='Name of Hotel')
    parser.add_argument('--airline', default=None, help='Name of Airline')
    args = parser.parse_args()
    categories = {
        "hotels": ['Cleanliness', 'Amenities', 'Facility', 'Food', 'Staff', 'Ambience', 'Price'],
        "airlines": ['Cleanliness', 'Amenities', 'Checkin', 'Food', 'Service', 'Flight Ambience', 'Price']
    }
    if args.domain == 'hotels':
        df = pd.read_csv("All_data.csv")
        if df["Hotel Name"].str.contains(str(args.hotel_name)).any():
            print("Hotel data already scraped.")
            issues = display(args.hotel_name, args.domain)
            for i in issues:
                print("Category: ", i)
                for index, j in enumerate(issues[i]):
                    print(index+1, '. ', j[0], '\t', j[1])
        else:
            print("About to Scrape............")
            scrape(args.url, args.hotel_name, args.domain)  # Web Scraping
            print("Web Scraping Done!!")
            df = pd.read_csv('data.csv', encoding='ISO-8859-1')
            df.dropna()
            df.to_csv('data.csv')
            review_categorizer("data.csv", args.domain)
            print("Review Categorization complete")
            final_df = pd.DataFrame(columns=["Hotel Name", "Review", "Review_Lemma", "Keyword", "Sentiment",
                                             "User Contribution", "Recency", "joy", "sadness", "fear", "disgust", "anger", "category"])
            for i in categories[args.domain]:
                df = pd.read_csv(str(i)+".csv")
                df['category'] = str(i)
                final_df = final_df.append(df, sort=False)
            final_df.to_csv(args.hotel_name+".csv")
            rank_revrank_hotels(args.hotel_name+".csv")
    elif args.domain == 'airlines':
        df = pd.read_csv('airline_links.csv')
        if df["Airline"].str.contains(str(args.airline)).any():
            print("Airline data already scraped.")
            issues = display(args.airline, args.domain)
            for i in issues:
                print("Category: ", i)
                for index, j in enumerate(issues[i]):
                    print(index+1, '. ', j[0], '\t', j[1])
        else:
            print("About to Scrape............")
            scrape(args.url, args.hotel_name, args.domain)  # Web Scraping
            print("Web Scraping Done!!")
            df = pd.read_csv('data.csv', encoding='ISO-8859-1')
            df.dropna()
            df.to_csv('data.csv')
            review_categorizer_airline("data.csv", args.domain)
            print("Review Categorization complete")
            final_df = pd.DataFrame(columns=["Airline", "Review", "From", "To", "Area", "Class", "Review_Lemma", "Keyword",
                                             "Sentiment", "User Contribution", "Recency", "joy", "sadness", "fear", "disgust", "anger", "category"])
            for i in categories[args.domain]:
                df = pd.read_csv(str(i)+".csv")
                df['category'] = str(i)
                final_df = final_df.append(df, sort=False)
            final_df.to_csv(args.airline+".csv")
            rank_revrank_airlines(args.airline+".csv")


if __name__ == "__main__":
    capture_stdout()
    main()
