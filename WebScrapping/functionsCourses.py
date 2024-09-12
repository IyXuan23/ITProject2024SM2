import requests
from bs4 import BeautifulSoup
import json
import os
from functions import parseTable

def writeCoursesJSONFile(filePath, overviewData, overviewTable, reqData, skillsData, structureData, majorsData, furtherStudyData, 
                        courseName, courseCode):

    """function for writing the scrapped data for courses into a JSON file"""

    data = {
        'Course name': courseName,
        'Course code': courseCode,
        'Overview text': overviewData,
        'Overview table': overviewTable,
        'Entry and participation requirements': reqData,
        'Attribute, outcomes and skills': skillsData,
        'Course Structure': structureData,
        'Majors, minors and specialisations': majorsData,
        'Further Study': furtherStudyData
    }

    with open(filePath, 'w') as json_file:
        json.dump(data, json_file, indent=4)


def parseOverviewTable(table):

    """helper function for scraping the data from the table in the overview section of the course"""

    jsonData = {}

    rows = table.find_all('tr')
    for row in rows:
        header = row.find('th').get_text(strip=True)
        data = row.find('td').get_text(strip=True)

        jsonData[header] = data

    return jsonData

def scrapeOverview(url):

    """function will scrape data from the overview of the course page, and return the text and table info"""

    overviewText = []
    overviewTable = None

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    #scrap subject details
    overviewData = soup.find('div', class_='sidebar-tabs__panel')

    header = overviewData.find('h2')
    stopDiv = overviewData.find('div', class_='course__overview-box-links')

    #start at the header and go down, and stop when reaching the stop div
    nextElem = header.find_next()
    while nextElem != stopDiv:

        nextElem = nextElem.find_next()

        if hasattr(nextElem, 'name') and nextElem.name == 'p':
            overviewText.append(nextElem.get_text(strip=True))

        if hasattr(nextElem, 'name') and nextElem.name == 'table':
            overviewTable = parseOverviewTable(nextElem)

    return overviewText, overviewTable

def titleSearcherReq(lst):

    """(helper) function will look for the header containing [Entry requirements] and 
    [Inherent requirements (core participation requirements)] and return the list of elements."""
    targetList = []

    for item in lst:
        if hasattr(item, 'get_text') and item.get_text() == 'Entry requirements':
            targetList.append(item)

        if (hasattr(item, 'get_text') and item.get_text() == 
            'Inherent requirements (core participation requirements)'):

            targetList.append(item)

    return targetList        

def parseUL(ul):

    """helper function for parsing text from a ul"""

    ulText = []
    lis = ul.find_all('li')

    topLevelUL = ul.find('ul')
    if topLevelUL:
        embeddedLi = topLevelUL.find_all('li', recursive=False)

        newLis = [li for li in lis if li not in topLevelUL]
        lis = newLis

    for li in lis:
        
        #prevent getting text from embedded lists
        txt = ''.join(str(child) for child in li.contents if not child.name)
        if txt != '' and txt != None:
            ulText.append(txt)
            print(txt)

        if li.find('ul') != None:
            
            innerText = []
            innerUL = li.find('ul')
            innerLi = innerUL.find_all('li')
            for li in innerLi:
                innerText.append(li.get_text(strip=True))
            ulText.append(innerText)
            print(innerText)

        #find embedded para text
        embeddedPara = li.find_all('p')
        if embeddedPara:
            for para in embeddedPara:
                paraTxt = parsePara(para)
                ulText.append(paraTxt)    

    return ulText    

def parseOL(ol):
    """helper function for parsing text from a ol"""

    olText = []
    lis = ol.find_all('li')
    index = 1

    for li in lis:
        olText.append(str(index) + '. ' + li.get_text())
        index += 1

    return olText    

def parsePara(para):
    """helper function for parsing text from a para"""
    for br in para.find_all('br'):
        br.replace_with('\n')
    txt = para.get_text(strip=True)
    return txt    

def parseA(a):
    """helper function for parsing text from a href tag"""
    txt = a.get_text(strip=True)
    return txt

def scrapeReq(url):

    """function will scrape the pre-requisites needed for a course and return the data in a json format"""

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    #scrap subject details
    reqDiv = soup.find('div', class_='sidebar-tabs__panel')

    h2s = reqDiv.find_all('h2')
    stopDiv = soup.find('div', 'course__prev-next-buttons')

    #look for [entry requirements] and [inherent requirements...]
    headers = titleSearcherReq(h2s)

    reqData = {}

    for header in headers:
        
        headerText = header.get_text(strip=True)
        nextElem = header.find_next()

        textData = []

        while (nextElem != stopDiv and nextElem not in headers):
            
            if hasattr(nextElem, 'name') and nextElem.name == 'p':
                if parsePara(nextElem) != '':
                    textData.append(parsePara(nextElem))

            if hasattr(nextElem, 'name') and nextElem.name == 'ul':
                textData.extend(parseUL(nextElem))    

            if hasattr(nextElem, 'name') and nextElem.name == 'ol':
                textData.extend(parseOL(nextElem))

            nextElem = nextElem.find_next()

        reqData[headerText] = textData

    return reqData    

