import os
os.system("color")
class color:
   PURPLE = '\033[95m'
   GREEN = '\033[92m'
   BLUE = '\033[94m' 
   BOLD = '\033[1m'
   END = '\033[0m'

import requests
from bs4 import BeautifulSoup

# Asks for a valid url and if the link given is not valid it asks for a valid URL
response = requests.get(url=input("Enter your Wikipedia Article Link Here"),)
while(response.status_code!=200):
    response = requests.get(url=input("Enter a valid Wikipedia Article Link Here"),)

#puts the json into a easy to read html file
soupHelper = BeautifulSoup(response.content,'html.parser')

#This just grabs the heading of the article and then prints it out
title = soupHelper.find(id="firstHeading")
print("\n"+color.PURPLE+"The title of this page is ",title.string+color.END)

#Gets all of the content in the wikipedia page
body =soupHelper.find(id="mw-content-text")

#This is all of the stop words according to NTLK
textFile = open("english.txt", "r")
stopWords = textFile.read()
stopWords_list = stopWords.split("\n")
textFile.close()

#creates an empty dictionary that I will populate later in the code
dictionary = {}

#creates an empty list for links
links=[]

#Lists through all of the tags it finds useful becuase some tags lead to non useful and sometimes damaging text
for tag in body.find_all(['h2','p','ul','ol','dl','a']):
    #First looks for anything that has the a tag which means link
    if tag.name=='a':
        #Then as long as the link is populated and it doesnt start with a # add it to the list we created earlier
        if tag.get('href') and not tag.get('href')[0] == '#':
            #Unshorted the link to make it easy to navigate to
            newLink = tag.get('href').replace('/wiki/','https://en.wikipedia.org/wiki/')
            links.append(newLink)
    #Second look for all of the headers which is the tag of h2 which is the header size wikipedia uses for all of its headers
    elif tag.name == 'h2':
        #This is where we print out the information about the last section to insure it has went over every single tag it could
        if dictionary:
            dictionary=dict(sorted(dictionary.items(), key=lambda x: x[1], reverse=True))
            print(color.BLUE+"The word that appears the most in this section is:"+color.GREEN+"",list(dictionary.keys())[0],""+color.BLUE+"and it appears"+color.GREEN+"",dictionary[list(dictionary.keys())[0]],""+color.BLUE+"times"+color.END)
            print ('\n'.join(links))
        #Here we clear all of the lits and dictionaries to prepare for a new section
        links.clear()
        dictionary.clear()
        newString = tag.text.replace('[edit]', '')
        print(color.BLUE+"\nThe title of this section is: "+color.GREEN+"",newString+""+color.END)
    #Lastly it looks for everything that is not a link nor a header
    elif tag.text!="\n" and tag.text!="" and tag.text!=" ":
        #I split the text by a space to be able to iterate through every word
        for word in tag.text.split(" "):
            #Then if the word is not already in the dictionary I add it and if it is I just increment the count 
            if word.lower() not in stopWords_list:
                if dictionary.get(word.lower()):
                    dictionary[word.lower()]+=1
                else:
                    dictionary[word.lower()]=1

#This is just to print out the last section because I usally print it out right before the next section
dictionary=dict(sorted(dictionary.items(), key=lambda x: x[1], reverse=True))
print(color.BLUE+"The word that appears the most in this section is:"+color.GREEN+"",list(dictionary.keys())[0],""+color.BLUE+"and it appears"+color.GREEN+"",dictionary[list(dictionary.keys())[0]],""+color.BLUE+"times"+color.END)
print ('\n'.join(links))
input("Press any Key to End")
