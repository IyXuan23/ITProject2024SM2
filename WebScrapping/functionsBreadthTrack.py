import requests
from bs4 import BeautifulSoup
import json
import os
from functions import parseTable
from functionsCourses import parseA, parseOL, parseUL, parsePara

def writeBTJSONFile(filePath, nameBT, dataBT):

    """function to write the breadth track data as a JSON file"""

    data = {
        'name': nameBT,
        'information': dataBT
    }

    with open(filePath, 'w') as json_file:
        json.dump(data, json_file, indent=4)

def scrapeBTData(element):

    """helper function for scraping breadth track data, by checking for each HTML tag"""

    if hasattr(element, 'name'):

        if element.name == 'p':
            if element.find('table') == None:
                return parsePara(element)
        
        if element.name == 'ul':
            return parseUL(element)

        if element.name == 'ol':
            return parseOL(element)

        if element.name == 'table':
            return parseTable(element)
    return None        

def scrapeBTOverview(url):

    """scrape overview of the breadth track, returning the name and overview of the track"""

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    #get the name of the course
    nameContainer = soup.find('span', class_='header--course-and-subject__main')
    nameBT = nameContainer.get_text(strip=True)


    #scrape the data
    dataBT = {}
    container = soup.find('div', class_='layout-sidebar__main__inner')
    headers = container.find_all('h2')
    stopDiv = soup.find('div', class_='course__prev-next-buttons')

    if len(headers) > 0:
        for header in headers:

            headerName = header.get_text(strip=True)
            nextElem = header.find_next()
            currData = []

            while nextElem not in headers and nextElem != stopDiv:
                text = scrapeBTData(nextElem)
                if text != None:
                    currData.append(text)
                nextElem = nextElem.find_next() 

            dataBT[headerName] = currData      

    return nameBT, dataBT 

def scrapeBT(url):

    """main scraping function for scraping breadth tracks"""

    #https://handbook.unimelb.edu.au/2024/components/btrack-121
    nameBT, dataBT = scrapeBTOverview(url)

    #writing to JSON file
    fileName = nameBT + '_info.json'
    filePath = os.path.join('breadthTrackInfo', fileName)

    writeBTJSONFile(filePath, nameBT, dataBT)