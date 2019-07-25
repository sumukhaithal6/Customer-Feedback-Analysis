# Customer-Feedback-Analysis
Find the most critical issues of the company by analysing reviews on TripAdvisor
A Customer Feedback Model to analyze the customer review data of a company, and help identify critical issues based on their severity and impact on customers as well as management.
Customer review data for a company is collected, classified into categories (buckets). Aspect-based sentiment/emotion analysis is performed to filter out the negative-sentiment issues; Non-granular reviews (reviews that don't give specific/detailed issues) are removed using dependency parsing, and issues are ranked based on a severity score that is generated, to finally return the top-ranked issues.

Note:

1. You will need to enter the IBM Natural Language Understanding API key in the review_categorizer.py file.
To get the API Key register at IBM Cloud and create a resource - Natural Language Understanding.The lite account gives you access to 30,000 NLU  Items per month.

2. To execute the program run python main.py with all the required arguments
 
 Example: python main.py --domain airlines --url https://www.tripadvisor.in/Airline_Review-d8729004-Reviews-Air-India --airline "Air India"
 
 If the reviews are already available in our dataset(airlines.csv) , the critical issues are displayed based on the categories in the domain
