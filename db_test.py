import re
from bs4 import BeautifulSoup
from selenium import webdriver
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configure MySQL database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:C$ocks2016!@localhost/grammy_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Year(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.Integer)
    categories = db.relationship('Category', backref='year', lazy=True)

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    year_id = db.Column(db.Integer, db.ForeignKey('year.id'), nullable=False)
    name = db.Column(db.String(255))
    winners = db.relationship('Winner', backref='category', lazy=True)
    nominees = db.relationship('Nominee', backref='category', lazy=True)

class Winner(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    artist = db.Column(db.String(255))
    work = db.Column(db.String(255))

class Nominee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    artist = db.Column(db.String(255))
    work = db.Column(db.String(255))

# Your HTML content (replace this with your actual HTML)
with open("links.html") as file:
    links_content = file.read()

# Parse the HTML content
soup = BeautifulSoup(links_content, 'html.parser')

# Extract links
base_url = "https://www.grammy.com"  # Replace with your actual base URL
url_list = [base_url + link['href'] for link in soup.find_all('a', href=True)]

# Set up Selenium WebDriver (make sure you have the appropriate WebDriver for your browser)
driver = webdriver.Chrome()  # You can change this to Firefox or other supported browsers
with app.app_context():

    db.session.query(Nominee).delete()
    db.session.query(Winner).delete()
    db.session.query(Category).delete()
    db.session.query(Year).delete()
    db.session.commit()

    db.create_all()
    year_number = 0
    for url in url_list:
        year_number += 1

        # Check if the year already exists in the database
        year = Year.query.filter_by(year=year_number).first()
        if not year:
            year = Year(year=year_number)
            db.session.add(year)
            db.session.commit()
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
            category_name = re.sub(' +', ' ', unformatted_category_text)

            winner_work_div = child_section.find('div', class_='w-full text-center md-xl:text-left text-17 md-xl:text-22 mr-10px md-xl:mr-30px font-polaris font-bold md-xl:leading-8 tracking-wider')
            winner_work = winner_work_div.text.strip()

            if (winner_div := child_section.find('div', class_='awards-category-link')) is not None:
                unformatted_winner_text = winner_div.text.strip().replace('\n', '')
                winner_artist = re.sub(' +', ' ', unformatted_winner_text)
            elif (winner_div := child_section.find('div', class_='w-full text-left text-14 font-polaris md-xl:leading-normal')) is not None:
                unformatted_winner_text = winner_div.text.strip().replace('\n', '')
                winner_artist = re.sub(' +', ' ', unformatted_winner_text)
            elif winner_div is None:
                winner_artist = "Null"

            # Extract the nominees
            nominee_sections = child_section.find_all('div', class_='accordion__section')
            nominees = []

            for section in nominee_sections:
                unformatted_nominee_work = section.find('span').text.strip().replace('\n', '')
                nominee_work = re.sub(' +', ' ', unformatted_nominee_work)

                nominee_artist_element = section.find('div', class_='awards-nominees-link')

                if nominee_artist_element and not nominee_artist_element.text:
                    accordion_content_element = section.find('div', class_='accordion__content')
                    unformatted_nominee_artist = accordion_content_element.text.strip().replace('\n', '') if accordion_content_element else None
                elif nominee_artist_element:
                    unformatted_nominee_artist = nominee_artist_element.text.strip().replace('\n', '')

                nominee_artist = re.sub(' +', ' ', unformatted_nominee_artist) if unformatted_nominee_artist else "Null"

                nominees.append(Nominee(artist=nominee_artist, work=nominee_work))

            # Create database entries
            category = Category(year_id=year.id, name=category_name, winners=[Winner(artist=winner_artist, work=winner_work)], nominees=nominees)
            db.session.add(category)
            db.session.commit()
# Create tables if not exist
with app.app_context():
    db.create_all()

# Quit the Selenium WebDriver
driver.quit()
