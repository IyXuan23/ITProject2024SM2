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

def writeJSONFile(filePath, name, code, aims, indicativeContent, necessaryPreReq, oneOfPreReq, coReq, nonAllowed):
    """writes information to JSON file for the corresponding subbject. Naming convention is [subjectCode]_info.json"""

    data = {
        "subject_name": name,
        "subject_code": code,
        "aims": aims, 
        "indicative_content": indicativeContent,
        "necessary pre_requisite": necessaryPreReq,
        "one of pre_requisite": oneOfPreReq,
        "corequisites": coReq,
        "non_allowed_subjects": nonAllowed 
    }

    with open(filePath, 'w') as json_file:
        json.dump(data, json_file, indent=4)

def scrapeOverview(url):
    """function will scrape the subject code and name, overview content and indicative content, and return it as an array
    note: there may be changes to this function down the line to add in ILOs"""

    #note: url is in the format:
    #https://handbook.unimelb.edu.au/2024/subjects/comp30022

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

    return subjectName, subjectCode, aims, indicativeContent

def parseTable(table):
    """helper function: parse table from html, will return the courses as an array"""

    courses = []
    rows = table.find_all('tr')

    for row in rows:
        tds = row.find_all('td')
        if tds:
            courseCode = tds[0].text.strip()
            courses.append(courseCode)

    return courses        

def parsePreReq(courseCode):
    """function will look through the required pre-requisites of a subject, and return the necessary data accordingly.
    2 arrays will be returned, one with the subjects that are necessary [singlePreReq], and one where the student as to do (one of)
    the listed subjects to qualify [oneOfPreReq]"""

    #note: url is in form:
    #https://handbook.unimelb.edu.au/subjects/comp30022/eligibility-and-requirements

    courseCode = courseCode.lower()
    preReqURL = 'https://handbook.unimelb.edu.au/subjects/' + courseCode + '/eligibility-and-requirements'

    response = requests.get(preReqURL)
    soup = BeautifulSoup(response.text, 'html.parser')

    try: 
        preReqContainer = soup.find('div', id='prerequisites')

        singlePreReq = []
        oneOfPreReq = []

        paragraphs = preReqContainer.find_all('p')

        for para in paragraphs:

            text = para.get_text(strip=True).lower()

            if "one of" in text:
                table = para.find('table')
                if table:
                    oneOfPreReq.extend(parseTable(table))

            else:
                table = para.find('table')
                if table:
                    singlePreReq.extend(parseTable(table))       

    except AttributeError:
        print("Pre-Req Not Found")

    return singlePreReq, oneOfPreReq

def scrapeCoReq(courseCode):
    """function for scraping the co-requisite requirement, result will either be a string 'None', or 
    it will return [TEMP VALUE] (function incomplete)""" 

    courseCode = courseCode.lower()
    preReqURL = 'https://handbook.unimelb.edu.au/subjects/' + courseCode + '/eligibility-and-requirements'

    response = requests.get(preReqURL)
    soup = BeautifulSoup(response.text, 'html.parser')

    try:
        coReqHeader = soup.find('h3', text='Corequisites')
        coReqPara = coReqHeader.find_next('p')

        if coReqPara.text.strip().lower() == 'none':
            return 'None'
        else:
            return 'tempValue'

    except AttributeError:
        print("coReq Not Found")

def scrapeNonAllowed(courseCode):
    """function will scrap Non-allowed subjects, either returning the string None, or a list of non-allowed
    subjects"""

    courseCode = courseCode.lower()
    preReqURL = 'https://handbook.unimelb.edu.au/subjects/' + courseCode + '/eligibility-and-requirements'

    response = requests.get(preReqURL)
    soup = BeautifulSoup(response.text, 'html.parser')

    print(soup.prettify())

    try:
        nonAllowedHeader = soup.find('h3', text='Non-allowed subjects')

    except AttributeError:
        print("Non-allowed Subject Not Found")
        return -1

    #look for the none tag
    nonAllowedPara = nonAllowedHeader.find_next('p')   
    if nonAllowedPara.text.strip().lower() == 'none':
        return 'None' 
    
    #there is something, look for tables first, then followed by paragraphs of strings
    else:
        nonAllowedSubjects = []

        #we check each <p>, if there is a table, we extract the codes
        #then check for text and extract subject codes [example: IT Project]
        #we look for <p> until we hit the next header <h3>, then terminate the search
        nextSubject = nonAllowedHeader.find_next(['p', 'h3'])

        while nextSubject and nextSubject.name == 'p':

            table = nextSubject.find('table')
            if table:
                nonAllowedSubjects.extend(parseTable(table))

            else:
                text = nextSubject.text.strip()

                if text:
                    nonAllowedSubjects.append(text)
            
            nextSubject = nextSubject.find_next(['p', 'h3'])

        return nonAllowedSubjects



    


def scrapSubject(url):

    """function for scraping a singular subject information, and will return the data in the form of a json file"""

    subjectName, subjectCode, aims, indicativeContent = scrapeOverview(url)

    necessaryPreReq, oneOfPreReq = parsePreReq(subjectCode)
    coReq = scrapeCoReq(subjectCode)
    nonAllowed = scrapeNonAllowed(subjectCode)

    #writing to JSON file
    fileName = subjectCode + '_info.json'
    filePath = os.path.join('subjectInfo', fileName)

    writeJSONFile(filePath, subjectName, subjectCode, aims, indicativeContent, necessaryPreReq, oneOfPreReq, coReq, nonAllowed)

    #https://handbook.unimelb.edu.au/subjects/comp30022/assessment
    #https://handbook.unimelb.edu.au/2024/subjects/comp30022/dates-times
    #https://handbook.unimelb.edu.au/subjects/comp30022/further-information


