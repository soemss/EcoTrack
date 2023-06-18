import pandas as pd
import requests
import lxml
from bs4 import BeautifulSoup
import os
cwd = os.getcwd()


def zip_to_county_name(zip):
    df = pd.read_csv(f'{cwd}/zip_code_database.csv')
    row_num = df[df['zip'] == zip].index[0]
    return df.at[row_num, "county"].replace(" County", ""), df.at[row_num, "state"]

site = 'https://alerts.weather.gov/cap'
def county_warnings_link(county, state):
    county_reference_link = f"{site}/{state.lower()}.php?x=3"
    county_reference_page = requests.get(county_reference_link)
    soup = BeautifulSoup(county_reference_page.text, "lxml")
    table = soup.find("table", width=700)
    all_rows = table.find_all("tr")
    for row in all_rows:
        if str(row).count(county.title()) > 0:
            split_up = str(row).split(county.title()) 
            href = split_up[0].rsplit('href="', 1)[1].split('"')[0]
            return f"{site}/{href}"

class alert():
    def __init__(self, soup, index):
        all_alert_summaries = soup.find_all("summary")
        if len(all_alert_summaries) == 0:
            self.alert = "There are no alerts for your region" 
            self.event = ""
            self.expires = ""
            self.urgency = ""
            self.severity = ""
        else:
            all_data = {"summary": all_alert_summaries}
            event = all_data["summary"][index]
            try:
                event = str(event).split(">")[1].split("<")[0]
                event_split = event.replace("* WHAT", "").replace("* WHERE", "").replace("* WHEN", "").split("...")
                self.alert = f"{event_split[1]}. Where is this happening: {event_split[4]} When is this happening: {event_split[5]}"
                self.event = str(soup.find_all("cap:event")[index]).split(">")[1].split("<")[0]
                self.expires = str(soup.find_all("cap:expires")[index]).split(">")[1].split("<")[0].replace("T", " ")
                self.urgency = str(soup.find_all("cap:urgency")[index]).split(">")[1].split("<")[0]
                self.severity = str(soup.find_all("cap:severity")[index]).split(">")[1].split("<")[0]
            except:
                self.alert = event
                self.event = str(soup.find_all("cap:event")[index]).split(">")[1].split("<")[0]
                self.expires = str(soup.find_all("cap:expires")[index]).split(">")[1].split("<")[0].replace("T", " ")
                self.urgency = str(soup.find_all("cap:urgency")[index]).split(">")[1].split("<")[0]
                self.severity = str(soup.find_all("cap:severity")[index]).split(">")[1].split("<")[0]
def all_alerts(warnings_link):
    page = requests.get(warnings_link)
    soup = BeautifulSoup(page.text, "lxml")
    all_alert_summaries = soup.find_all("summary")
    all_alert_list = []
    index = 0
    while index < len(all_alert_summaries):
        all_alert_list.append(alert(soup, index))
        index += 1
    final_dict = {}
    for aler in all_alert_list:
        dictionary = {"alert": aler.alert, "event": aler.event, "expires": aler.expires, "urgency": aler.urgency, "severity": aler.severity}
        for key, value in dictionary.items():
            final_dict.setdefault(key, []).append(value)
    return final_dict




