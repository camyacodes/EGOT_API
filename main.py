import re

from bs4 import BeautifulSoup

from pprint import pprint

from selenium import webdriver

# Your HTML content (replace this with your actual HTML)
with open("links.html") as file:
    links_content = file.read()

# Parse the HTML content
soup = BeautifulSoup(links_content, 'html.parser')

# Extract links
base_url = "https://www.grammy.com"  # Replace with your actual base URL
links = [base_url + link['href'] for link in soup.find_all('a', href=True)]

# Print the extracted links
for link in links:
    print(link)



# Set up Selenium WebDriver (make sure you have the appropriate WebDriver for your browser)
driver = webdriver.Chrome()  # You can change this to Firefox or other supported browsers

for url in url_list:
    # Use Selenium to get the HTML content
    driver.get(url)
    contents = driver.page_source

    # Use BeautifulSoup for parsing the HTML
    soup = BeautifulSoup(contents, 'html.parser')

    # Your existing code for scraping data from each page goes here
    
# sections = soup.find_all('section')
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

    api_format = {
    'category': category,
    'nominees': nominees,
    'winner': {'artist': winner, 'work': winner_work}
    }

    # pprint(api_format)

    # Close the current tab (optional, depending on your use case)
    driver.execute_script("window.close();")

# Quit the Selenium WebDriver
driver.quit()


# with open("2nd_annual.html") as file:
#     contents = file.read()

# soup = BeautifulSoup(contents, 'html.parser')

# # sections = soup.find_all('section')
# parent_sections = soup.find_all('section', class_='h-full w-full flex flex-col items-center mt-6 md-xl:mt-8')

# for parent in parent_sections:

#     child_section = parent.find('section')

#     category_div = child_section.find('div', class_='w-full text-left md-xl:text-right mb-1 md-xl:mb-20px text-14 md-xl:text-22 font-polaris uppercase')
#     unformatted_category_text = category_div.text.strip().replace('\n', '')
#     category = re.sub(' +', ' ', unformatted_category_text)
#     # print(category)

#     winner_work_div = child_section.find('div', class_='w-full text-center md-xl:text-left text-17 md-xl:text-22 mr-10px md-xl:mr-30px font-polaris font-bold md-xl:leading-8 tracking-wider')
#     winner_work = winner_work_div.text.strip()
#     # print(winner_work)

#     if (winner_div := child_section.find('div', class_='awards-category-link')) is not None:
#         unformatted_winner_text = winner_div.text.strip().replace('\n', '')
#         winner = re.sub(' +', ' ', unformatted_winner_text)
#     elif (winner_div := child_section.find('div', class_='w-full text-left text-14 font-polaris md-xl:leading-normal')) is not None:
#         unformatted_winner_text = winner_div.text.strip().replace('\n', '')
#         winner = re.sub(' +', ' ', unformatted_winner_text)
#     elif winner_div is None:
#         winner = "Null"



    
#     # Extract the nominees
#     # nominee_arr = child_section.find_all('div', class_='awards-nominees-link')
#     nominee_sections = child_section.find_all('div', class_='accordion__section')
#     nominees = []
    
#     for section in nominee_sections:
#         unformatted_nominee_work = section.find('span').text.strip().replace('\n', '')
#         nominee_work = re.sub(' +', ' ', unformatted_nominee_work)

#         # unformatted_nominee_artist = section.find('div', class_='awards-nominees-link').text.strip().replace('\n', '')
#         # if unformatted_nominee_artist:
#         #     nominee_artist = re.sub(' +', ' ', unformatted_nominee_artist)
#         # elif (unformatted_nominee_artist := section.find('div', class_='accordion__content').text.strip().replace('\n', '')):
#         #     unformatted_nominee_artist = section.find('div', class_='accordion__content').text.strip().replace('\n', '')
#         #     nominee_artist = re.sub(' +', ' ', unformatted_nominee_artist)
#         # elif unformatted_nominee_artist is None: 
#         #     nominee_artist = "Null"

#         # nominee_data = {'artist': nominee_artist, 'work': nominee_work}
#         # nominees.append(nominee_data)
#         nominee_artist_element = section.find('div', class_='awards-nominees-link')
#         # print(nominee_artist_element)
#         if nominee_artist_element and not nominee_artist_element.text:
#             # If artist information is not in 'awards-nominees-link', check 'accordion__content'
#             accordion_content_element = section.find('div', class_='accordion__content')
#             # print(accordion_content_element)
#             unformatted_nominee_artist = accordion_content_element.text.strip().replace('\n', '') if accordion_content_element else None
#         elif nominee_artist_element:
#             unformatted_nominee_artist = nominee_artist_element.text.strip().replace('\n', '')

