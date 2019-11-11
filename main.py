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
spamusers = set()
spamtexts = set()
run = True
def update_groups(groups):
    groupsjson = requests.get("https://api.groupme.com/v3/groups?token=Qd6uMeO92kqntymFmJ3czFgY9ul0VGy6CVMRmiPh").json()
    # print(json.dumps(groupsjson, indent = 4))
    if "response" in groupsjson:
        for group in groupsjson["response"]:
            group_id = group["group_id"].encode('ascii','ignore')
            member_dict = dict()
            for member in group["members"]:
                member_dict[member["user_id"]] = member["id"]
                if member["user_id"] in spamusers:
                    response = requests.post("https://api.groupme.com/v3/groups/" + str(group_id) + "/members/" + member["id"] + "/remove" + "?token=Qd6uMeO92kqntymFmJ3czFgY9ul0VGy6CVMRmiPh")

            groups[group_id] = member_dict

def spamcheck(groups, spamtexts, spamusers, userfile):
    for group_id in groups:
        messagesjson = requests.get("https://api.groupme.com/v3/groups/" + str(group_id) + "/messages?token=Qd6uMeO92kqntymFmJ3czFgY9ul0VGy6CVMRmiPh").json()
        # print(json.dumps(messagesjson, indent=4 ))
        if "response" in messagesjson:
            for message in messagesjson["response"]["messages"]:
                for spamtext in spamtexts:
                    if message["text"] != None and groups[group_id] != None:
                        if spamtext in message["text"] and ("http" in message["text"]) and (message["user_id"] in groups[group_id]):
                            response = requests.post("https://api.groupme.com/v3/groups/" + str(group_id) + "/members/" + groups[group_id][message["user_id"]] + "/remove" + "?token=Qd6uMeO92kqntymFmJ3czFgY9ul0VGy6CVMRmiPh")
                            spamusers.add(message["user_id"])
                            uf = open(userfile,"a")
                            uf.write("\n" + message["user_id"])
                            uf.close()


def update_data(spamtexts, spamusers, textfile, userfile):
    with open(textfile) as tf:
        wordlist = tf.readlines()
        for word in wordlist:
            spamtexts.add(str(word[:-2]))
    with open(userfile) as uf:
        wordlist = uf.readlines()
        for word in wordlist:
            if word[-1] == "\r" or word[-1] == "\n":
                spamusers.add(str(word[:-1]))
            else:
                spamusers.add(str(word))
    tf.close()
    uf.close()

textfile = "badtexts.txt"
userfile = "badusers.txt"
update_data(spamtexts, spamusers, textfile, userfile)
print(spamusers)
while(run):
    update_groups(groups)
    spamcheck(groups, spamtexts, spamusers, userfile)
    time.sleep(1)
