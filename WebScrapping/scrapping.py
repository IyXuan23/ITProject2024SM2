import requests
from bs4 import BeautifulSoup

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



#function to scrape the links for each item, by iterating through their pages and getting the relevant links for each subject/course/
#breadth track
def scrapeLinks(numOfPages, targetArray, url):

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

scrapeLinks(NUM_OF_COURSES_PAGES, courseLinkArray, courseURL)
scrapeLinks(NUM_OF_SUBJECTS_PAGES, subjectLinkArray, subjectURL)
scrapeLinks(NUM_OF_BREADTH_TRACK_PAGES, breadthtrackLinkArray, breadthURL)
