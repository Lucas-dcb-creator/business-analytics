# In[ ]:


import requests
import bs4 

url = "https://www.airbnb.com/experiences/1677350?currentTab=experience_tab&federatedSearchId=99f5bcea-d8eb-40bc-9798-421a39b67923&searchId=6b41c597-8221-4c8a-80ad-629609de194d&sectionId=badc9767-3385-4288-9882-09a2e2d30289&source=p2"

response = requests.get(url,headers = {'User-agent': 'Super Bot Power Level Over 9000'})

if response.status_code == 200:
    soup = bs4.BeautifulSoup(response.text)
    # we search tag <p> with attribute class 'partial_entry'
    # find the first occurrence
    review = soup.find('div', class_='_1y6fhhr')
    print(review.text)
    print("Review text printed successfully!!")
else:
    print("Issue getting url")


# In[ ]:


import requests
import bs4 

url = "https://www.airbnb.com/experiences/1677350?currentTab=experience_tab&federatedSearchId=99f5bcea-d8eb-40bc-9798-421a39b67923&searchId=6b41c597-8221-4c8a-80ad-629609de194d&sectionId=badc9767-3385-4288-9882-09a2e2d30289&source=p2"

response = requests.get(url,headers = {'User-agent': 'Super Bot Power Level Over 9000'})

print(response.status_code)

if response.status_code == 200:
    soup = bs4.BeautifulSoup(response.text, 'html.parser')
    # we search tag <p> with attribute class 'partial_entry'
    # find all occurrences
    reviews = soup.find_all('div', class_='_1y6fhhr')
    print('Number of reviews scrapped:', len(reviews))
    
    count = 1 
    for review in reviews:
        print('review number:', count)
        """ We are interested only in the review text, 
        and the review content is stored as text
        """
        print(review.text)
        print('\n')
        count += 1
else:
    print('Failed to get a response from the url. Error code: ', response.status_code)


# #### Expanding this further
# 
# To add additional details we can inspect the tags further 
# and add the review rating, review date, review title, and review content.

# In[ ]:


import requests
from bs4 import BeautifulSoup

def scrapecontent(url):
    """This function parses the HTML page representing the url using the BeautifulSoup module
    and returns the created python readable data structure (soup)"""
    scrape_response = requests.get(url) 
    print(scrape_response.status_code)

    if scrape_response.status_code == 200:
        soup = BeautifulSoup(scrape_response.text)
        return soup
    else:
        print('Error accessing url : ',scrape_response.status_code)
        return None

def main():
    # scrape_url = 'https://www.tripadvisor.com/Restaurant_Review-g187147-d1751525-Reviews-Cafe_Le_Dome-Paris_Ile_de_France.html'  
    scrape_url = "https://www.tripadvisor.com/Restaurant_Review-g227613-d3531819-Reviews-Le_Jardin_Napolitain-Jouy_en_Josas_Versailles_Yvelines_Ile_de_France.html"
    ret_soup = scrapecontent(scrape_url)
    if ret_soup:
        count = 1
        
        for rev_data in ret_soup.find_all('div', class_= 'review-container'):
            print('review number:', count)
        
            # find the review text/content
            review = rev_data.find('p', class_ = 'partial_entry') 
            print('review text:', review.text)
            
            # find the review title
            title = rev_data.find('span', class_ = 'noQuotes') 
            print('review title:', title.text)
            
            # find and print review date
            date = rev_data.find('span', class_ ='ratingDate') # Get the date if the review
            print('review date:', date.text) # find the text
            print('review date:', date['title']) # find the value of the attribute 'title'
            
            # find and print review rating
            rating = rev_data.find('span', class_='ui_bubble_rating') # Get the rating of the review
            print(rating['class'])
            print(rating['class'][0]) # 'ui_bubble_rating'
            print(rating['class'][1]) # 'bubble_50'
            print('review rating:', int(int(rating['class'][1][7:])/10))     
            
            count += 1
            print('\n')
            
main()


# ##### Excercise
# * Using sentiment analysis code that we wrote in Lab 2 and 
# * the corpus of sentiment found in the word_sentiment.csv file, calculate the sentiment of the reviews.*

# In[ ]:


import csv
import requests
import bs4 

SENTIMENT_CSV = "/Users/lix/Dropbox (HEC PARIS-)/02 Courses/Business Analytics Using Python at HEC/02 Python Basics/word_sentiment.csv"