def titleSearcherSkills(lst):
    
    """(helper) function will look for the header containing [Professional accreditation] and 
    return the list of elements."""
    targetList = []

    for item in lst:
        if hasattr(item, 'get_text') and item.get_text() == 'Professional accreditation':
            targetList.append(item)

    return targetList      
    
def scrapeSkills(url):

    """function to scrape the skills page in the course data"""

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    skillsContainer = soup.find('div', class_='sidebar-tabs__panel')

    headers = titleSearcherSkills(skillsContainer.find_all('h2'))
    stopDiv = skillsContainer.find('div', id='learning-outcomes')

    skillsData = {}

    for header in headers:
        
        headerText = header.get_text(strip=True)
        nextElem = header.find_next()

        textData = []

        while (nextElem != stopDiv and nextElem not in headers):

            if hasattr(nextElem, 'name') and nextElem.name == 'p':
                text = nextElem.get_text(strip=True)
                if text != '':
                    textData.append(text)

            if hasattr(nextElem, 'name') and nextElem.name == 'ul':
                textData.extend(parseUL(nextElem))    

            if hasattr(nextElem, 'name') and nextElem.name == 'ol':
                textData.extend(parseOL(nextElem))

            nextElem = nextElem.find_next()

        skillsData[headerText] = textData

    return skillsData    

def elementSearcher(header, element, stopDivs):
    """searches for sub-elements by iterating downwards from the provided element. 
    Cannot be replaced by find() as the sub-elements are on the same hierarchy"""
    targets = []

    nextElem = header.find_next()
    while nextElem not in stopDivs:

        if hasattr(nextElem, 'name') and nextElem.name == element:
            targets.append(nextElem)
        #early exit for a depreciated webpage
        if nextElem == None:
            return targets
        nextElem = nextElem.find_next()

    return targets

def scrapStructureText(element):

    """helper function for scraping text from the course structure page"""

    if hasattr(element, 'name') and element.name == 'p':
        if element.find('table') == None:
            txt = parsePara(element)
            if txt != '':
                return txt    

    if hasattr(element, 'name') and element.name == 'ul':
        return parseUL(element)

    if hasattr(element, 'name') and element.name == 'ol':
        return parseOL(element)

    if hasattr(element, 'name') and element.name == 'table':
        return parseTable(element)

    return None    
        
def scrapeStructure(url):

    """function to scrape the course structure page in the courses"""

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    container = soup.find('div', class_='sidebar-tabs__panel')
    headers = container.find_all('h2')
    stopDiv = container.find('div', class_='course__prev-next-buttons')

    #structureData should hold a list of headers
    structureData = {}

    for header in headers:

        headerData = {}
        stopConditions = headers.copy()
        stopConditions.append(stopDiv)
        subHeaders = elementSearcher(header, 'h3', stopConditions)
        nextElem = header.find_next()
        headerText = header.get_text(strip=True)

        extraText = []
        
        #if there are no h3 subheaders, search for h4 immediately
        #since the stop conditions overlap with future h4's, there is no issue
        #with the double loop below
        if len(subHeaders) == 0:
            subHeaders = elementSearcher(header, 'h4', stopConditions)

        #get the text before the subHeaders
        while (nextElem not in headers and nextElem not in 
        subHeaders and nextElem != stopDiv):

            txt = scrapStructureText(nextElem)
            if txt != None and txt != ' ' and txt != '':
                extraText.append(txt)

            if hasattr(nextElem, 'name') and nextElem.name == 'ul':
                nextElem = nextElem.find_next_sibling()
            else:
                nextElem = nextElem.find_next()

        headerData['overview'] = extraText

        for subHeader in subHeaders:
            
            subHeaderData = {}
            subStopConditions = stopConditions.copy()
            subStopConditions = stopConditions.extend(subHeaders)
            subSubHeaders = elementSearcher(subHeader, 'h4', stopConditions)
            nextElem = subHeader.find_next()
            subHeaderText = subHeader.get_text(strip=True)

            extraSubText = []

            while (nextElem not in headers and nextElem not in 
            subHeaders and nextElem not in subSubHeaders and nextElem != stopDiv):

                txt = scrapStructureText(nextElem)
                if txt != None and txt != '' and txt != " ":
                    extraSubText.append(txt)
                if hasattr(nextElem, 'name') and nextElem.name == 'ul':
                    nextElem = nextElem.find_next_sibling()
                else:
                    nextElem = nextElem.find_next()

            subHeaderData['overview'] = extraSubText    
            
            for subSubHeader in subSubHeaders:
                                    
                nextElem = subSubHeader.find_next()
                subSubHeaderData = {}
                subSubHeaderText = subSubHeader.get_text(strip=True)
                extraSubSubText = []

                while (nextElem not in headers and nextElem not in subHeaders and 
                nextElem not in subSubHeaders and nextElem != stopDiv):
                    
                    txt = scrapStructureText(nextElem)
                    if txt != None and txt != ''  and txt != " ":
                        extraSubSubText.append(txt)
                    
                    if hasattr(nextElem, 'name') and nextElem.name == 'ul':
                        nextElem = nextElem.find_next_sibling()
                    else:
                        nextElem = nextElem.find_next()
                subSubHeaderData['overview'] = extraSubSubText   

                subHeaderData[subSubHeaderText] = subSubHeaderData
            headerData[subHeaderText] = subHeaderData
        structureData[headerText] = headerData
    return structureData    

