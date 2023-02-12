import requests
import faker
import mysql.connector

from bs4 import BeautifulSoup

con = mysql.connector.connect(host='sql6.freesqldatabase.com',
                              user='sql6491827',
                              password='5XP9swKJeZ',
                              port=3306,
                              database='sql6491827')

if con.is_connected():
    print('Connected')
else:
    print('Not connected')

cur = con.cursor()

ua = faker.Faker().firefox()
site = 'https://jobs.amdocs.com/search/'
head = {'User-Agent': ua}

l = []
c = 1
for i in range(0, 151, 15):
    query = {
        'q': 'engineer',
        'startrow': i
    }
    res = requests.get(url=site, headers=head, params=query)

    soup = BeautifulSoup(res.text, 'html.parser')

    jobs = soup.find(name='table', id='searchresults').find_all(class_='colTitle')

    for i in jobs:
        l.append(i.find(attrs={'class': 'jobTitle-link'}).text.strip())
        l.append(i.find(attrs={'class': 'jobLocation'}).text.strip())
        l.append(i.find(attrs={'class': 'jobDate'}).text.strip())
        link = ('https://jobs.amdocs.com' + i.find(attrs={'class': 'jobTitle-link'}).get('href'))

        res = requests.get(url=link, headers=head)
        soup = BeautifulSoup(res.text, 'html.parser')

        job_data = soup.find(class_='jobDisplay')

        apply_link = job_data.find('a').get('href')
        l.append('https://jobs.amdocs.com' + apply_link)

        job_id = job_data.find(class_='jobdescription')
        try:
            l.append(job_id.p.span.text)
        except:
            l.append(None)

        desp = job_data.find_all('div')[23]
        l.append(desp.p.text)

        cur.execute('insert into amdocs_jobs values(%s, %s, %s, %s, %s, %s)', l)
        con.commit()

        l.clear()
        print(c, 'done')
        c += 1

con.close()
