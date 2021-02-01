import pandas as pd
import requests
import numpy as np
from bs4 import BeautifulSoup
from time import sleep
from random import randint

headers = dict()
headers[
    "User-Agent"
] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"

pavadinimai = []
links = []
alga = []
net_or_gross = []
valiuta = []
miestas = []
laikas = []
test_boxes = []
column_name_1 = []
column_value_1 = []
column_name_2 = []
column_value_2 = []
column_name_3 = []
column_value_3 = []
column_name_4 = []
column_value_4 = []

page_count = 0

pages = np.arange(1, 55, 1)
for page in pages:
    url = f"https://www.cvbankas.lt/?miestas=Vilnius&page={str(page)}"
    results = requests.get(url, headers=headers)
    soup = BeautifulSoup(results.content, 'html.parser')

    listings = soup.find('div', id="js_id_id_job_ad_list")
    items = listings.find_all('article')
    listing_container = BeautifulSoup(str(listings.find_all(class_="list_a can_visited list_a_has_logo")), 'html.parser')
    sleep(randint(2, 6))
    page_count = page
    ad_count = 0

    for link in listing_container.findAll('a'):
        links.append(link.get('href'))

        ad_count += 1
        results2 = requests.get(link.get('href'), headers=headers)
        soup2 = BeautifulSoup(results2.content, 'html.parser')

        job_description_box = soup2.find('section', itemprop="description")
        sections = job_description_box.find_all('section')

        try:
            heading1 = sections[0].find('h4', class_="heading4 jobad_subheading").get_text() if sections[0].find('h4', class_="heading4 jobad_subheading") is not None else ""
            column_name_1.append(heading1)
            text1 = sections[0].find('div', class_="jobad_txt").get_text() if sections[0].find('div', class_="jobad_txt") is not None else ""
            column_value_1.append(text1)

            heading2 = sections[1].find('h4', class_="heading4 jobad_subheading").get_text() if sections[1].find('h4', class_="heading4 jobad_subheading") is not None else ""
            column_name_2.append(heading2)
            text2 = sections[1].find('div', class_="jobad_txt").get_text() if sections[1].find('div', class_="jobad_txt") is not None else ""
            column_value_2.append(text2)

            heading3 = sections[2].find('h4', class_="heading4 jobad_subheading").get_text() if sections[2].find('h4', class_="heading4 jobad_subheading") is not None else ""
            column_name_3.append(heading3)
            text3 = sections[2].find('div', class_="jobad_txt").get_text() if sections[2].find('div', class_="jobad_txt") is not None else ""
            column_value_3.append(text3)

            heading4 = sections[3].find('h4', class_="heading4 jobad_subheading").get_text() if sections[3].find('h4', class_="heading4 jobad_subheading") is not None else ""
            column_name_4.append(heading4)
            text4 = sections[3].find('div', class_="jobad_txt").get_text() if sections[3].find('div', class_="jobad_txt") is not None else ""
            column_value_4.append(text4)
        except IndexError:
            if len(sections) == 3:
                heading4 = ""
                column_name_4.append(heading4)
                text4 = ""
                column_value_4.append(text4)
            elif len(sections) == 2:
                heading3 = ""
                column_name_3.append(heading3)
                text3 = ""
                column_value_3.append(text3)
                heading4 = ""
                column_name_4.append(heading4)
                text4 = ""
                column_value_4.append(text4)
            elif len(sections) == 1:
                heading2 = ""
                column_name_2.append(heading2)
                text2 = ""
                column_value_2.append(text2)
                heading3 = ""
                column_name_3.append(heading3)
                text3 = ""
                column_value_3.append(text3)
                heading4 = ""
                column_name_4.append(heading4)
                text4 = ""
                column_value_4.append(text4)
            else:
                print(f"!!!  UNKNOWN INDEX ERROR for ad {ad_count} on page {page_count}  !!!")
            print(f"Index Error for ad {ad_count} on page {page_count}. Most likely the ad description was shorter than usual.")

        except AttributeError:
            heading1 = ""
            column_name_1.append(heading1)
            text1 = ""
            column_value_1.append(text1)
            heading2 = ""
            column_name_2.append(heading2)
            text2 = ""
            column_value_2.append(text2)
            heading3 = ""
            column_name_3.append(heading3)
            text3 = ""
            column_value_3.append(text3)
            heading4 = ""
            column_name_4.append(heading4)
            text4 = ""
            column_value_4.append(text4)
            print(f"!!! Attribute error on page {page_count} for ad {ad_count}! Filled in blanks for column names and values...")

        sleep(randint(2, 3))
        print(f"Done with ad {ad_count} on page {page_count}")

    for item in items:
        job_title = item.find('h3').get_text() if item.find('h3') is not None else ""
        pavadinimai.append(job_title)
        salary = item.find('span', class_="salary_amount").get_text() if item.find('span', class_="salary_amount") is not None else ""
        alga.append(salary)
        salary_calculation = item.find('span', class_="salary_calculation").get_text() if item.find('span', class_="salary_calculation") is not None else ""
        net_or_gross.append(salary_calculation)
        salary_period = item.find('span', class_="salary_period").get_text() if item.find('span', class_="salary_period") is not None else ""
        valiuta.append(salary_period)
        list_city = item.find('span', class_="list_city").get_text() if item.find('span', class_="list_city") is not None else ""
        miestas.append(list_city)
        txt_list_2 = item.find('span', class_="txt_list_2").get_text() if item.find('span', class_="txt_list_2") is not None else item.find('span', class_="txt_list_important").get_text() if item.find('span', class_="txt_list_important") is not None else ""
        laikas.append(txt_list_2)

    print(f"Finished scraping page {page_count}")

output = pd.DataFrame(
     {
         'job_name': pavadinimai,
         'job_salary': alga,
         'job_net_or_gross': net_or_gross,
         'job_currency': valiuta,
         'job_city': miestas,
         'job_time': laikas,
         'job_link': links,
         'job_desc_column_name_1': column_name_1,
         'job_desc_column_text_1': column_value_1,
         'job_desc_column_name_2': column_name_2,
         'job_desc_column_text_2': column_value_2,
         'job_desc_column_name_3': column_name_3,
         'job_desc_column_text_3': column_value_3,
         'job_desc_column_name_4': column_name_4,
         'job_desc_column_text_4': column_value_4,
      })
