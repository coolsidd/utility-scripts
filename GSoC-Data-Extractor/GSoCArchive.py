#! /usr/bin/python3

import os
import re
import json
import pandas
import requests
from bs4 import BeautifulSoup


session = requests.session()

def org_getter(url_list, json4fill):
    for item in url_list:
        org_name = item.text
        org_page_url = "https://www.google-melange.com"+item.get("href")
        org_page = session.get(org_page_url)
        soup = BeautifulSoup(org_page.text, "html.parser")
        projhref = re.compile(item.get('href')+"/projects")
        projects = [proj.text for proj in soup.find_all(href=projhref)]
        org_dict = {
            "org_name": org_name,
            "no_people": len(projects),
            "projects": projects,
        }
        json4fill.append(org_dict)


def runGSOCold():
    for year in range(9, 15):
        if 10 > year:
            styr = "0"+str(year)
        else:
            styr = str(year)

        file_name = "gsoc"+styr+".json"
        year_url = "https://www.google-melange.com/archive/gsoc/20"+styr
        Soup = BeautifulSoup(session.get(year_url).text, "html.parser")
        result_set = [{"file_name": file_name, "year_url": year_url}]
        url_href_type = re.compile("/archive/gsoc/20../orgs/")
        url_list = [item for item in Soup.find_all(href=url_href_type)]
        org_getter(url_list, result_set)
        with open(file_name, 'w') as final_file:
            final_file.write(json.dumps(result_set))
        print("FILE: "+file_name)

runGSOCold()


def url_list(soup):
    urls = soup.find_all('a', 'organization-card__link')
    urls = ['https://summerofcode.withgoogle.com'+x.get('href') for x in urls]
    return urls

def convert(styrs):
    for styr in styrs:
        jFile = pandas.read_json("gsoc"+styr+".json")
        jFile.to_excel("./gsoc"+styr+".xlsx")
        os.remove("gsoc"+styr+".json")

def populate(soup, urls, result_set):
    for x in range(len(urls)):
        org_page = session.get(urls[x])
        soup = BeautifulSoup(org_page.text, "html.parser")
        no_people = len(soup.find_all('md-card', 'archive-project-card'))
        org_title = soup.find('h3', 'banner__title').contents[0]
        topic_tags = soup.find_all(
            'li',
            'organization__tag organization__tag--topic')
        topic_tags = [x.contents for x in topic_tags]
        tech_tags = soup.find_all(
            'li',
            'organization__tag organization__tag--technology')
        tech_tags = [x.contents for x in tech_tags]
        mhary_dicty = {
            'name': org_title,
            'no_people': no_people,
            'topic_tags': topic_tags,
            'technology_tags': tech_tags}
        result_set.append(mhary_dicty)


URL_2017 = 'https://summerofcode.withgoogle.com/archive/2017/organizations/'
URL_2016 = 'https://summerofcode.withgoogle.com/archive/2016/organizations/'


def runGSOC(file_name):
    with open(file_name, 'r+') as working_file:
        result_set = json.load(working_file)
    year_url = result_set[0]["year_url"]
    soup = BeautifulSoup(session.get(year_url).text, "html.parser")
    urls = url_list(soup)
    populate(soup, urls, result_set)
    with open(file_name, 'w') as final_file:
        final_file.write(json.dumps(result_set))
    print("FILE: "+file_name)


def init_json(file_name, year_url):
    init_data = [{"file_name": file_name, "year_url": year_url}]
    with open(file_name, 'w') as jfl:
        json.dump(init_data, jfl)


init_json('gsoc16.json', URL_2016)
runGSOC('gsoc16.json')
init_json('gsoc17.json', URL_2017)
runGSOC('gsoc17.json')
styrs = ["0" + str(year) if year<10 else str(year) for year in range(9,18)]

convert(styrs)
