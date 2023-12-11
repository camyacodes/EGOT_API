import re

from bs4 import BeautifulSoup


with open("1st_annual.html") as file:
    contents = file.read()

soup = BeautifulSoup(contents, 'html.parser')

# sections = soup.find_all('section')
parent_sections = soup.find_all('section', class_='h-full w-full flex flex-col items-center mt-6 md-xl:mt-8')

for parent in parent_sections:

    child_section = parent.find('section')

    category = child_section.find('div', class_='w-full text-left md-xl:text-right mb-1 md-xl:mb-20px text-14 md-xl:text-22 font-polaris uppercase')
    unformatted_category_text = category.text.strip().replace('\n', '')
    category_text = re.sub(' +', ' ', unformatted_category_text)
    print(category_text)

# section_ids = [section['id'] for section in parent_sections if section.get('id') is not None]
# print(section_ids)

unique_categories = []
winners = {}


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