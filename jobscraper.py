from bs4 import BeautifulSoup
import urllib
import requests
import json
import sqlite3
import itertools

#path C:\Users\LethalAsian\Desktop\jay\code\jobscraper\main.py
#path C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Python 3.7\python.exe
def load_indeed_jobs(jobtitle, location, experience):
    '''method for loading user inputs into dict vars and then using urllib to encode it into 
    a usable url. Then get html from the page and parse tag where all job info is surrounded in'''

    vars = {'q': jobtitle,'l' : location, 'explvl': experience, 'fromage': 14}
    url = "https://www.indeed.com/jobs?" + urllib.parse.urlencode(vars) #urllib encodes the variables into the url

    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    jobs = soup.find(id="resultsCol")   #gets the html section where all jobs are included in as a soup obj
    print(url)
    return jobs

def extract_job_title_indeed(job_card):
    title_elem = job_card.find('h2', class_='title')
    title = title_elem.text.strip()
    return title

def extract_company_indeed(job_card):
    company_elem = job_card.find('span', class_='company')
    company = company_elem.text.strip()
    return company

def extract_link_indeed(job_card):
    a = job_card.find('a')
    link = a.get('href', None)
    if link == None:
        return "no link found"
    link = 'www.Indeed.com' + link
    return link

def extract_date_indeed(job_card):
    date_elem = job_card.find('span', class_='date')
    date = date_elem.text.strip()
    return date

def extract_summary(job_card):
    summary_elem = job_card.find_all('li')
    summary = [li.text.strip() for li in summary_elem]
    return summary

#because class is a reserved word you have to use class_
#https://www.crummy.com/software/BeautifulSoup/bs4/doc/#searching-by-css-class

def extract_all_job_cards(jobs):
    job_elems = jobs.find_all('div', class_='jobsearch-SerpJobCard') 
    #extracts all htmlblocks within the above parameters
    return job_elems

 
def extract_all_info():
    jobs = load_indeed_jobs('Web Dev', 'New York', 'entry_level')
    job_cards = extract_all_job_cards(jobs)
    extracted_info = []

    summaries = []
    titles = []
    links = []
    for job in job_cards:
        summaries.append(extract_summary(job))
        titles.append(extract_job_title_indeed(job))
        links.append(extract_link_indeed(job))

    extracted_info.append(summaries)
    extracted_info.append(titles)
    extracted_info.append(links)
    return extracted_info


def save_job_db(info, db_file):
    conn = sqlite3.connect(db_file)    
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS jobs (
        id integer PRIMARY KEY,
        title text,
        summary text,
        link text
    )''')

    summaries = info[0]
    titles = info[1]
    links = info[2]
    for (summary, title, link) in zip(summaries, titles, links):
        # print (summary, title, link)
        data = (title, str(summary), link)
        sql = 'INSERT INTO jobs(title,summary,link) VALUES(?,?,?)'
        cur.execute(sql, data)
    conn.commit()
    conn.close()

# print(extract_job_title_indeed(jobs))
# print(extract_company_indeed(jobs))
# info = extract_all_info()
# save_job_db(info, 'jobs.db')
# jobs = load_indeed_jobs('Web Dev', 'New Jersey', 'Entry')
# job_cards = extract_all_job_cards(jobs)
def main():
    info = extract_all_info()
    print('before adding the file')
    save_job_db(info, 'jobs.db')
    print('after adding to the file')

if __name__ == '__main__':
    main()