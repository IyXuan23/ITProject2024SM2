import requests
from bs4 import BeautifulSoup
import json
import os
from functions import parseTable
from functionsCourses import parseA, parseOL, parseUL, parsePara

def writeBTJSONFile(filePath, nameBT, dataBT):

    data = {
        'name': nameBT,
        'information': dataBT
    }

    with open(filePath, 'w') as json_file:
        json.dump(data, json_file, indent=4)

def scrapeBTData(element):


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

    #https://handbook.unimelb.edu.au/2024/components/btrack-121
    nameBT, dataBT = scrapeBTOverview(url)

    #writing to JSON file
    fileName = nameBT + '_info.json'
    filePath = os.path.join('breadthTrackInfo', fileName)

    writeBTJSONFile(filePath, nameBT, dataBT)