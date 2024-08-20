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

def writeJSONFile(filePath, name, code, aims, indicativeContent, optionsPreReq,
                coReq, nonAllowed, assessments, dateTimes, contactInfo, availability):
    """writes information to JSON file for the corresponding subbject. Naming convention is [subjectCode]_info.json"""

    data = {
        "subject name": name,
        "subject code": code,
        "subject availability": availability,
        "aims": aims, 
        "indicative content": indicativeContent,
        "pre-requisites": optionsPreReq,
        "corequisites": coReq,
        "non-allowed subjects": nonAllowed,
        "assessments": assessments,
        "dates and times": dateTimes,
        "contact information": contactInfo
    }

    with open(filePath, 'w') as json_file:
        json.dump(data, json_file, indent=4)

def scrapeOverview(url):
    """function will scrape the subject code and name, overview content and indicative content, and availability
    and return it as an array
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
        print("Subject Name Not Found")

    #scrapping aim and description
    try:
        aims = None
        indicativeContent = None

        container = soup.find('div', class_='course__overview-wrapper')
        descriptionArray = container.find_all('p')

        for para in descriptionArray:
            
            if para.get_text(strip=True) == 'AIMS':
                aims = para.find_next('p').get_text(strip=True)

            elif para.get_text(strip=True) == 'INDICATIVE CONTENT':
                
                indicativeContent = para.find_next('p').get_text(strip=True)
                if indicativeContent == '':
                    ul = para.find_next('ul')
                    if ul:
                        lines = ul.find_all('li')
                        indicativeContent = []
                        for line in lines:
                            indicativeContent.append(line.get_text(strip=True))

            if indicativeContent and aims:
                break

    except AttributeError:
        description = None
        print("Subject Aims and Content Not Found")

    try:
        availability = []

        table = soup.find('table', class_="zebra")
        rows = table.find_all('tr')

        for row in rows:
            header = row.find('th')
            content = row.find('td')

            if (header and header.get_text(strip=True) == 'Availability'):
                availableSem = content.find_all('div')

                for div in availableSem:
                    availability.append(div.get_text(strip=True))

    except AttributeError:
        print("Subject Availability Not Found")                
                

    return subjectName, subjectCode, aims, indicativeContent, availability

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

def parsePreReqOptions(soup):
    """function will look through the soup, and look for whether there is the presence of option 1, 2, etc
    If there is, it will return it in that format, else it will return None"""

    preReqContainer = soup.find('div', id='prerequisites')

    #look for the existence of options
    allP = preReqContainer.find_all('p')
    options = [p for p in allP if 'Option' in p.get_text(strip=True)]

    preReq = []

    if len(options) == 0:
        return None
    else:
        for option in options:
            
            optionText = option.get_text(strip=True)
            courses = []
            txt = None

            table = option.find_next()
            table = table.find_next()
            table = table.find('table')

            if hasattr(table, 'name') and table.name == 'table':
                courses = parseTable(table)

                nextElem = table.find_next('p')
                if hasattr(nextElem, 'get_text') and nextElem.get_text(strip=True) == 'AND':
                    txt = nextElem.find_next('p').get_text(strip=True)
            
            else:
                txt = option.find_next('p').get_text(strip=True)

            data = {
                'option': optionText,
                'courses': courses,
                'points': txt
            }

            preReq.append(data)
        return preReq    


def formatOptions(courseCode):
    """function will look through the soup, and look for whether there is the presence of option 1, 2, etc
    If there is, it will return it in that format, else it will call the other parsePreReq function"""

    courseCode = courseCode.lower()
    preReqURL = 'https://handbook.unimelb.edu.au/subjects/' + courseCode + '/eligibility-and-requirements'

    response = requests.get(preReqURL)
    soup = BeautifulSoup(response.text, 'html.parser')

    preReqContainer = soup.find('div', id='prerequisites')

    #look for the existence of options
    allP = preReqContainer.find_all('p')
    options = [p for p in allP if 'Option' in p.get_text(strip=True)]
    optionList = []


    #there is no options label, we must then use the searching method
    if len(options) == 0:
        return parseORoptions(soup)
    
    #scrape option by option
    else:
        for option in options:
            optionText = option.get_text(strip=True)
            
            targetWords = ['all of', 'one of', 'or', 'and', '']
            necessaryPreReq = []
            oneOfPreReq = []
            altPreReq = []    
        
            nextElem = option.find_next()

            oneOfIndicator = False
            andIndicator = False

            print('OPTION START')

            while ((nextElem not in options) and (hasattr(nextElem, 'get_text') 
                                            and nextElem.get_text() != 'Corequisites')):

                #if it is an item that is not AND, ALL OF, OR blank para
                if ((hasattr(nextElem, 'get_text') and nextElem.get_text(strip=True).lower() not in targetWords) 
                    or (not hasattr(nextElem, 'get_text'))):

                    #if its a table, get the info
                    if (hasattr(nextElem, 'name') and nextElem.name == 'table'):
                        courses = parseTable(nextElem)

                        #either parse it as a oneOf or necessary preReq, depending on what we saw before
                        if (oneOfIndicator):
                            oneOfPreReq.append(courses)
                            #since oneOf / AND oneOf are equivalent in human reading
                            oneOfIndicator = False
                            andIndicator = False
                        else:
                            necessaryPreReq.append(courses)
                    
                    #if its text
                    elif (hasattr(nextElem, 'name') and nextElem.name == 'p' and not nextElem.find('table')):
                        
                        txt = nextElem.get_text(strip=True)
                        
                        if (andIndicator):
                            necessaryPreReq.append(txt)
                            andIndicator = False 
                        else:
                            altPreReq.append(txt)

                    #if its a list
                    elif (hasattr(nextElem, 'name') and nextElem.name == 'ul'):
                        
                        liArray = nextElem.find_all('li')
                        for li in liArray:
                            altPreReq.append(li.get_text(strip=True))
                
                #check for 'One of' or 'All of', if neither are there, assume that it is 'All of'
                if hasattr(nextElem, 'get_text'):
                    if 'all of' in nextElem.get_text().lower():
                        oneOfIndicator = False
                    if 'one of' in nextElem.get_text().lower():
                        oneOfIndicator = True
                    if 'and' in nextElem.get_text().lower():
                        andIndicator = True

                nextElem = nextElem.find_next()

            optionData = {
                'option': optionText,
                'necessary pre-requisite': necessaryPreReq,
                'one of pre-requisite': oneOfPreReq,
                'alternate pre-requisite': altPreReq
            }
            optionList.append(optionData)
            print(optionData)
    return optionList

def parseORoptions(soup):

    print('parsing using OR')

    preReqContainer = soup.find('div', id='prerequisites')

    #look for OR keywords, if there are, use them as options
    allOR = preReqContainer.find_all('p')
    options = [p for p in allOR if 'OR' in p.get_text(strip=True)]

    #We add an initial item to start, have the loop run as many times as needed
    options.insert(0, preReqContainer.find_next())

    optionList = []
    optionNum = 1

    for option in options:
        
        targetWords = ['all of', 'one of', 'or', 'and', '']
        necessaryPreReq = []
        oneOfPreReq = []
        altPreReq = []    
    
        nextElem = option.find_next()

        oneOfIndicator = False
        andIndicator = False

        print('OPTION START')

        while ((nextElem not in options) and (hasattr(nextElem, 'get_text') 
                                        and nextElem.get_text() != 'Corequisites')):

            #if it is an item that is not AND, ALL OF, OR blank para
            if ((hasattr(nextElem, 'get_text') and nextElem.get_text(strip=True).lower() not in targetWords) 
                or (not hasattr(nextElem, 'get_text'))):

                #if its a table, get the info
                if (hasattr(nextElem, 'name') and nextElem.name == 'table'):
                    courses = parseTable(nextElem)

                    #either parse it as a oneOf or necessary preReq, depending on what we saw before
                    if (oneOfIndicator):
                        oneOfPreReq.append(courses)
                        #since oneOf / AND oneOf are equivalent in human reading
                        oneOfIndicator = False
                        andIndicator = False
                    else:
                        necessaryPreReq.append(courses)
                
                #if its text
                elif (hasattr(nextElem, 'name') and nextElem.name == 'p' and not nextElem.find('table')):
                    
                    txt = nextElem.get_text(strip=True)
                    
                    if (andIndicator):
                        necessaryPreReq.append(txt)
                        andIndicator = False 
                    else:
                        altPreReq.append(txt)

                #if its a list
                elif (hasattr(nextElem, 'name') and nextElem.name == 'ul'):
                    
                    liArray = nextElem.find_all('li')
                    for li in liArray:
                        altPreReq.append(li.get_text(strip=True))
            
            #check for 'One of' or 'All of', if neither are there, assume that it is 'All of'
            if hasattr(nextElem, 'get_text'):
                if 'all of' in nextElem.get_text().lower():
                    oneOfIndicator = False
                if 'one of' in nextElem.get_text().lower():
                    oneOfIndicator = True
                if 'and' in nextElem.get_text().lower():
                    andIndicator = True

            nextElem = nextElem.find_next()

        optionData = {
            'option': 'Option ' + str(optionNum),
            'necessary pre-requisite': necessaryPreReq,
            'one of pre-requisite': oneOfPreReq,
            'alternate pre-requisite': altPreReq
        }
        optionList.append(optionData)
        optionNum += 1
        print(optionData)

    return optionList


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
    
    #first look for 'OR' statements, and use these as to replace the options

    try: 
        preReqContainer = soup.find('div', id='prerequisites')

        singlePreReq = []
        oneOfPreReq = []
        altPreReq = []

        paragraphs = preReqContainer.find_all('p')

        for para in paragraphs:

            text = para.get_text(strip=True).lower()

            if "one of" in text:
                table = para.find('table')
                if table:
                    oneOfPreReq.extend(parseTable(table))

            elif 'or' in text:
                nextElem = para.find_next()

                while nextElem and nextElem.name != 'h3':

                    if nextElem.name == 'p':
                        txt = nextElem.get_text(strip=True)
                        if txt != '':
                            altPreReq.append(txt)
                    if nextElem.name == 'ul':
                        liArray = nextElem.find_all('li')
                        for li in liArray:
                            altPreReq.append(li.get_text(strip=True))

                    nextElem = nextElem.find_next()       

            else:
                table = para.find('table')
                if table:
                    singlePreReq.extend(parseTable(table))        

    except AttributeError:
        print("Pre-Req Not Found")

    return singlePreReq, oneOfPreReq, altPreReq, []

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

        if coReqPara.text.strip().lower() == 'none' or coReqPara.text.strip() == '':
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


def scrapeAssessment(courseCode):
    """will scrape the assessments and return the items in a nested JSON style
    unlikely to return empty (as far as i can tell all subjects have assessments)"""

    #note: url is in the form of:
    #https://handbook.unimelb.edu.au/subjects/comp30022/assessment
    courseCode = courseCode.lower()
    assessmentURL = 'https://handbook.unimelb.edu.au/subjects/' + courseCode + '/assessment'

    response = requests.get(assessmentURL)
    soup = BeautifulSoup(response.text, 'html.parser')

    assessments = []

    try:
        table = soup.find('table', class_='assessment-details')

        rows = table.find_all('tr')[1:]

        for row in rows:
            cols = row.find_all('td')
            description = cols[0].get_text(separator='. ', strip=True)
            timing = cols[1].get_text(strip=True)
            percentage = cols[2].get_text(strip=True)

            assessment = {
                "description":description,
                "timing":timing,
                "percentage":percentage
            }
            assessments.append(assessment)

        return assessments    

    except AttributeError:
        print("Assessment Not Found")

def scrapeContactInfo(soup):
    """function will receive soup and scrape the contact info and return it in JSON format"""

    contactInfo = []

    container = soup.find('div', class_='layout-sidebar__side__inner')
    sems = container.find_all('h5')

    for sem in sems:
        currSem = sem.get_text(strip=True)
        data = sem.find_next()
        
        nameContainer = data.find('p')
        name = []
        email = []
        
        #scrape the names of the contact info
        try:
            for element in nameContainer.contents:
                
                #check whether the element is a string, or the name is encoded within <span> or
                #<p>, but also avoid emails which may also be encoded in <span> or <p>
                if hasattr(element, 'name'):
                    if element.name == 'span' or element.name == 'p':
                        if not element.find('a'):
                            name.append(element.get_text(strip=True))
                if isinstance(element, str):
                    name.append(element.strip())

        except TypeError:
            print("Contact Info Not Found")
        
        try:
            emailContainer = data.find_all('a')
            for eCon in emailContainer:
                email.append(eCon.get_text(strip=True))
        except TypeError:
            print("Email Not Found")        


        jsonData = {currSem:{
            'name': name,
            'email': email
        }}

        contactInfo.append(jsonData)

    return contactInfo

def scrapeDateTime(courseCode):
    """function will scrape the date and times page, along with the relevant info in the given table, and return the info
    in JSON format"""

    #note: url is in the form of:
    #https://handbook.unimelb.edu.au/2024/subjects/comp30022/dates-times
    courseCode = courseCode.lower()
    assessmentURL = 'https://handbook.unimelb.edu.au/subjects/' + courseCode + '/dates-times'

    response = requests.get(assessmentURL)
    soup = BeautifulSoup(response.text, 'html.parser')

    availableSemsDateTimes = []
    

    try:
        container = soup.find('div', class_="sidebar-tabs__panel")
        ul = container.find('ul', class_='accordion')

        termList = ul.find_all('li')

        for lst in termList:
            lstDivs = lst.find_all('div')

            dateTimes = []

            for div in lstDivs:
                if div.has_attr('class') and 'accordion__title' in div['class']:
                    termName = div.get_text(strip=True)

                if div.has_attr('class') and 'accordion__hidden' in div['class']:
                    table = div.find('table', class_='contact_details')
                    rows = table.find_all('tr')

                    for row in rows:
                        header = row.find('th').get_text(strip=True)
                        data = row.find('td').get_text(strip=True)

                        dateTime = {
                            header:data
                        }

                        dateTimes.append(dateTime)
                    
                    semDateTime = {
                        termName:dateTimes
                    }
                    availableSemsDateTimes.append(semDateTime)        


        contactInfo = scrapeContactInfo(soup)
        return availableSemsDateTimes, contactInfo


    except AttributeError:
        print("Date Time Not Found")


def scrapSubject(url):

    """function for scraping a singular subject information, and will return the data in the form of a json file"""

    subjectName, subjectCode, aims, indicativeContent, availability = scrapeOverview(url)

    coReq = scrapeCoReq(subjectCode)
    nonAllowed = scrapeNonAllowed(subjectCode)

    assessments = scrapeAssessment(subjectCode)

    dateTimes, contactInfo = scrapeDateTime(subjectCode)

    optionsPreReq = formatOptions(subjectCode)

    #writing to JSON file
    fileName = subjectCode + '_info.json'
    filePath = os.path.join('subjectInfo', fileName)

    writeJSONFile(filePath, subjectName, subjectCode, aims, indicativeContent, optionsPreReq, \
                coReq, nonAllowed, assessments, dateTimes, contactInfo, availability)

    #https://handbook.unimelb.edu.au/subjects/comp30022/further-information