def word_sentiment(word):
    """ This function returns the sentiment of the given word"""
    with open(SENTIMENT_CSV,'rt', encoding= 'utf-8') as csvobj:
        csvdata = csv.reader(csvobj)
        for row in csvdata:
            if row[0] == word:
                return row[1]
        return 0

def makesoup(url):
    """ This function returns the parsed soup for a given url"""
    response = requests.get(url)
    if response.status_code == 200:
        soup = bs4.BeautifulSoup(response.text)
        return soup
    else:
        print("Issue getting url")
        return None

def main(url):
    "The main function that returns the review from a website and finds the sentiment of the sentence"
    ret_soup = makesoup(url)
    count = 1 
    for rev in ret_soup.find_all('p', class_ = 'partial_entry'):
        print('review number:', count)
        t_rev = rev.text
        print(t_rev)
        count += 1
        
        sentiment_score = 0
        l_rev = t_rev.split()
        for word in l_rev:
            sentiment_score += int(word_sentiment(word))
        print('sentiment score of the review content:', sentiment_score)
        
        if sentiment_score > 0 : 
            print("positive sentiment \n")
        elif sentiment_score == 0: print("neutral sentiment \n")
        else: print("negative sentiment \n")

url = "https://www.tripadvisor.com/Restaurant_Review-g227613-d3531819-Reviews-Le_Jardin_Napolitain-Jouy_en_Josas_Versailles_Yvelines_Ile_de_France.html"

main(url)


# ##### Write the reviews and sentiment in csv
# 
# Recap of the ***with open*** command
# 
# ***with open('filename', 'mode', 'encoding') as *fileobj* ***
# 
# Where ***fileobj*** is the file object returned by open(); ***filename*** is the string name of the file. ***mode*** indicates what you want to do with the file and ***ecoding*** defines the type of encoding with which you want to open the file.
# 
# Mode could be:
# * w -> write. if the file exists it is overwritten
# * r-> read
# * **a** -> append. Write at the end of the file
# * x - > write. Only if the file does not exist. It does not allow a file to be re-written
# 
# For each, adding a subfix **t** refers to read/write as text and the subfix 'b' refers to read/write as bytes.
# 
# After opening the file, we call the **csv.writer()** function to write the data into csv.

# In[ ]:


import requests
import bs4 
import csv

def makesoup(url):
    """ This function returns the parsed soup for a given url"""
    response = requests.get(url)
    if response.status_code == 200:
        soup = bs4.BeautifulSoup(response.text)
        return soup
    else:
        print("Issue getting url")
        return None

def appendrowcsv(SENTIMENT_CSV, row):
    """ This function appends a given list to the sentiment_csv file"""
    with open(SENTIMENT_CSV, 'at', encoding = 'utf-8', newline = '') as csvobj:
        writeobj = csv.writer(csvobj)
        revcsv = writeobj.writerow(row)

def word_sentiment(SENTIMENT_CSV, word):
    """ This function returns the sentiment of the given word"""
    with open(SENTIMENT_CSV,'rt', encoding= 'utf-8') as csvobj:
        csvdata = csv.reader(csvobj)
        for row in csvdata:
            if row[0] == word:
                return row[1]
        return 0

def main(SENTIMENT_CSV, url):
    "The main function that returns the review from a website and finds the sentiment of the sentence"
    ret_soup = makesoup(url)
    row = list()
    for rev in ret_soup.find_all('p', class_ = 'partial_entry'):
        del row[:] # delete all elements in the list
        t_rev = rev.text
        row.append(t_rev)
        sentiment = 0
        l_rev = t_rev.split()
        for word in l_rev:
            sentiment = sentiment + int(word_sentiment(SENTIMENT_CSV, word))
        row.append(sentiment)
        print("print row:", row)
        print("\n")
        appendrowcsv(SENTIMENT_CSV, row)

        
url = "https://www.tripadvisor.com/Restaurant_Review-g227613-d3531819-Reviews-Le_Jardin_Napolitain-Jouy_en_Josas_Versailles_Yvelines_Ile_de_France.html"
SENTIMENT_CSV = "/Users/lix/Dropbox (HEC PARIS-)/02 Courses/Business Analytics Using Python at HEC/02 Python Basics/word_sentiment.csv"

main(SENTIMENT_CSV, url)


