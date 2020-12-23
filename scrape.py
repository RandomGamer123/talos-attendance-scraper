import json, datetime, requests
from bs4 import BeautifulSoup
with open("config.json", "r") as config_file:
    config = json.load(config_file)
urls = []
startdate = datetime.datetime.strptime(config["startdate"], "%Y/%m/%d")
enddate = datetime.datetime.strptime(config["enddate"], "%Y/%m/%d")
baselink = config["baselink"]
datediff = (enddate - startdate).days
sendlinksatonce = 5
for x in range(0, (datediff + 1)):
    urls.append(baselink + ((startdate + datetime.timedelta(days = x)).strftime("%Y/%m/%d")))
output = ""
headers = {str('Cookie'): str(config["cookies"])}
for i in range(0, len(urls)):
    rsp = requests.get(urls[i], headers=headers)
    soup = BeautifulSoup(rsp.text, 'html.parser')
    datacontent = str((soup.find_all("div", class_="col-lg-6", limit = 2)[1]))
    search1 = "There are no attendance objects for this student in this category."
    search2 = "Absent"
    date = urls[i][-10:]
    if (search1 in datacontent):
        output = output + date + ": " + "NO DATA \n"
        continue
    if (search2 in datacontent):
        output = output + date + ": " + "ABSENT \n"
        continue
    output = output + date + ": " + "PRESENT \n"
with open ("output.txt", "w") as output_file:
    output_file.write(output)