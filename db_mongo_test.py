import re

from bs4 import BeautifulSoup

from pprint import pprint

from selenium import webdriver

import pymongo

# Connect to MongoDB (replace these values with your actual MongoDB connection details)
client = pymongo.MongoClient("mongodb+srv://camyacodes:qqp7qWEtiPZBW3vw@egot.qbuwfik.mongodb.net/")
valid_database_name = "NIQUES_EATS"

database = client[valid_database_name]
collection = database["EGOT"]


# Your HTML content (replace this with your actual HTML)
with open("1st_annual.html") as file:
    page_content = file.read()

# Parse the HTML content
soup = BeautifulSoup(page_content, 'html.parser')

# Extract links
# base_url = "https://www.grammy.com"  # Replace with your actual base URL
# url_lists = [base_url + link['href'] for link in soup.find_all('a', href=True)]

# Print the extracted links
# for link in links:
#     print(link)



# Set up Selenium WebDriver (make sure you have the appropriate WebDriver for your browser)
# driver = webdriver.Chrome()  # You can change this to Firefox or other supported browsers

# for url in url_list:
#     # Use Selenium to get the HTML content
#     driver.get(url)
# contents = driver.page_source

    # Use BeautifulSoup for parsing the HTML
# soup = BeautifulSoup(page_content, 'html.parser')

    # Your existing code for scraping data from each page goes here
year = 1   
# sections = soup.find_all('section')
year_data = {'Year': year, 'categories': []}

parent_sections = soup.find_all('section', class_='h-full w-full flex flex-col items-center mt-6 md-xl:mt-8')

for parent in parent_sections:


    child_section = parent.find('section')

    category_div = child_section.find('div', class_='w-full text-left md-xl:text-right mb-1 md-xl:mb-20px text-14 md-xl:text-22 font-polaris uppercase')
    unformatted_category_text = category_div.text.strip().replace('\n', '')
    category = re.sub(' +', ' ', unformatted_category_text)
    # print(category)

    winner_work_div = child_section.find('div', class_='w-full text-center md-xl:text-left text-17 md-xl:text-22 mr-10px md-xl:mr-30px font-polaris font-bold md-xl:leading-8 tracking-wider')
    winner_work = winner_work_div.text.strip()
    # print(winner_work)

    if (winner_div := child_section.find('div', class_='awards-category-link')) is not None:
        unformatted_winner_text = winner_div.text.strip().replace('\n', '')
        winner = re.sub(' +', ' ', unformatted_winner_text)
    elif (winner_div := child_section.find('div', class_='w-full text-left text-14 font-polaris md-xl:leading-normal')) is not None:
        unformatted_winner_text = winner_div.text.strip().replace('\n', '')
        winner = re.sub(' +', ' ', unformatted_winner_text)
    elif winner_div is None:
        winner = "Null"



    
    # Extract the nominees
    # nominee_arr = child_section.find_all('div', class_='awards-nominees-link')
    nominee_sections = child_section.find_all('div', class_='accordion__section')
    nominees = []
    
    for section in nominee_sections:
        unformatted_nominee_work = section.find('span').text.strip().replace('\n', '')
        nominee_work = re.sub(' +', ' ', unformatted_nominee_work)

        # unformatted_nominee_artist = section.find('div', class_='awards-nominees-link').text.strip().replace('\n', '')
        # if unformatted_nominee_artist:
        #     nominee_artist = re.sub(' +', ' ', unformatted_nominee_artist)
        # elif (unformatted_nominee_artist := section.find('div', class_='accordion__content').text.strip().replace('\n', '')):
        #     unformatted_nominee_artist = section.find('div', class_='accordion__content').text.strip().replace('\n', '')
        #     nominee_artist = re.sub(' +', ' ', unformatted_nominee_artist)
        # elif unformatted_nominee_artist is None: 
        #     nominee_artist = "Null"

        # nominee_data = {'artist': nominee_artist, 'work': nominee_work}
        # nominees.append(nominee_data)
        nominee_artist_element = section.find('div', class_='awards-nominees-link')
        # print(nominee_artist_element)
        if nominee_artist_element and not nominee_artist_element.text:
            # If artist information is not in 'awards-nominees-link', check 'accordion__content'
            accordion_content_element = section.find('div', class_='accordion__content')
            # print(accordion_content_element)
            unformatted_nominee_artist = accordion_content_element.text.strip().replace('\n', '') if accordion_content_element else None
        elif nominee_artist_element:
            unformatted_nominee_artist = nominee_artist_element.text.strip().replace('\n', '')

        nominee_artist = re.sub(' +', ' ', unformatted_nominee_artist) if unformatted_nominee_artist else "Null"

        nominee_data = {'artist': nominee_artist, 'work': nominee_work}
        nominees.append(nominee_data)

    category_data = {
    'category': category,
    'nominees': nominees,
    'winner': {'artist': winner, 'work': winner_work}
    }

    year_data['categories'].append(category_data)

collection.insert_one(year_data)


client.close()


    # api_format = {
    # 'Year': year, 
    #     'category': category,
    #     'nominees': nominees,
    #     'winner': {'artist': winner, 'work': winner_work}
    #  }


    # pprint(api_format)
    # pprint(year_data)

    # Close the current tab (optional, depending on your use case)
    # driver.execute_script("window.close();")

# Quit the Selenium WebDriver
# driver.quit()


