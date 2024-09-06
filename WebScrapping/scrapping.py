import requests
from bs4 import BeautifulSoup

from functions import *
from functionsCourses import *
from functionsBreadthTrack import *

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

subjectLinks = retrieveLinks('linkStorage\subjectLinks.json')
#courseLinks = retrieveLinks('linkStorage\courseLinks.json')

#0-50 DONE
#51-266 DONE
#267-892 DONE
# for link in subjectLinks:
#       scrapSubject(link[2], link[1], link[0])

# print(courseLinks.index([
#             "080CN",
#             "Master of Psychology (Clinical Neuropsychology)/Doctor of Philosophy",
#             "https://handbook.unimelb.edu.au/2024/courses/080cn"
#         ]))

scrapSubject('https://handbook.unimelb.edu.au/subjects/educ91197', 'Research Project in Education', 'EDUC91197')

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
# for link in courseLinks[45:]:
#     print(link[1])
#     scrapeCourses(link[2], link[1], link[0])

#scrapping for the (bachelor) courses

#scrapeCourses('https://handbook.unimelb.edu.au/2024/courses/b-sci')
#scrapeCourses('https://handbook.unimelb.edu.au/2024/courses/b-des', 'Bachelor of Design', 'B-DES')
# scrapeCourses("https://handbook.unimelb.edu.au/2024/courses/gc-ahrc", 
#             "Graduate Certificate in Aboriginal Health in Rural Communities", "GC-AHRC")


#scrapping for breadth track
#scrapeBT('https://handbook.unimelb.edu.au/2024/components/btrack-121')
# for BT in breadthtrackLinkArray:
#     scrapeBT(BT)



