import requests
import json
import time
import re

#Notes
# Store the message to read from for each group as a json file and update and
# access it when reqruired
#In the future it could be useful to keep track of members by storing them
#and making additive and removal changes

groups = dict(dict())
spamtexts = {"Essay Writing", "Essay Writer"}
run = True
def update_groups(groups):
    groupsjson = requests.get("https://api.groupme.com/v3/groups?token=Qd6uMeO92kqntymFmJ3czFgY9ul0VGy6CVMRmiPh").json()
    # print(json.dumps(groupsjson, indent = 4))
    for group in groupsjson["response"]:
        group_id = group["group_id"]
        member_dict = dict()
        for member in group["members"]:
            member_dict[member["user_id"]] = member["id"]
        groups[group_id] = member_dict

def spamcheck(groups, spamtexts):
    for group_id in groups:
        messagesjson = requests.get("https://api.groupme.com/v3/groups/" + str(group_id) + "/messages?token=Qd6uMeO92kqntymFmJ3czFgY9ul0VGy6CVMRmiPh").json()
        for message in messagesjson["response"]["messages"]:
            for spamtext in spamtexts:
                if spamtext in message["text"] and (message["user_id"] in groups[group_id]):
                    response = requests.post("https://api.groupme.com/v3/groups/" + str(group_id) + "/members/" + groups[group_id][message["user_id"]] + "/remove" + "?token=Qd6uMeO92kqntymFmJ3czFgY9ul0VGy6CVMRmiPh")


while(run):
    update_groups(groups)
    spamcheck(groups, spamtexts)
    time.sleep(1)
"""

tok = "Qd6uMeO92kqntymFmJ3czFgY9ul0VGy6CVMRmiPh"
group_id = "groups/50093480/"
task = "messages"
messageurl = "https://api.groupme.com/v3/" + group_id + task + "?token=" + tok
memberurl  = "https://api.groupme.com/v3/groups/50093480?token=Qd6uMeO92kqntymFmJ3czFgY9ul0VGy6CVMRmiPh"
removeurl = "https://api.groupme.com/v3/groups/50093480/members/"


while(true):
    memberjson = requests.get(memberurl).json()
    members = memberjson["response"]["members"]

    member_dict = dict()
    for member in members:
        member_dict[member["user_id"]] = member["id"]

    messagejson = requests.get(messageurl).json()
    messages = messagejson["response"]["messages"]

    for message in messages:
        for spam in spamtexts:
            if (spam in message["text"]) and (message["user_id"] in member_dict):
                url = removeurl + member_dict[message["user_id"]] + "/remove" + "?token=" + tok
                response = requests.post(url)
                print(response)

    time.sleep(3)
"""
