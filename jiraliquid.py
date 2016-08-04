import json
import os
import sys
import flask
from liquidplanner.auth import BasicCredentials
from dateutil import tz
import datetime
import liquidplanner
import jira
import time
import datetime


app = flask.Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if flask.request.method == 'POST':
        print("I got a post.....")
        jsondata = flask.request.get_json()
        print(jsondata)
        if 'webhookEvent' in jsondata.keys():
            jwebhook(jsondata)
        else:
            lwebhook(jsondata)
        return "Done"
    else:
        print(" ANOTHER GET") # see this in console
        return "GET request" # see this on page


def jwebhook(jsondata):
    credentials = BasicCredentials('email', 'password') # Entter your LiquidPlanner email and pasword
    lp = liquidplanner.LiquidPlanner(credentials)
    foundproject = 0
    print("I got a jira post")
    print("here is my jira json: {}".format(jsondata))
    if 'updated' in jsondata['webhookEvent'] or 'created' in jsondata['webhookEvent']:
        projects = lp.projects.all()
        for p in projects:
            if p['name'] in jsondata['issue']['fields']['project']['name']:
                id = p['id']
                task = lp.tasks.create({'name': jsondata['issue']['fields']['summary'], "parent_id": int(id),
                                        "project_id": int(id), "description": jsondata['issue']['fields']['summary']})
                foundproject = 1
                break
            else:
                foundproject -= 1
        if foundproject < 0:
            print("I have to create a project for the issue now")
            proj = lp.projects.create({'name': jsondata['issue']['fields']['project']['name']})
            print("yay I created a project")
            print(proj)
            id = proj['id']
            task = lp.tasks.create(
                {'name': jsondata['issue']['fields']['summary'], "parent_id": int(id),
                 "description": jsondata['issue']['fields']['summary']})
            print(task)
            print("done")
    return "JIRA Webhook Accepted"


def lwebhook(jsondata):
    print("I got a liquidplanner post")
    return "LiquidPlanner Webhook Accepted"

def jiratoliquiddate(aa): # for use when adding a date from JIRA to LiquidPlanner
    z = aa.split("-")
    year = int(z[0])
    month = int(z[1])
    zz = z[2].split("T")
    day = int(zz[0])
    nz = zz[1][:-4]
    nzz = nz.split(":")
    hour = int(nzz[0])
    minute = int(nzz[1])
    second = int(nzz[2])
    return datetime.datetime(year, month, day, hour, minute, second, tzinfo=tz.tzutc())


if __name__ == '__main__':
    app.run(port=5000, threaded=True)
