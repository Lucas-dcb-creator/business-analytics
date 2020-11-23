#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 20 17:25:21 2020
​
@author: arianedeletang
"""
​
import requests
import bs4 
import csv
import datetime
​
​
url = input("Please provide the link of the first page of a website on TrustPilot: ")
pages_to_scrape = int(input("How many pages are there to scrape: "))
limit=datetime.date(2020,3,1)
sentiment_csv = "/Users/arianedeletang/Documents/Scolarité/HEC/M2/Business_analytics_Python/Fichiers Python/Web scrap/word_sentiment.csv"
​
def makesoup(url):
    response = requests.get(url) 
    #print('response code is: ', response.status_code)
​
    if response.status_code == 200:
        soup = bs4.BeautifulSoup(response.text, 'html.parser')
        return soup
    else:
        print('Issue getting url, Error code: ', response.status_code)
        return None
​
​
#Scrap all reviews and their date, sort them in 2 lists depending on the date (before/after March 1st)
def sort_reviews():
    review_no = 1
    page_no = 1
    scrape_url = str(url)
    review_list_before=[]
    review_list_after=[]
    review_list=[]
    while(page_no <= pages_to_scrape):
        ret_soup = makesoup(scrape_url)
        if ret_soup:   
            for rev_data in ret_soup.find_all('div', class_= 'review-content'): 
                date_init = rev_data.find('script', attrs={"data-initial-state" : "review-dates"}) 
                raw_date= "\n".join(str(date_init)).split("\n")[1:-1]
                year=''.join(raw_date[85:89])
                month=''.join(raw_date[90:92])
                day=''.join(raw_date[93:95])
                date=datetime.date(int(year),int(month),int(day))
                review = rev_data.find('p', class_ = 'review-content__text') 
                if review is None:
                    text="no text in this review"
                else:
                    text=review.text.replace('\n','')
                    text=text.replace('            ','')
                    text=text.replace('    ','')
                if date<limit:
                    review_list_before.append(text)
                else:
                    review_list_after.append(text)
                review_no += 1
        page_no += 1
        scrape_url = str(url)+'&page='+str(page_no)
    review_list.append(review_list_before)
    review_list.append(review_list_after)
    print('Total number of reviews scrapped::', review_no-1)
    print('Number of reviews before '+str(limit)+":",len(review_list_before))
    print('Number of reviews after '+str(limit)+":",len(review_list_after))
    return review_list
​
#Give a sentiment score to a word based on our csv document
def word_sentiment(word):
    sentiment_val=0
    count=0
    with open(sentiment_csv, 'rt',encoding = 'utf-8') as senti_data:
        sentiment = csv.reader(senti_data)
        for data_row in sentiment:
            count+=1
            if data_row[0] == word.lower():
                sentiment_val = data_row[1]
                return sentiment_val
            elif count==2477:
                break
        return sentiment_val
                
​
​
# Compute aggregated sentiment score of all reviews before and all reviews after March, 1st            
def main():
    sentiment_before = 0 
    sentiment_after = 0
    all_reviews=sort_reviews()
    sentence_before = ' '.join(all_reviews[0]).lower()
    words_list_before = sentence_before.split()
    sentence_after = ' '.join(all_reviews[1]).lower()
    words_list_after = sentence_after.split()
    
    for word in words_list_before:
        sentiment_before = sentiment_before + int(word_sentiment(word))
    print("The sentiment score of all the reviews before "+str(limit)+" is: ",sentiment_before)
    
    for word in words_list_after:
        sentiment_after = sentiment_after + int(word_sentiment(word))
    print("The sentiment score of all the reviews after "+str(limit)+" is: ",sentiment_after)
    
    return(sentiment_before, sentiment_after)
   
              
print(main())
