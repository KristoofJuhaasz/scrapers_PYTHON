import requests
import bs4
import csv
import os

def crawler(max_pages):
    player_list=[]
    for page_num in range(1,max_pages+1):
        url='https://www.futbin.com/world-cup/players?page='+str(page_num)
        source_code = requests.get(url)
        database = bs4.BeautifulSoup(source_code.text, "lxml")
        table = database.find('table', id="repTb")
        for tr in table.find_all('tr'):
            td = tr.find_all('td')
            name=(td[0].text).lstrip().replace('\n', '')
            country_input=str(td[0].find_all('a')[1])
            country=country_to_string(country_input)
            rating=td[1].text.lstrip().replace('\r', '')
            mode_input=str(td[1].span)
            mode=mode_to_string(mode_input)
            result=(country, name, rating, mode) #bovitheto
            player_list.append(result)
    write_to_csv(player_list)
    print('Output file is ready!')
    #return player_list

def country_to_string(input_str):
    first=int(input_str.find('data-original-title="'))+len('data-original-title="')
    for i in range(first,first+100):
        if input_str[i]=='"':
            last=int(i)
            break
    country=input_str[first:last]
    return country

def mode_to_string(input_str):
    first=int(input_str.find('<span class="'))+len('<span class="')
    for i in range(first,first+100):
        if input_str[i]=='"':
            last=int(i)
            break
    mode=input_str[first:last]
    return mode

def write_to_csv(to_be_saved):
    filename = os.path.join(os.environ["HOMEDRIVE"], os.environ["HOMEPATH"], "Desktop", "results.csv")
    myFile = open(filename, 'w', newline='', encoding="utf-8")
    header=('country','name','rating','mode')
    with myFile:
        writer = csv.writer(myFile)
        writer.writerow(header)
        writer.writerows(to_be_saved)
    
print(crawler(39))