#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 12 18:45:22 2025

@author: spanichella
"""
#!pip install xmltodict

#requirement "pip install requests xmltodict geopy folium" and "pip install xmltodict"
#requirement "conda install -c conda-forge xmltodict"
# python -m pip install xmltodict
#python -c "import xmltodict;
#pip3 install requests
#pip install folium
#pip install geopy
#pip install beautifulsoup4
#pip install scholarly
# pip install googlesearch-python
#pip install pycountry 
# pip install time
#pip install GeoText
#pip install google-api-python-client
# pip install scholarly  fuzzywuzzy
# pip install wikipedia
# pip install requests beautifulsoup4 scholarly selenium webdriver-manager
#pip install folium geopy

##PART 1

import numpy

import requests
import xmltodict

# Function to fetch co-authors from DBLP using XML format
def get_coauthors(author_name):
    search_url = f"https://dblp.org/search/author/api?q={author_name}&format=json"
    
    # Fetch author search results
    response = requests.get(search_url)
    if response.status_code != 200:
        print(f"Error fetching author data: HTTP {response.status_code}")
        return []

    data = response.json()
    if "result" not in data or "hits" not in data["result"]:
        print("DBLP API returned unexpected format.")
        return []

    # Extract author ID (PID) from the DBLP result
    authors = data["result"]["hits"]["hit"]
    if not authors:
        print("Author not found in DBLP.")
        return []

    author_info = authors[0]["info"]
    if "url" not in author_info:
        print("Author URL not found in DBLP data.")
        return []
    
    # Correct the author ID format based on the link structure
    author_url = author_info["url"]
    print(f"Extracted Author URL: {author_url}")  # Debugging output

    # The author_id from the URL should be split properly
    author_id_parts = author_url.split("/")
    if len(author_id_parts) < 3:
        print("Error: Unable to extract correct author ID from URL.")
        return []
    
    # Correct the author ID (use the appropriate PID format)
    author_id = author_id_parts[-2] + "/" + author_id_parts[-1]
    print(f"Correct Author ID: {author_id}")  # Debugging output

    # Fetch the author's publications in XML format
    publications_url = f"https://dblp.org/pid/{author_id}.xml"
    print(f"Fetching publications from URL: {publications_url}")  # Debugging output

    pub_response = requests.get(publications_url)
    if pub_response.status_code != 200:
        print(f"Error fetching publications: HTTP {pub_response.status_code}")
        return []

    # Print out the raw XML response for debugging
    print(pub_response.text)  # Debugging output to see the raw XML

    # Parse the XML response
    try:
        pub_data = xmltodict.parse(pub_response.content)
    except Exception as e:
        print(f"Error parsing XML data: {e}")
        return []

    coauthors = set()

    # Extract co-authors from the publications data
    if "dblpperson" in pub_data and "r" in pub_data["dblpperson"]:
        records = pub_data["dblpperson"]["r"]
        if isinstance(records, list):  # Multiple records
            for record in records:
                pub = record.get("article") or record.get("inproceedings") or {}
                authors = pub.get("author", [])
                if isinstance(authors, list):
                    # Loop through the authors list and add individual author names
                    for author in authors:
                        if isinstance(author, str):
                            coauthors.add(author)
                        elif isinstance(author, dict) and "text" in author:
                            coauthors.add(author["text"])
                elif isinstance(authors, str):  # Single author case
                    coauthors.add(authors)

    coauthors.discard(author_name)  # Remove self from co-author list
    return list(coauthors)

# Function to save co-authors to a file in the format "Name Surname"
def save_coauthors_to_file(coauthors, filename="coauthors.txt"):
    with open(filename, "w") as file:
        for coauthor in coauthors:
            # Split the name into first name and surname (this assumes names are in "Name Surname" format)
            name_parts = coauthor.strip().split(" ")
            if len(name_parts) > 1:
                # If the name contains more than one part, assume the last part is the surname
                first_name = " ".join(name_parts[:-1])
                surname = name_parts[-1]
                file.write(f"{first_name} {surname}\n")
            else:
                # In case the name only contains a single part, treat it as first name or surname
                file.write(f"{name_parts[0]}\n")
    print(f"Co-authors saved to {filename}")

# Function to generate a list of names and surnames in the format "Name Surname"
def generate_name_surname_list(coauthors):
    name_surname_list = []
    for coauthor in coauthors:
        name_parts = coauthor.strip().split(" ")
        if len(name_parts) > 1:
            # If the name contains more than one part, assume the last part is the surname
            first_name = " ".join(name_parts[:-1])
            surname = name_parts[-1]
            name_surname_list.append(f"{first_name} {surname}")
        else:
            # In case the name only contains a single part, treat it as first name or surname
            name_surname_list.append(f"{name_parts[0]}")
    return name_surname_list

# Main function to fetch and save the co-authors
def generate_coauthors_file(author_name):
    coauthors = get_coauthors(author_name)
    
    if not coauthors:
        print("No co-authors found or DBLP API error.")
        return
    
    # Generate the list of names and surnames
    name_surname_list = generate_name_surname_list(coauthors)
    
    # Print the list of names and surnames
    print("List of co-authors (Name Surname):")
    for name_surname in name_surname_list:
        print(name_surname)
    
    # Save the co-authors to a file
    save_coauthors_to_file(coauthors)

# Run the script
author_name = "Sebastiano Panichella"  # Change this to your target author
generate_coauthors_file(author_name)



#### PART 2


import requests
from bs4 import BeautifulSoup
from googlesearch import search
import time

authors = [
    "Aaron Visaggio", "Adelina Ciurumelea", "Alberto Bacchelli", "Alessandra Gorla", "Alessio Gambi", 
    "Alexander Boll", "Alexander Egyed", "Alexander Serebrenik", "Andrea De Lucia", "Andrea Di Sorbo", 
    "Andreas Schaufelbühl", "Andrian Marcus", "Andy Zaidman", "Anand Ashok Sawant", "Annibale Panichella", 
    "Antonio Martini 0001", "Arianna Blasi", "Arnaud Beller", "Atif Mashkoor", "Bill Bosshard", "Carmine Vassallo", 
    "Carol V. Alexandru", "Changzhi Wang", "Charith Munasinghe", "Christian Birchler", "Christoph Laaber", 
    "Christoph Mayr-Dorn", "Chuyue Wu", "Cyrill Rohrbach", "Damian A. Tamburri", "Daniele Romano", 
    "Danielle Gonzalez", "David Lo 0001", "Davide Taibi 0001", "Diego Martín", "Emitza Guzman", "Fabio Palomba", 
    "Fatemeh Mohammadi Amin", "Fiorella Zampetti", "Filomena Ferrucci", "Fitsum Meshesha Kifetew", 
    "Francesco Mercaldo", "Gabriele Bavota", "Gerald Schermann", "Gerardo Canfora", "Giovanni Capobianco", 
    "Giovanni Grano", "Giovani Guizzo", "Giuliano Antoniol", "Gordon Fraser 0001", "Gregorio Robles", 
    "Harald C. Gall", "Hyeongkyun Kim", "Jairo Aponte", "Jens Horneber", "Jeremy Daly", "Jitong Zhao", 
    "José J. Merchante", "Josef Spillner", "Juan P. Galeotti", "Junji Shimagaki", "Liliana Pasquale", 
    "Lucas Pelloni", "Maggie Ma", "Maliheh Izadi", "Manuel Leuenberger", "Marcela Ruiz", "Martin Brandtner", 
    "Massimiliano Di Penta", "Mathias Birrer", "Mehdi Mirakhorli", "Meiyappan Nagappan", "Mohammad Ghafari", 
    "Mohammad Imranur Rahman", "Mohammed Al-Ameen", "Moritz Beller", "Muhammad Ilyas Azeem", "Nataliia Stulova", 
    "Nicolas Erni", "Nicolas Ganz", "Nik Zaugg", "Nikolaos Tsantalis", "Norbert Seyff", "Oscar Chaparro", 
    "Oscar Nierstrasz", "Pablo Valenzuela-Toledo", "Paolo Tonella", "Pasquale Salza", "Philipp Leitner 0001", 
    "Pooja Rani 0001", "Pouria Derakhshanfar", "Prasun Saurabh", "Rafael Kallis", "René Just", "Ritu Kapur", 
    "Rocco Oliveto", "Roman Machácek", "Saghan Mudbhari", "Sajad Khatiri", "Sandro Hernandez", "Sebastian Proksch 0001", 
    "Stefano Giannantonio", "Stephan Lukasczyk", "Taolue Chen 0001", "Tanzil Kombarabettu Mohammed", 
    "Teodora Nechita", "Tianhai Liu", "Timofey V. Titov", "Timo Blattner", "Timo Kehrer", "Timothy Zimmermann", 
    "Usman Ashraf", "Valentina Lenarduzzi", "Venera Arnaoudova", "Vincenzo Riccio", "Vincent J. Hellendoorn", 
    "Xavier Devroey", "Xin Yan", "Yanqi Su", "Yu Zhou 0010", "Zhiqiu Huang", "Ziyi Zhang"
]

# Complete list of countries
countries = [
    "Afghanistan", "Albania", "Algeria", "Andorra", "Angola", "Antigua and Barbuda", "Argentina",
    "Armenia", "Australia", "Austria", "Azerbaijan", "Bahamas", "Bahrain", "Bangladesh", "Barbados",
    "Belarus", "Belgium", "Belize", "Benin", "Bolivia", "Bosnia and Herzegovina", "Botswana", "Brazil",
    "Brunei", "Bulgaria", "Burkina Faso", "Burma", "Burundi", "Cambodia", "Cameroon", "Canada", "Chile",
    "China", "Colombia", "Comoros", "Congo", "Costa Rica", "Croatia", "Cuba", "Cyprus", "Czechia",
    "Democratic Republic of the Congo", "Denmark", "Djibouti", "Dominica", "Dominican Republic", "Ecuador",
    "Egypt", "El Salvador", "Estonia", "Eswatini", "Ethiopia", "Fiji", "Finland", "France", "Gabon", "Gambia",
    "Georgia", "Germany", "Greece", "Grenada", "Guatemala", "Guinea", "Guinea-Bissau", "Guyana", "Haiti", "Honduras",
    "Hungary", "Iceland", "India", "Indonesia", "Iran", "Iraq", "Ireland", "Israel", "Italy", "Jamaica", "Japan",
    "Jordan", "Kazakhstan", "Kenya", "Kosovo", "Kuwait", "Kyrgyzstan", "Laos", "Latvia", "Lebanon", "Liberia",
    "Libya", "Liechtenstein", "Lithuania", "Luxembourg", "Malaysia", "Malta", "Mexico", "Moldova", "Monaco", "Morocco",
    "Mozambique", "Namibia", "Nepal", "Netherlands", "New Zealand", "Nigeria", "North Macedonia", "Norway", "Pakistan",
    "Panama", "Papua New Guinea", "Paraguay", "Peru", "Philippines", "Poland", "Portugal", "Qatar", "Romania", "Russia",
    "Rwanda", "Saudi Arabia", "Senegal", "Serbia", "Singapore", "Slovakia", "Slovenia", "South Africa", "South Korea",
    "Spain", "Sri Lanka", "Sudan", "Sweden", "Switzerland", "Syria", "Tajikistan", "Tanzania", "Thailand", "Turkey", "Uganda",
    "Ukraine", "United Kingdom", "United States", "Uruguay", "Uzbekistan", "Venezuela", "Vietnam", "Yemen", "Zambia", "Zimbabwe"
]


# Known affiliations
known_affiliations = {
    "Giuliano Antoniol": "Polytechnique Montréal, Canada",
    "Gabriele Bavota": "Università della Svizzera italiana, Switzerland",
    "Oscar Nierstrasz": "University of Bern, Switzerland",
    "Massimiliano Di Penta": "University of Sannio, Italy",
    "Fabio Palomba": "University of Salerno, Italy",
    "Alberto Bacchelli": "University of Zurich, Switzerland"
}

# # Function to extract affiliation using Google Search
# def get_affiliation_google(author):
#     if author in known_affiliations:
#         return known_affiliations[author]
    
#     query = f"{author} affiliation"
#     try:
#         for url in search(query, num_results=5):  # Get top 5 results
#             response = requests.get(url, timeout=5)
#             soup = BeautifulSoup(response.text, 'html.parser')
            
#             # Try extracting university/institution from meta tags or paragraphs
#             for tag in soup.find_all(['p', 'span', 'div']):
#                 text = tag.get_text()
#                 if any(keyword in text.lower() for keyword in ["university", "institute", "lab", "research center"]):
#                     return text
#             time.sleep(1)  # Avoid hitting Google's rate limit
#     except:
#         return "Unknown"
#     return "Unknown"

# # Function to extract affiliation from Researchr Conference pages
# def get_affiliation_researchr(author):
#     query = f"{author} site:conf.researchr.org"
#     try:
#         for url in search(query, num_results=3):  # Get top 3 results from Researchr
#             response = requests.get(url, timeout=5)
#             soup = BeautifulSoup(response.text, 'html.parser')
            
#             # Look for country or institution in paragraphs/divs
#             for tag in soup.find_all(['p', 'span', 'div']):
#                 text = tag.get_text()
#                 if any(keyword in text.lower() for keyword in ["university", "institute", "lab", "research center", "country"]):
#                     return text
#             time.sleep(1)  # Avoid hitting Google's rate limit
#     except:
#         return "Unknown"
#     return "Unknown"

# # Function to map affiliations to countries
# def map_affiliation_to_country(affiliation):
#     country_mapping = {
#         "ETH Zurich": "Switzerland",
#         "University of Toronto": "Canada",
#         "National University of Singapore": "Singapore",
#         "Stanford University": "United States",
#         "University of Tokyo": "Japan",
#         "Polytechnique Montréal": "Canada",
#         "Università della Svizzera italiana": "Switzerland",
#         "University of Bern": "Switzerland",
#         "University of Sannio": "Italy",
#         "University of Salerno": "Italy",
#         "University of Zurich": "Switzerland"
#     }
#     for key in country_mapping:
#         if key.lower() in affiliation.lower():
#             return country_mapping[key]
#     return "Unknown"

# # Mapping authors to countries
# author_location_map = {}
# #for author in authors:
# for i in (range(numpy.size(authors)-1)):
#     author = authors[i]
#     print(author+ " under analysis" + " author "+str(i+1)+" out of "+str(numpy.size(authors)))
#     affiliation = get_affiliation_researchr(author)
#     if affiliation == "Unknown":
#         affiliation = get_affiliation_google(author)
    
#     country = map_affiliation_to_country(affiliation)
#     author_location_map[author] = country

# # Print results
# for author, country in author_location_map.items():
#     print(f"{author}: {country}")


##PART 3 - create map

import folium
import time
from geopy.geocoders import Nominatim

# List of collaborators and their countries
collaborators = {
    "Aaron Visaggio": "Italy",
    "Adelina Ciurumelea": "Switzerland",
    "Alberto Bacchelli": "Switzerland",
    "Alessandra Gorla": "Spain",
    "Alessio Gambi": "Austria",
    "Alexander Boll": "Switzerland",
    "Alexander Egyed": "Austria",
    "Alexander Serebrenik": "Netherlands",
    "Andrea De Lucia": "Italy",
    "Andrea Di Sorbo": "Italy",
    "Andreas Schaufelbühl": "Switzerland",
    "Andrian Marcus": "USA",
    "Andy Zaidman": "Netherlands",
    "Anand Ashok Sawant": "USA",
    "Annibale Panichella": "Netherlands",
    "Antonio Martini": "Norway",
    "Arianna Blasi": "Switzerland",
    "Arnaud Beller": "Netherlands",
    "Atif Mashkoor": "USA",
    "Bill Bosshard": "Canada",
    "Carmine Vassallo": "Switzerland",
    "Carol V. Alexandru": "Switzerland",
    "Changzhi Wang": "China",
    "Charith Munasinghe": "Switzerland",
    "Christian Birchler": "Switzerland",
    "Christoph Laaber": "Norway",
    "Christoph Mayr-Dorn": "Austria",
    "Chuyue Wu": "Switzerland",
    "Cyrill Rohrbach": "Switzerland",
    "Damian A. Tamburri": "Italy",
    "Daniele Romano": "Switzerland",
    "Danielle Gonzalez": "USA",
    "David Lo": "Singapore",
    "Davide Taibi": "Finland",
    "Diego Martín": "Switzerland",
    "Emitza Guzman": "Germany",
    "Fabio Palomba": "Italy",
    "Fatemeh Mohammadi Amin": "Switzerland",
    "Fiorella Zampetti": "Canada",
    "Filomena Ferrucci": "Canada",
    "Fitsum Meshesha Kifetew": "Italy",
    "Francesco Mercaldo": "Italy",
    "Gabriele Bavota": "Switzerland",
    "Gerald Schermann": "Switzerland",
    "Gerardo Canfora": "Italy",
    "Giovanni Capobianco": "Italy",
    "Giovanni Grano": "Switzerland",
    "Giovani Guizzo": "UK",
    "Giuliano Antoniol": "Canada",
    "Gordon Fraser": "Germany",
    "Gregorio Robles": "Spain",
    "Harald C. Gall": "Switzerland",
    "Hyeongkyun Kim": "Switzerland",
    "Jairo Aponte": "Colombia",
    "Jens Horneber": "Switzerland",
    "Jeremy Daly": "USA",
    "Jitong Zhao": "China",
    "José J. Merchante": "USA",
    "Josef Spillner": "Switzerland",
    "Juan P. Galeotti": "Argentina",
    "Junji Shimagaki": "Japan",
    "Liliana Pasquale": "Ireland",
    "Lucas Pelloni": "Switzerland",
    "Maggie Ma": "Canada",
    "Maliheh Izadi": "Canada",
    "Manuel Leuenberger": "Switzerland",
    "Marcela Ruiz": "Switzerland",
    "Martin Brandtner": "Switzerland",
    "Massimiliano Di Penta": "Canada",
    "Mathias Birrer": "Switzerland",
    "Mehdi Mirakhorli": "Hawaii",
    "Meiyappan Nagappan": "Canada",
    "Mohammad Ghafari": "Canada",
    "Mohammad Imranur Rahman": "Switzerland",
    "Mohammed Al-Ameen": "Germany",
    "Moritz Beller": "Netherlands",
    "Muhammad Ilyas Azeem": "Luxembourg",
    "Nataliia Stulova": "Switzerland",
    "Nicolas Erni": "Switzerland",
    "Nicolas Ganz": "Switzerland",
    "Nik Zaugg": "Switzerland",
    "Nikolaos Tsantalis": "Canada",
    "Norbert Seyff": "Switzerland",
    "Oscar Chaparro": "USA",
    "Oscar Nierstrasz": "Switzerland",
    "Pablo Valenzuela-Toledo": "Switzerland",
    "Paolo Tonella": "Switzerland",
    "Pasquale Salza": "Switzerland",
    "Philipp Leitner": "Sweden",
    "Pooja Rani": "Switzerland",
    "Pouria Derakhshanfar": "Netherlands",
    "Prasun Saurabh": "Switzerland",
    "Rafael Kallis": "Switzerland",
    "René Just": "USA",
    "Ritu Kapur": "Italy",
    "Rocco Oliveto": "Italy",
    "Roman Machácek": "Switzerland",
    "Saghan Mudbhari": "USA",
    "Sajad Khatiri": "Switzerland",
    "Sebastian Proksch": "Netherlands",
    "Stefano Giannantonio": "Italy",
    "Stephan Lukasczyk": "Germany",
    "Taolue Chen": "UK",
    "Timofey V. Titov": "Switzerland",
    "Timo Blattner": "Switzerland",
    "Timo Kehrer": "Switzerland",
    "Timothy Zimmermann": "Switzerland",
    "Usman Ashraf": "Pakistan",
    "Valentina Lenarduzzi": "Finland",
    "Venera Arnaoudova": "USA",
    "Vincenzo Riccio": "Italy",
    "Vincent J. Hellendoorn": "USA",
    "Xavier Devroey": "Belgium",
    "Xin Yan": "China",
    "Yanqi Su": "China",
    "Yu Zhou": "China",
    "Zhiqiu Huang": "China",
    "Tahereh Zohdinasab": "Switzerland",
    "Victor Crespo Rodriguez":"Australia",
    "Neelofar":"Australia",
    "Atefeh Rohani":"Switzerland", 
    "Gregorio Dalia":"Italy", 
    "Alexander Boll":"Switzerland", 
    "Sandro Hernandez Goicochea":"Switzerland",  
    "Aldeida Aleti":"Australia",
    "Catia Trubiani":"Italy", 
    "Anna Rita Fasolino":"Italy", 
    "Alexandre Bergel":"Chile", 
    "Sasa Miladinovic":"Switzerland", 
    # Company collaborations
    "Genedata (Biopharma R&D)": "Switzerland",
    "Terraview (Agriculture)": "Switzerland",
    "Stadler Signalling AG (Mobility)": "Switzerland",
    "ANYbotics (Autonomous robots)": "Switzerland",
    "LEDCity (AI Lighting)": "Switzerland",
    "BeamNG (Self-driving simulation)": "Germany",
    "ARQUIMEA (Autonomous vehicles)": "Spain",
    "BOND (E-bikes)": "Switzerland",
    "Helio (Computation)": "Switzerland",
    "Siemens Healthcare GmbH (e-Health)": "Germany",
    "Intelligentia S.r.l. (Aerospace)": "Italy",
    "AICAS GmbH (Automotive)": "Germany",
    "Q-media s.r.o. (Railways)": "Czech Republic",
    "Unparallel Innovation (Water-smart systems)": "Portugal",
    "The Open Group (Tech standards)": "Belgium",
    "Siemens AG (DevOps provider)": "Germany",
    "GMV (Aviation)": "Spain",
    "Red Hat (DevOps)": "Switzerland",
    "Swisscom": "Switzerland",
    "VSHN (DevOps)": "Switzerland",
    "Ikubinfo (DevOps)": "Austria",
    "ING Netherlands": "Netherlands",
    "Sony Mobile Communications": "Japan"
}

# Initialize the map
m = folium.Map(location=[20, 0], zoom_start=2)

# Initialize geolocator
geolocator = Nominatim(user_agent="geoapi")

# Add points to the map
for name, country in collaborators.items():
    try:
        location = geolocator.geocode(country)
        if location:
            folium.Marker(
                location=[location.latitude, location.longitude],
                popup=name,
                tooltip=country
            ).add_to(m)
        time.sleep(1)  # Avoid excessive API requests
    except:
        pass

# Save the map to an HTML file
m.save("collaborator_map.html")
print("Map saved as 'collaborator_map.html'. Open in a browser to view.")
