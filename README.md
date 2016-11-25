# Jira-to-LiquidPlanner Realtime API Integrator
# Description

a Python Flask web application for realtime integration of JIRA API and LiquidPlanner API



# Why

To make updates in JIRA and to see them in LiquidPlanner and vice-versa



# Dependencies

Flask

Python-3.5

ngrok



# How

Setup an ngrok tunnel to point to your flask app on whatever port you chose in the flask app 

Edit the script to choose the port and enter in your LiquidPlanner credentials

Setup a webhook in Jira that points to your ngrok url e.g. xxxxxx.ngrok.com/

Use JIRA as you normally would



# To-Do

Map more fields in the JIRA webhook to LiquidPlanner fields

Map LiquidPlanner webhook fields to JIRA fields

Check webhooks for last issue update timestamps to prevent infinite loops


