#!/usr/bin/python3
"""
SunDev Flask App 
"""
#from flask import Flask, render_template, url_for
from quart import Quart
from quart import (
     abort, redirect, render_template, request, session,
     url_for,
 )
import uuid
import requests
import datetime

# flask setup
app = Quart(__name__)
#app = Flask(__name__)
app.url_map.strict_slashes = False
port = 5000
host = '0.0.0.0'

""" HEADER FOR THE REQUEST LIBRARY """
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'}

""" API key, that allows me to use the comic vine services """
apikey = '7b60a268a25a1f46fb909c253c3a888ec6f79881'

@app.errorhandler(404)
def page_not_found(error):
    """
    404 error handler method
    """
    return render_template('404.html'), 404

@app.route('/')
def main_page():
    """
    handles the rendering for the main page, or home
    """
    return render_template('index.html',comic_list=render_main_page(0))

@app.route('/<index_page>')
def main_page_index(index_page):
    """
    handles the rendering of the main page with a page number like a parameter in the URL
    """
    return render_template('index.html',comic_list=render_main_page(index_page))

@app.route('/issue/<issue_id>')
def display_issue(issue_id):
    """
    handles the rendering for the each Issue number
    """
    url = 'https://comicvine.gamespot.com/api/issue/4000-' + issue_id +'/?api_key=' + apikey + '&format=json'
    response = requests.get(url, headers=headers)

    data = response.json()['results']

    """
    if the data variable doesnt contains anything, this condition will handle that case
    """
    if len(data) != 0:
        issue_pict = data['image']['original_url']
        issue_description = data['description'] if data['description'] is not None else ""
        volume_name = data['volume']['name'] if data['volume']['name'] is not None else ""
        issue_number = data['issue_number'] if data['issue_number'] is not None else ""
        issue_name = data['name'] if data['name'] is not None else ""
        issue_title = str(volume_name + " #" + issue_number + " " + issue_name)

        return render_template('issue.html',
                               chara_list=get_chara_info('character_credits' ,data),
                               creator_list=get_chara_info('person_credits' ,data),
                               teams_list=get_chara_info('team_credits' ,data),
                               location_list=get_chara_info('location_credits' ,data),
                               concept_list=get_chara_info('concept_credits' ,data),
                               issue_pict=issue_pict,
                               issue_title=issue_title,
                               issue_description=issue_description
                               )
    else:
        return render_template('404.html')

def get_person_pict(api_adress):
    """
    handles the request to get the picture of the characters from another endpoint
    This process take a bit of time, there was an attemp to make this petition asynchronous, but I failed achievent it
    """
    url = api_adress + '?api_key=' + apikey + '&format=json'
    print("///initiating : getting picture from another endpoint")
    print(url)
    data = []
    try:
        response = requests.get(url, headers=headers)
        data = response.json()['results']['image']['original_url']
    except:
        print("/////ERROR///////An exception occurred in the request of " + api_adress + "!")
    print(data)
    print("////")
    return data

def get_chara_info(category , api_data):
    """
    handles the iteration for each character category, here we call the method that handles the character picture adquisition
    """
    chara_info = []
    print("len of category: " +category + ": " + str(len(api_data[category])))
    if len(api_data[category]) != 0: 
        for item in api_data[category]:
            chara_info.append([item['name'], get_person_pict(item['api_detail_url'])])
    else:
        print("empty category: " + category)
    return chara_info

def render_main_page(index_page):
    """
    An unified method that handles the API petition and the rendering of the main page, with page number added and without
    The API request URL is sorted in desc order
    """
    page_index = 0
    
    """ This try/except was implemented to see if the index page entered is valid to making it an incrementable index,
        otherwise, show a EMPTY list of comics in the maing page
    """
    try:
        if int(index_page) > 0:
            page_index = str(index_page) + '00'
    except:
        return ["NOT FOUND"]

    url = 'https://comicvine.gamespot.com/api/issues/?api_key=' + apikey + '&format=json' + '&sort=date_added:desc' + '&offset=' + str(page_index)
    response = requests.get(url, headers=headers)
    data = response.json()['results']
    comic_list = []
    for item in data:
        name = item['name'] if item['name'] is not None else ""
        date_time_obj = datetime.datetime.strptime(item['date_added'], '%Y-%m-%d %H:%M:%S')
        comic_list.append([item['volume']['name'], item['issue_number'], name, date_time_obj.strftime("%B %d, %Y") ,item['image']['small_url'],item['id']])
    return comic_list

if __name__ == "__main__":
    """
    MAIN Flask App"""
    app.run(host=host, port=port)