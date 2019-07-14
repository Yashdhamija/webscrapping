import requests, re
from bs4 import BeautifulSoup
import pandas

#Get the first page to extract page numbers
r=requests.get("http://www.pyclass.com/real-estate/rock-springs-wy/LCWYROCKSPRINGS/",
headers={'User-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0'})
# Parse the data as html document
soup=BeautifulSoup(r.content,"html.parser")

page_nr=soup.find_all("a",{"class":"Page"})[-1].text
# print(page_nr,"number of pages were found")

# The list for containing dictionary of content
l=[]

base_url="http://www.pyclass.com/real-estate/rock-springs-wy/LCWYROCKSPRINGS/t=0&s="
for page in range(0,int(page_nr)*10,10):
    r=requests.get(base_url+str(page)+".html",
    headers={'User-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0'})

    soup=BeautifulSoup(r.content,"html.parser")
    # get all the div tags containing description of properties
    divs=soup.find_all("div",{"class":"propertyRow"})
    for div in divs:
        # dictionary of content of form, Feature:Value
        d={}
        d["Address"]=div.find_all("span",{"class":"propAddressCollapse"})[0].text
        try:
            d["Locality"]=div.find_all("span",{"class":"propAddressCollapse"})[1].text
        except:
            d["Locality"]=None

        d["Price"]=div.find("h4",{"class":"propPrice"}).text.replace("\n","").replace(" ","")

        try:
            d["Beds"]=div.find("span",{"class":"infoBed"}).find("b").text
        except:
            d["Beds"]=None

        try:
            d["Area"]=div.find("span",{"class":"infoSqFt"}).find("b").text
        except:
            d["Area"]=None

        try:
            d["Full Baths"]=div.find("span",{"class":"infoValueFullBath"}).find("b").text
        except:
            d["Full Baths"]=None

        try:
            d["Half Baths"]=div.find("span",{"class":"infoValueHalfBath"}).find("b").text
        except:
            d["Half Baths"]=None

        for column_group in div.find_all("div",{"class":"columnGroup"}):
            for feature_group, feature_name in zip(column_group.find_all("span",{"class":"featureGroup"}),column_group.find_all("span",{"class":"featureName"})):
                if "Lot Size" in feature_group.text:
                    d["Lot Size"]=feature_name.text

        l.append(d)

df=pandas.DataFrame(l)

df.to_csv("Output.csv")
