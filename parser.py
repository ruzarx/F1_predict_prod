import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime, os
from gc import collect

# Parsing the list of available races

def links_list(html):
    soup = BeautifulSoup(html, 'lxml')
    pages = soup.find('div', class_ = 'table-wrap').find_all('a', class_ = 'dark bold ArchiveLink')
    items = []
    for page in pages:
        values = page.get('href').split('/')
        items.append([values[3], values[5], values[6]])

    return items


# Get html code of the (url) page

def get_html(url):
    r = requests.get(url)
    return r.text

# Getting results table from an html page

def get_page_data(html):
    soup = BeautifulSoup(html, 'lxml')
    table = soup.find('div', class_ = 'resultsarchive-col-right')

    soup = BeautifulSoup(str(table.contents), 'lxml')
    table = soup.find("table", attrs={"class":"resultsarchive-table"})

    # The first tr contains the field names.
    cols = [th.get_text() for th in table.find("tr").find_all("th")]

    line = []
    for row in table.find_all("tr")[1:]:
        line.append([td.get_text() for td in row.find_all("td")])
    
    df = pd.DataFrame(line, columns = cols)

    df['Driver'] = [x.replace('\n', ' ')[-4:] for x in df['Driver']]

    return df

# Parsing practice sessions

def practice_parse(races, data_path):

    for race in races:

        print(race[0], race[2])

        base_url = 'https://www.formula1.com/en/results.html/' + race[0] + '/races/' + race[1] + '/' + race[2] + '/'
         
        # Parsing 3 practice sessions separately into tables
        for ses in ['practice-1', 'practice-2', 'practice-3']:

            # Check if file exists
            if os.path.isfile(data_path + ses + '/' + race[0] + '_' + race[1] + '_' + race[2] + '.csv'):
                continue

            # If not, parse it
            url_gen = base_url + ses + '.html'
            html = get_html(url_gen)
            df = get_page_data(html)
            df['Session'] = ses
            df['Year'] = race[0]
            df['Race_no'] = race[1]
            df['Track'] = race[2]
            df.to_csv(data_path + ses + '/' + race[0] + '_' + race[1] + '_' + race[2] + '.csv', index = False)

    try:
        del df
    except UnboundLocalError:
        pass
    collect()


# Parsing qualifications

def qualification_parse(races, data_path):

    for race in races:

        print(race[0], race[2])

        #https://www.formula1.com/en/results.html/2019/races/1013/italy/practice-3.html
        url_gen = 'https://www.formula1.com/en/results.html/' + race[0] + '/races/' + race[1] + '/' + race[2] + '/qualifying.html'

        # Check if file exists
        if os.path.isfile(data_path + 'qualifying/' + race[0] + '_' + race[1] + '_' + race[2] + '.csv'):
            continue

        # If not, parse it
        html = get_html(url_gen)
        df = get_page_data(html)
        df['Year'] = race[0]
        df['Race_no'] = race[1]
        df['Track'] = race[2]
        df.to_csv(data_path + 'qualifying/' + race[0] + '_' + race[1] + '_' + race[2] + '.csv', index = False)

    try:
        del df
    except UnboundLocalError:
        pass
    collect()


# Parsing races

def race_parse(races, data_path):

    for race in races:

        print(race[0], race[2])

        #https://www.formula1.com/en/results.html/2019/races/1013/italy/practice-3.html
        url_gen = 'https://www.formula1.com/en/results.html/' + race[0] + '/races/' + race[1] + '/' + race[2] + '/race_result.html'

        # Check if file exists
        if os.path.isfile(data_path + 'race/' + race[0] + '_' + race[1] + '_' + race[2] + '.csv'):
            continue

        # If not, parse it

        html = get_html(url_gen)
        df = get_page_data(html)
        df['Year'] = race[0]
        df['Race_no'] = race[1]
        df['Track'] = race[2]
        df.to_csv(data_path + 'race/' + race[0] + '_' + race[1] + '_' + race[2] + '.csv', index = False)

    try:
        del df
    except UnboundLocalError:
        pass
    collect()

# Main function

def main():

    all_races = []
    current_year = datetime.datetime.now().year

    # Entering needed year to start parsing from
    starting_year = input("What is the starting season for parse? ")
    digit = False
    number = False
    while digit == False | number == False:
        try:
            int(starting_year)
        except ValueError:
            starting_year = input("Wrong format. Should be a number. Try again: ")
            digit = False
            number = False
            continue
        else:
            digit = True

        if int(starting_year) not in range(1950, current_year + 1):
            starting_year = input("Wrong format. Should be from 1950 to current year. Type again: ")
            number = False
            digit = False
            continue
        else:
            number = True         

    for year in range(int(starting_year), 2020):
        url = 'https://www.formula1.com/en/results.html/' + str(year) + '/races.html'
        all_races.append(links_list(get_html(url)))

    races = [item for sublist in all_races for item in sublist]

    if not os.path.exists('./data/'): os.mkdir('./data/')
    for session_dir in ['practice-1', 'practice-2', 'practice-3', 'qualifying', 'race']:
        if not os.path.exists('./data/' + session_dir): os.mkdir('./data/' + session_dir) 

    data_path = './data/'

    print()
    print('PARSING PRACTICES', end = '\n\n')
    practice_parse(races, data_path)
    print()
    print('PARSING QUALIFICATIONS', end = '\n\n')
    qualification_parse(races, data_path)
    print()
    print('PARSING RACES', end = '\n\n')
    race_parse(races, data_path)

if __name__ == '__main__':
    main()