# ##### Enable pagination
# 
# Automatically access subsequent pages
# 1st page url: https://www.tripadvisor.com/Restaurant_Review-g187147-d1751525-Reviews-Cafe_Le_Dome-Paris_Ile_de_France.html
# 2nd page url: https://www.tripadvisor.com/Restaurant_Review-g187147-d1751525-Reviews-or10-Cafe_Le_Dome-Paris_Ile_de_France.html
# 3rd page url: https://www.tripadvisor.com/Restaurant_Review-g187147-d1751525-Reviews-or20-Cafe_Le_Dome-Paris_Ile_de_France.html

# In[ ]:

import requests
from bs4 import BeautifulSoup

def scrapecontent(url):
    """This function parses the HTML page representing the url using the BeautifulSoup module
    and returns the created python readable data structure (soup)"""
    scrape_response = requests.get(url) 
    print(scrape_response.status_code)

    if scrape_response.status_code == 200:
        soup = BeautifulSoup(scrape_response.text, 'html.parser')
        return soup
    else:
        print('Error accessing url : ',scrape_response.status_code)
        return None

def main():
    page_no = 0
    count = 1
    while(page_no < 30):
        # note the 'page_no'
        scrape_url = 'https://www.tripadvisor.com/Restaurant_Review-g187147-d1751525-Reviews-or'+str(page_no)+'-Cafe_Le_Dome-Paris_Ile_de_France.html'  
        ret_soup = scrapecontent(scrape_url)
        if ret_soup:
            for review in ret_soup.find_all('p', class_='partial_entry'): 
                print('review number:', count)
                print(review.text) #We are interested only in the text data, since the reviews are stored as text
                print("\n")
                count += 1
        page_no += 10
            
main()


# #### Expanding this further
# 
# How to get the full text of a review if the review text is long?

# https://medium.com/ymedialabs-innovation/web-scraping-using-beautiful-soup-and-selenium-for-dynamic-page-2f8ad15efe25

# IMPORTANT
# need to downloand and install 'chromedriver' from https://sites.google.com/a/chromium.org/chromedriver/home
# pay attention to the Google Chrome version when you choose to download the driver
# remember to install selenium
pip install selenium

from selenium import webdriver
import time
from bs4 import BeautifulSoup

def scrapecontent(url):
    """This function parses the HTML page representing the url using the BeautifulSoup module
    and returns the created python readable data structure (soup)"""
    # Part 1: webdriver
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--incognito')
    options.add_argument('--headless')
    WEBDRIVER_PATH = '/Users/lix/Dropbox (HEC PARIS-)/02 Courses/Business Analytics Using Python at HEC/03 Data Collection/chromedriver'
    driver = webdriver.Chrome(WEBDRIVER_PATH, chrome_options=options)

    # Part 2: click "More"
    driver.get(url)
    more_links = driver.find_elements_by_class_name("taLnk.ulBlueLinks")
    # more_links = driver.find_elements_by_xpath("//span[@class='taLnk ulBlueLinks'][contains(.,'More')]")
    
    if len(more_links)>0:
        more_links[0].click()

    # IMPORTANT: HAVE TO SLEEP TO WAIT FOR CLICKING
    time.sleep(3)

    page_source = driver.page_source
    driver.quit()

    # Part 3:
    ret_soup = BeautifulSoup(page_source)
    # ret_soup = BeautifulSoup(page_source, 'html.parser')
    return ret_soup

def main():
    scrape_url = 'https://www.tripadvisor.com/Restaurant_Review-g187147-d1751525-Reviews-Cafe_Le_Dome-Paris_Ile_de_France.html'
    
    ret_soup = scrapecontent(scrape_url)
    
    review_container = ret_soup.find_all('div', class_='review-container')
    print('number of reviews:', len(review_container))

    count = 1
    for review_data in review_container:
        print('review number:', count)
        
        # find and print review date
        date = review_data.find('span', class_ ='ratingDate') # Get the date if the review
        print('review date:', date['title']) # find the value of the attribute 'title'
    
        # find and print review rating
        rating = review_data.find('span', class_='ui_bubble_rating') # Get the rating of the review
        print('review rating:', int(int(rating['class'][1][7:])/10)) # 'bubble_20'
        
        # print review text
        review = review_data.find('p')
        print('review text:', review.text)
        print('\n')
        count += 1

main()  

# * Using the review data and the ratings available is there any way we can improve the corpus of sentiments "word_sentiment.csv" file?*

# In[ ]:

#Wher is your Test ?