#         nominee_artist = re.sub(' +', ' ', unformatted_nominee_artist) if unformatted_nominee_artist else "Null"

#         nominee_data = {'artist': nominee_artist, 'work': nominee_work}
#         nominees.append(nominee_data)

#     api_format = {
#     'category': category,
#     'nominees': nominees,
#     'winner': {'artist': winner, 'work': winner_work}
#     }

#     pprint(api_format)



            

        
        
    # nominee_work = re.sub(' +', ' ', nominee_sections.find('span').text.strip().replace('\n', ''))


    # nominee_artist = re.sub(' +', ' ', nominee_sections.find('div', class_='awards-nominees-link').text.strip().replace('\n', ''))
    # if nominee_artist is None:
    #     nominee_artist = re.sub(' +', ' ', nominee_sections.find('p', class_='pt-8 pb-4"').text.strip().replace('\n', ''))
   

    # print({nominee_artist : nominee_work})


    
    # nominee_names = [name.text.strip() for name in nominee_arr]
    # unformatted_nominee_works = [work.find('span').text.strip().replace('\n', '') for work in nominee_work_arr]
    # nominee_works = [re.sub(' +', ' ', work) for work in unformatted_nominee_works]
    
    # nominees = dict(zip(nominee_names, nominee_works))

    # api_format = {
    # 'category': category,
    # 'nominees': nominees,
    # 'winner': {winner: winner_work}
    # }

    # pprint(api_format)








# section_ids = [section['id'] for section in parent_sections if section.get('id') is not None]
# print(section_ids)

# unique_categories = []
# winners = {}


#LOOP THROUGH EACH SECTION
# for each_section in section_ids:
#     section_html = soup.find_all('section', id=each_section)
#
#     for each_section_html in section_html:
#
#         category = each_section_html.find('div', class_='w-full text-left md-xl:text-right mb-1 md-xl:mb-20px text-14 md-xl:text-22 font-polaris uppercase')
#         unformatted_category_text = category.text.strip().replace('\n', '')
#         category_text = re.sub(' +', ' ', unformatted_category_text)
#         if category_text not in unique_categories:
#             unique_categories.append(category_text)
#
#
#         winner_name = (each_section_html.find('div', class_='awards-category-link'))
#         # if winner_name is not None:
#                        # .find('p').get_text(strip=True))
#             # print(winner_name.find('p').get_text(strip=True))
#
#
#         winner_work = each_section_html.find('div', class_='w-full text-center md-xl:text-left text-17 md-xl:text-22 mr-10px md-xl:mr-30px font-polaris font-bold md-xl:leading-8 tracking-wider')
#
#         if winner_work is not None:
#             winner_work.find('p').get_text(strip=True)
            # print(winner_work.find('p').get_text(strip=True))
# print(unique_categories)


# Find the section with id="627"
# section_627 = soup.find('section', id='627')


# # Extract the category name
# category = section_627.find('div', class_='text-14').text.strip()
# # Extract the winner
# winner_work = section_627.find('div', class_='text-17').text.strip()
# winner_name = section_627.find('div', class_='awards-category-link').find('a').text.strip()
#
#
# # Extract the nominees
# nominee_arr = section_627.find_all('div', class_='awards-nominees-link')
# nominee_work_arr = section_627.find_all('button', class_='accordion')
#
# nominee_names = [name.text.strip() for name in nominee_arr]
# nominee_works = [work.find('span').text.strip() for work in nominee_work_arr]
#
#
# nominees = dict(zip(nominee_names, nominee_works))
#
# api_format = {
#     'category': category,
#     'nominees': dict(zip(nominee_names, nominee_works)),
#     'winner': {winner_name: winner_work}
# }

# print(api_format)


# for work in nominee_work_arr:
#     nominee_work = work.find('span').text.strip()
#     print(nominee_work)

# for work in nominee_work_arr:


# for nominee in nominee_arr:
#     nominee_name = nominee.text.strip()
#     print(nominee_name)

# nominees_input = section_627.find('input', class_='nominees-input')
# nominee_elements = nominees_input.find_all_next('div', class_='pt-15px')
#
# nominees = {}
# for nominee_element in nominee_elements:
#     nominee_name = nominee_element.find('a').text.strip()
#     nominee_work = nominee_element.find('span', class_='cursor-pointer').text.strip()
#     nominees[nominee_name] = nominee_work

# # Print the results
# print(f"Category: {category}")
# print("Winner:", {winner_name: winner_work})
# print("Nominees:", nominees)