def scrapeMajorTable(table):

    """helper function to scrape the table in the majors minor specialisations page"""

    tableData = {}

    rows = table.find_all('tr')
    rows.pop(0)
    
    for row in rows:

        data = row.find_all('td')
        majorName = data[0].get_text(strip=True)
        creditPoints = data[1].get_text(strip=True) + ' Credits'

        tableData[majorName] = creditPoints

    return tableData

def scrapeMajorText(element):

    """helper function to scrape the text in the majors minor specialisations page"""

    if hasattr(element, 'name') and element.name == 'p':
        if element.find('table') == None:
            return parsePara(element)

    if hasattr(element, 'name') and element.name == 'ol':
        return parseOL(element)

    if hasattr(element, 'name') and element.name == 'ul':
        return parseUL(element)

    if hasattr(element, 'name') and element.name == 'table':
        return scrapeMajorTable(element)

    return None    

def scrapeMajors(url):

    """function to scrape the major minors and specialisations page in the courses"""

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    print(url)
    print(response.url)

    #some master subjects have no major/minor, if so we return an empty list back
    if response.url != url:
        return []
    
    container = soup.find('div', class_='sidebar-tabs__panel')
    header = container.find('h2')
    stopDiv = container.find('div', class_='course__prev-next-buttons')

    headers = []
    headers.extend(elementSearcher(header, 'h3', stopDiv))
    headers.extend(elementSearcher(header, 'h4', stopDiv))

    majorsData = {}

    for header in headers:

        nextElem = header.find_next()
        headerText = header.get_text(strip=True)
        headerData = []

        while nextElem not in headers and nextElem != stopDiv:
            
            data = scrapeMajorText(nextElem)
            if data != None and data != '' and data != []:
                
                headerData.append(data)

            nextElem = nextElem.find_next()

        majorsData[headerText] = headerData   

    return majorsData     

def scrapeFurtherStudy(url):

    """function for scraping the further study page in the courses"""

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    container = soup.find('div', class_='sidebar-tabs__panel')
    header = container.find('h2')
    stopDiv = container.find('div', class_='course__prev-next-buttons')

    furtherStudyData = []

    nextElem = header.find_next()

    while nextElem != header and nextElem != stopDiv:
            
        data = scrapeMajorText(nextElem)
        if data != None:
            furtherStudyData.append(data)

        nextElem = nextElem.find_next()

    return furtherStudyData   

def scrapeCourses(url, courseName, courseCode):


    #https://handbook.unimelb.edu.au/courses/b-sci
    overviewText, overviewTable = scrapeOverview(url)

    #https://handbook.unimelb.edu.au/2024/courses/b-sci/entry-participation-requirements
    reqData = scrapeReq(url + '/entry-participation-requirements')

    #https://handbook.unimelb.edu.au/2024/courses/b-sci/attributes-outcomes-skills
    skillsData = scrapeSkills(url + '/attributes-outcomes-skills')

    #https://handbook.unimelb.edu.au/2024/courses/b-sci/course-structure
    structureData = scrapeStructure(url + '/course-structure')

    #https://handbook.unimelb.edu.au/2024/courses/b-sci/majors-minors-specialisations
    majorsData = scrapeMajors(url + '/majors-minors-specialisations')

    # https://handbook.unimelb.edu.au/2024/courses/b-sci/further-study
    furtherStudyData = scrapeFurtherStudy(url + '/further-study')

    #writing to JSON file
    fileName = courseName.replace(" ", '') + '_info.json'
    fileName = fileName.replace('/', '-')
    filePath = os.path.join('courseInfo', fileName)

    writeCoursesJSONFile(filePath, overviewText, overviewTable, reqData, skillsData, structureData, majorsData,
                        furtherStudyData, courseName, courseCode)
    
    print('scrapped ' + filePath)