import csv

from selenium import webdriver
from datetime import date
from datetime import datetime, timedelta


def date_finder(st):
    month = {"Jan": "01", "Feb": "02", "Mar": "03", "Apr": "04", "May": "05", "Jun": "06",
             "Jul": "07", "Aug": "08", "Sep": "09", "Oct": "10", "Nov": "11", "Dec": "12"}
    ind = st.index('review')
    dat = st[ind+7:]
    today = date.today()
    year = str(today)[:4]
    if dat == "Yesterday":
        yesterday = str(today - timedelta(days=1))
        return str(yesterday[5:7])+"-"+str(yesterday[:4])
    elif dat == "Today":
        return str(today)[5:7]+"-"+str(today)[:4]
    elif year in dat or str((int)(year)-1) in dat or str((int)(year)-2) in dat:
        try:
            return month[dat[:3]]+"-"+dat[4:]
        except:
            return None
    elif dat[dat.index(' ')+1:] in month.keys():
        sp_ind = dat.index(' ')
        return month[dat[sp_ind+1:]]+"-"+year
    else:
        return None


def scrape(url, hotel_name, domain='hotels'):

    chromeOptions = webdriver.ChromeOptions()
    prefs = {'profile.managed_default_content_settings.images': 2,  # does not load images on web page
             'disk-cache-size': 1024}  # use disk cache to reduce page load time
    chromeOptions.add_experimental_option("prefs", prefs)
    chromeOptions.add_argument('--headless')
    chromeOptions.add_argument('--incognito')
    driver = webdriver.Chrome(
        "chromedriver.exe", options=chromeOptions)#path to chromedriver
    temp = []
    page = 0
    driver.get(url)
    print("Loading URL")
    with open('data.csv', mode='a+') as file:
        writer = csv.writer(file, delimiter=',',
                            quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(["Hotel Name", "Review Title", "Review",
                         "Rating", "Recency", "Contribution"])
    try:
        last_page_temp = driver.find_elements_by_css_selector(
            ".separator+ .pageNum")
        last_page = int(last_page_temp[0].text)
    except:
        last_page = 0
    print("Number of pages:", last_page)
    while (page < (last_page-2)*5):

        for i in range(5):
            try:
                driver.find_elements_by_class_name(
                    "hotels-review-list-parts-ExpandableReview__cta--3U9OU")[i].click()
            except:
                pass

        user_cont_temp = driver.find_elements_by_css_selector(
            ".social-member-MemberHeaderStats__stat_item--34E1r:nth-child(1) span , .social-member-MemberHeaderStats__hometown_stat_item--231iN+ .social-member-MemberHeaderStats__stat_item--34E1r span , .separator+ .pageNum")
        user_cont = []
        for i in range(1, 10, 2):
            try:
                user_cont.append(user_cont_temp[i].text)
            except:
                pass

            # Hotel name : i[0] the i from the outermost for loop

        try:
            reviews = driver.find_elements_by_class_name(
                "hotels-review-list-parts-ExpandableReview__reviewText--3oMkH")
            titles = driver.find_elements_by_class_name(
                "hotels-review-list-parts-ReviewTitle__reviewTitleText--3QrTy")
            ratings_temp = driver.find_elements_by_class_name(
                "hotels-review-list-parts-RatingLine__bubbles--1oCI4")
            date_review_temp = driver.find_elements_by_css_selector(
                ".social-member-event-MemberEventOnObjectBlock__event_type--3njyv span")
        except:
            pass

        ratings = []
        for i in range(5):
            try:
                ratings.append(str(int(ratings_temp[i].find_elements_by_tag_name(
                    "span")[0].get_attribute("class")[-2:])/10))
            except:
                pass

        dates = []
        for i in range(5):
            if(date_finder(str(date_review_temp[i].text))):
                dates.append(date_finder(str(date_review_temp[i].text)))

        if(len(dates) == 5):
            page += 5
            a = url
            b = a[:a.find("Reviews")+len("Reviews")+1]
            next_page = b + "or" + str(page) + "-" + a[len(b):]

            if (len(reviews) == 5):
                with open('data.csv', mode='a+') as file:
                    writer = csv.writer(
                        file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                    #writer.writerow(["Hotel name","Review Titles","Reviews","User Rating", "User Contribution(Review wise)"])
                    for i in range(5):
                        try:
                            writer.writerow(
                                [hotel_name, titles[i].text, reviews[i].text, ratings[i], dates[i], user_cont[i]])
                        except:
                            pass
            driver.get(next_page)
        else:
            break


def scrape_airlines(url, airline, domain='airlines'):

    chromeOptions = webdriver.ChromeOptions()
    prefs = {'profile.managed_default_content_settings.images': 2,  # does not load images on web page
             'disk-cache-size': 1024}  # use disk cache to reduce page load time
    chromeOptions.add_experimental_option("prefs", prefs)
    chromeOptions.add_argument('--headless')
    chromeOptions.add_argument('--incognito')
    #driver = webdriver.Chrome(options=chromeOptions)
    driver = webdriver.Chrome(
        "chromedriver.exe", options=chromeOptions)#enter path to chromedriver

    page = 0
    driver.get(url)
    try:
        last_page_temp = driver.find_elements_by_css_selector(
            ".separator+ .pageNum")
        last_page = int(last_page_temp[0].text)
        print(last_page, "\n")
    except:
        last_page = 0
        # Lufthansa 800
        # Air India 700
        # Spicejet 340
    while (page < (last_page-2)*5):
        print("\nInside Page", page)
        for i in range(5):
            try:
                driver.find_elements_by_class_name(
                    "location-review-review-list-parts-ExpandableReview__cta--2mR2g")[i].click()
                print("Read more clicked")
            except:
                pass

        user_cont_temp = driver.find_elements_by_css_selector(
            ".social-member-MemberHeaderStats__hometown_stat_item--231iN+ .social-member-MemberHeaderStats__stat_item--34E1r span , .social-member-MemberHeaderStats__stat_item--34E1r:nth-child(1) span")
        user_cont = []
        for i in range(1, 10, 2):
            try:
                user_cont.append(user_cont_temp[i].text)
            except:
                pass
        print("page", page, user_cont)
        # Hotel name : i[0] the i from the outermost for loop

        try:
            reviews = driver.find_elements_by_class_name(
                "location-review-review-list-parts-ExpandableReview__reviewText--gOmRC")
            titles = driver.find_elements_by_class_name(
                "location-review-review-list-parts-ReviewTitle__reviewTitle--2GO9Z")
            ratings_temp = driver.find_elements_by_class_name(
                "location-review-review-list-parts-RatingLine__bubbles--GcJvM")
            date_temp = driver.find_elements_by_css_selector(
                ".social-member-event-MemberEventOnObjectBlock__event_type--3njyv span")
            details_temp1 = driver.find_elements_by_class_name(
                "location-review-review-list-parts-RatingLine__labelBtn--e58BL")
        except:
            pass
        print("reviews len", len(reviews), "\ntitles len",
              len(titles), "\ndate temp len", len(date_temp))

        ratings = []
        for i in range(5):
            try:
                ratings.append(str(int(ratings_temp[i].find_elements_by_tag_name(
                    "span")[0].get_attribute("class")[-2:])/10))
            except:
                pass
        print("ratings", ratings)
        dates = []
        for i in range(5):
            try:
                if(date_finder(str(date_temp[i].text))):
                    dates.append(date_finder(str(date_temp[i].text)))
            except:
                pass
        print("dates", dates)

        details_temp = []
        for i in details_temp1:
            try:
                details_temp.append(i.text)
            except:
                pass
        dept = []
        dest = []
        flight_class = []
        area = []
        for i in range(0, len(details_temp), 3):
            try:
                dept.append(details_temp[i][:details_temp[i].index('-')-1])
                dest.append(details_temp[i][details_temp[i].index('-')+2:])
                area.append(details_temp[i+1])
                flight_class.append(details_temp[i+2])
            except:
                pass
        print("departure", dept, "\nDestination", dest,
              "\nArea", area, "\nClass", flight_class)

        page += 5
        a = url
        b = a[:a.find("Reviews")+len("Reviews")+1]
        next_page = b + "or" + str(page) + "-" + a[len(b):]

        if (len(reviews) == 5):
            count = 0
            with open('Indigo_final.csv', mode='a+') as file:
                writer = csv.writer(file, delimiter=',',
                                    quotechar='"', quoting=csv.QUOTE_MINIMAL)
                for i in range(5):
                    try:
                        writer.writerow([airline, titles[i].text, reviews[i].text, ratings[i],
                                         dates[i], user_cont[i], dept[i], dest[i], area[i], flight_class[i]])
                        count += 1
                        print(count, "done")
                    except:
                        pass
        driver.get(next_page)
