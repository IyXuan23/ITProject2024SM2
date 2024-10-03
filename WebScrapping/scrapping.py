import requests
from bs4 import BeautifulSoup
import os
import json

from functions import *
from functionsCourses import *
from functionsBreadthTrack import *
from functionsMajors import *

NUM_OF_SUBJECTS_PAGES = 314
NUM_OF_COURSES_PAGES = 28
NUM_OF_BREADTH_TRACK_PAGES = 7

#arrays to hold all the relevant links
subjectLinkArray = []
courseLinkArray = []
breadthtrackLinkArray = []

subjectURL = 'https://handbook.unimelb.edu.au/search?study_periods%5B%5D=all&area_of_study%5B%5D=all&level_type%5B%5D=all&campus_and_attendance_mode%5B%5D=all&types%5B%5D=subject&year=2024&org_unit%5B%5D=all&page='
courseURL = 'https://handbook.unimelb.edu.au/search?types%5B%5D=course&year=2024&subject_level_type%5B%5D=all&study_periods%5B%5D=all&area_of_study%5B%5D=all&org_unit%5B%5D=all&campus_and_attendance_mode%5B%5D=all&page='
breadthURL = 'https://handbook.unimelb.edu.au/search?study_periods%5B%5D=all&area_of_study%5B%5D=all&types%5B%5D=breadth&year=2024&level_type%5B%5D=all&campus_and_attendance_mode%5B%5D=all&org_unit%5B%5D=all&page='

#scrapeOfferedLinks(NUM_OF_COURSES_PAGES, courseLinkArray, courseURL, 'courseLinks.json')
#scrapeOfferedLinks(NUM_OF_SUBJECTS_PAGES, subjectLinkArray, subjectURL, 'subjectLinks.json')
#scrapeLinks(NUM_OF_BREADTH_TRACK_PAGES, breadthtrackLinkArray, breadthURL)

#subjectLinks = retrieveLinks('linkStorage\subjectLinks.json')
#courseLinks = retrieveLinks('linkStorage\courseLinks.json')
#majorLinks = retrieveLinks('linkStorage\majorLinks.json')

#0-50 DONE
#51-266 DONE
#267-892 DONE
# for link in subjectLinks:
#       scrapSubject(link[2], link[1], link[0])

# print(courseLinks.index([
#             "MC-BAPTME",
#             "Master of Business Administration",
#             "https://handbook.unimelb.edu.au/2024/courses/mc-baptme"
#         ]))

#scrapSubject('https://handbook.unimelb.edu.au/subjects/educ91197', 'Research Project in Education', 'EDUC91197')

#scrapSubject("https://handbook.unimelb.edu.au/subjects/comp30022")
# scrapSubject("https://handbook.unimelb.edu.au/2024/subjects/comp10001")
# scrapSubject("https://handbook.unimelb.edu.au/2024/subjects/comp10002")
# scrapSubject('https://handbook.unimelb.edu.au/2024/subjects/comp10003')

# scrapSubject('https://handbook.unimelb.edu.au/2024/subjects/comp20008')

#has options tag
# scrapSubject('https://handbook.unimelb.edu.au/2024/subjects/comp20007')
# scrapSubject('https://handbook.unimelb.edu.au/2024/subjects/comp20005')
# scrapSubject('https://handbook.unimelb.edu.au/2024/subjects/comp20003')

#TESTING: NEEDS OVERVIEW ADJUSTMENT
# scrapSubject('https://handbook.unimelb.edu.au/2024/subjects/comp30013')
# scrapSubject('https://handbook.unimelb.edu.au/2024/subjects/comp30020', 'Declarative Programming', 'COMP30020')
# scrapSubject('https://handbook.unimelb.edu.au/2024/subjects/comp30023')
# scrapSubject('https://handbook.unimelb.edu.au/2024/subjects/comp30024')
# scrapSubject('https://handbook.unimelb.edu.au/2024/subjects/comp30019')
# scrapSubject('https://handbook.unimelb.edu.au/2024/subjects/comp30027')
# scrapSubject('https://handbook.unimelb.edu.au/2024/subjects/comp30026')


#0-44 done
# for link in courseLinks :
#     print(link[1])
#     scrapeCourses(link[0], link[1], link[2])

#scrapping for the (bachelor) courses

#scrapeCourses('https://handbook.unimelb.edu.au/2024/courses/b-sci')
#scrapeCourses('https://handbook.unimelb.edu.au/2024/courses/b-des', 'Bachelor of Design', 'B-DES')
# scrapeCourses(            "B-BMED",
#             "Bachelor of Biomedicine",
#             "https://handbook.unimelb.edu.au/2024/courses/b-bmed")


#scrapping for breadth track
#scrapeBT('https://handbook.unimelb.edu.au/2024/components/btrack-121')
# for BT in breadthtrackLinkArray:
#     scrapeBT(BT)

# getMajorLinks(courseLinks)
# scrapeMajorInformation(majorLinks)

def filterDict(majorData):

    for element in majorData:
        if type(element) == dict:
            return element
    
    return None


directoryPath = 'courseInfo'
pairingList = []
for fileName in os.listdir(directoryPath):

    filePath = os.path.join(directoryPath, fileName)

    with open(filePath, 'r') as file: 

        data = json.load(file)
        courseName = data['Course name']

        if "Majors, minors and specialisations" in data:
            majorData = data["Majors, minors and specialisations"]

            keys = [key for key in majorData.keys() if 'major' in key.lower()]

            if len(keys) >= 1:
                majorDataArray = [majorData[key] for key in keys]

            else:
                print('no Majors = ' + courseName)
                print(keys)
                continue
        
        for majorData in majorDataArray:
            someData = filterDict(majorData)
            if someData == None:
                continue
            else:
                result = [[courseName, major, points] for major, points in someData.items()]
                pairingList.extend(result)

newFileName = 'courseMajorPairing.json'
newFilePath = os.path.join('majorInfo', newFileName)
with open(newFilePath, 'w') as newFile:
    json.dump(pairingList, newFile, indent=4)


