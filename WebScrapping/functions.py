import requests
from bs4 import BeautifulSoup
import json
import os

def scrapeLinks(numOfPages, targetArray, url):

    """#function to scrape the links for each item, by iterating through their pages and getting the 
    relevant links for each subject/course breadth track"""

    className = 'search-result-item__anchor'
    #while loop will iterate through all the subject pages and return an array of the links for each individual subject
    i = 1
    while (i <= numOfPages):

        newURL = url + str(i) + '&sort=_score%7Cdesc'

        response = requests.get(newURL)

        soup = BeautifulSoup(response.text, 'html.parser')

        links = soup.find_all('a', class_=className)
        
        for link in links:
            newLink = 'https://handbook.unimelb.edu.au' + link.get('href')
            targetArray.append(newLink)

        print("scrapped page" + str(i))
        i += 1    

def writeJSONFile(filePath, name, code, aims, indicativeContent):
    """writes information to JSON file for the corresponding subbject. Naming convention is [subjectCode]_info.json"""

    data = {
        "subject_name": name,
        "subject_code": code,
        "aims": aims, 
        "indicative_content": indicativeContent
    }

    with open(filePath, 'w') as json_file:
        json.dump(data, json_file, indent=4)


def scrapSubject(url):
    """function for scraping a singular subject information, and will return the data in the form of a json file"""

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    #scrapping name and subject code
    try:
        subjectHeader = soup.find('span', class_='header--course-and-subject__main')
        subjectText = subjectHeader.text.strip()
        parts = subjectText.split('(')
        
        subjectName = parts[0].strip()
        subjectCode = parts[1].replace(')', '').strip()

    except AttributeError:
        subjectHeader = None

    #scrapping aim and description
    try:
        container = soup.find('div', class_='course__overview-wrapper')
        descriptionArray = container.find_all('p')

        aims = descriptionArray[1].text.strip()
        indicativeContent = descriptionArray[4].text.strip()
    except AttributeError:
        description = None

    #writing to JSON file
    fileName = subjectCode + '_info.json'
    filePath = os.path.join('subjectInfo', fileName)

    writeJSONFile(filePath, subjectName, subjectCode, aims, indicativeContent)
    


