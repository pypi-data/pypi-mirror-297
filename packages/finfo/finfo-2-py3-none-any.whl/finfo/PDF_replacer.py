import requests
import os
import json
from datetime import date
from finfo.exceptions import InvalidCategory, InvalidSeason

# Get the absolute path to the directory containing this script
current_dir = os.path.dirname(os.path.abspath(__file__))

# Getting the path to the JSON file
historical_rankings = os.path.join(current_dir, "historical_rankings.json")


# Todays date
today = date.today()

# Getting the JSON data
with open(historical_rankings, "r") as file:
    content = file.read()
    if content.strip():  # Check if the file is not empty
        json_data = json.loads(content)
    else:
        raise ValueError("The JSON file is empty!")


# Getting the categories
categories = [category[:-4] for seasons in json_data.values() for category in seasons]


# function for downloading all files (with no arguments needed)
def _download_pdfs(urls, season):

    # Construct the absolute path to the pdf directory within your package
    pdf_dir = os.path.join(current_dir, 'pdf')

    sucess = 0
    failed = 0

    # Creating the PDF folder if it does not exist
    if not os.path.exists(pdf_dir):
        os.mkdir(pdf_dir)

    # Send GET request
    for key, value in urls.items():

        # Getting the pdf from ophardt
        response = requests.get(value.get("link")) 

        #Getting the file name
        file_name = os.path.join(pdf_dir, key)

        # Save the PDF
        if response.status_code == 200:
            sucess += 1

            # Writing the data to file in dir
            with open(file_name, "wb") as f:
                f.write(response.content)
            print(f"Downloading PDF: {file_name}")

            with open(historical_rankings, "w") as f:
                string_today = today.strftime("%Y-%m-%d")
                json_data[season][key]["date"] = string_today
                json.dump(json_data, f, indent=4)
        else:
            failed += 1
            print(response.status_code)
            print(f"Downloading PDF: {file_name} FAILED")
    print(f"Sucess {sucess}")
    print(f"Fuilure {failed}")


def _download_pdf(fencer, season, name):

    # Construct the absolute path to the pdf directory within your package
    pdf_dir = os.path.join(current_dir, 'pdf')

    # Creating the PDF folder if it does not exist
    if not os.path.exists(pdf_dir):
        os.mkdir(pdf_dir)

    try:
        response = requests.get(fencer.get("link"), timeout=10)  # Adjust timeout as needed
        response.raise_for_status()  # Raise an exception for 4xx/5xx errors
    except requests.exceptions.RequestException as e:
        print(f"Error downloading {name}: {e}")
        return

    #Getting the file name
    file_name = os.path.join(pdf_dir, name)

    # Save the PDF
    if response.status_code == 200:

        # Creating the file
        with open(file_name, "wb") as f:
            f.write(response.content)
            print(f"Downloading PDF: {file_name}")

        # Giving it todays date as date value
        with open(historical_rankings, "w") as f:
            string_today = today.strftime("%Y-%m-%d")
            json_data[season][name]["date"] = string_today
            json.dump(json_data, f, indent=4)
    else:
        print(response.status_code)
        print(f"Downloading PDF: {file_name} FAILED")

        
def download_pdf(name):
    name = f"{name}.pdf"
    for season in json_data:
        if name in json_data[season]:
            fencer = json_data[season][name]
            return(_download_pdf(fencer, season, name))

    raise InvalidCategory(name, categories)


def download_pdfs(season):
    if season not in json_data.keys():
        raise InvalidSeason(season, json_data.keys())
    else:
        urls = json_data[season]
        return(_download_pdfs(urls, season))

