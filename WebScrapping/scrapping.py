import requests
from bs4 import BeautifulSoup

from functions import *
from functionsCourses import *

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

# scrapeLinks(NUM_OF_COURSES_PAGES, courseLinkArray, courseURL)
# scrapeLinks(NUM_OF_SUBJECTS_PAGES, subjectLinkArray, subjectURL)
# scrapeLinks(NUM_OF_BREADTH_TRACK_PAGES, breadthtrackLinkArray, breadthURL)

# scrapSubject("https://handbook.unimelb.edu.au/subjects/comp30022")
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
# scrapSubject('https://handbook.unimelb.edu.au/2024/subjects/comp30020')
# scrapSubject('https://handbook.unimelb.edu.au/2024/subjects/comp30023')
# scrapSubject('https://handbook.unimelb.edu.au/2024/subjects/comp30024')
# scrapSubject('https://handbook.unimelb.edu.au/2024/subjects/comp30019')
# scrapSubject('https://handbook.unimelb.edu.au/2024/subjects/comp30027')
# scrapSubject('https://handbook.unimelb.edu.au/2024/subjects/comp30026')

scrapeCourses('https://handbook.unimelb.edu.au/2024/courses/b-sci')



