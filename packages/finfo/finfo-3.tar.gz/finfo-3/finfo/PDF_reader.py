from pypdf import PdfReader
import re
import os
import json
from datetime import datetime, date
from finfo.PDF_replacer import download_pdf
from finfo.exceptions import InvalidCategory

country_codes = {'AIN', 'VIE', 'TUN', 'JOR', 'AZE', 'BOL', 'CAN', 'TKM', 'NGR',
                 'ROU', 'GRE', 'MAR', 'UZB', 'IRI', 'NCA', 'EST', 'PHI', 'LBA',
                 'UAE', 'LBN', 'MKD', 'TPE', 'BUL', 'IRL', 'CYP', 'MGL', 'SEN',
                 'POL', 'POR', 'QAT', 'SUI', 'KSA', 'MAS', 'CZE', 'PAR', 'KGZ',
                 'TUR', 'MEX', 'BRA', 'ALG', 'IND', 'INA', 'ARM', 'PAN', 'DEN',
                 'CRC', 'ESP', 'EGY', 'THA', 'SRB', 'PUR', 'RSA', 'CHN', 'FIN',
                 'GBR', 'KUW', 'MDA', 'MAC', 'ITA', 'COD', 'AUS', 'CHI', 'ARG',
                 'ANG', 'USA', 'OMA', 'PER', 'KOR', 'FRA', 'JPN', 'NZL', 'NOR',
                 'UKR', 'SVK', 'MLT', 'HKG', 'SGP', 'COL', 'GER', 'SWE', 'ESA',
                 'JAM', 'LAT', 'VEN', 'SLO', 'LUX', 'BRN', 'GEO', 'CRO', 'BEL',
                 'AUT', 'NED', 'ISR', 'ISV', 'LTU', 'HUN', 'KAZ', 'DOM', 'ECU',
                 'GUA', 'URU', 'NIG', 'IRQ', 'GHA', 'BER', 'ISL', 'TOG', 'PAK',
                 'BAR', 'RUS', 'CPV', 'MLI', 'CIV', 'BAH', 'MRI', 'CUB', 'MNE',  # Added commas here
                 'GUY', 'TJK', 'BEN', 'PAK', 'SRI', 'KEN', 'BUR', 'HON', 'NEP',
                 'BRU', 'UGA', 'CMR', 'RWA', 'BAR', 'HAI', 'YEM', 'ARU', 'SYR',
                 'MNE', 'MON', 'SUD'}


# Get the absolute path to the directory containing this script
current_dir = os.path.dirname(os.path.abspath(__file__))

# Getting the path to the JSON file
historical_rankings = os.path.join(current_dir, "historical_rankings.json")


# Get JSON data
with open(historical_rankings, "r") as file:
    content = file.read()
    if content.strip():  # Check if the file is not empty
        json_data = json.loads(content)
    else:
        raise ValueError("The JSON file is empty!")


# Get all the categories
# :-4 so i do not get .pdf
categories = [category[:-4] for seasons in json_data.values() for category in seasons]

print(categories)

class ReadPdf:

    def __init__(self, pdf, season, category) -> None:
        self.pdf = pdf
        self.season = season
        self.category = category

    def run(self):
        try:
            self.updating_date()

            # Setting up the reader
            reader = self.set_up_reader()
            athletes_words = ReadPdf.clean_data(reader=reader)
            return ReadPdf.get_athlete(athletes_words)
        
        except Exception as e:
            print(f"An error occured: {e}")

    @staticmethod
    def clean_data(reader):
        letters_in_text = ''
        removal_start = ''
        name_country_split = r'(?<=[a-z])(?=[A-Z])'
        removal_start_pattern = r'T\d+T'

        # Getting all the text
        for i in range(len(reader.pages)):
            page = reader.pages[i].extract_text()
            letters_in_text += page

        # Splitting the text up into words so I can find the removal_start
        words_in_text = letters_in_text.split()

        # Finding the indecator for when the "athletes" actually begin coming
        for item in words_in_text:
            if re.search(removal_start_pattern, item):
                removal_start = item
                break

        # Removing everything before the "removal_start" parameter, because it has nothing to do with athletes.
        athletes_letters = letters_in_text.split(removal_start, 1)[1]

        # Removing everything after the text 'all assigned competitions' because it has nothing to do with athletes.
        athletes_letters = athletes_letters.split("all assigned competitions", 1)[0]

        #This removes all '/', numbers and '.' from the string.
        athletes_letters = re.sub(r'[./()\d]', '', athletes_letters)

        #This removes all "'" from the string.
        athletes_letters = re.sub(r"'", '', athletes_letters)

        # Sometimes the countryCode and name clumps togeter, this splits them apart, and puts a space between them.
        athletes_letters = re.sub(name_country_split, ' ', athletes_letters)

        # This splits the string up into a list.
        return athletes_letters.split()

    @staticmethod
    def get_athlete(athletes_words):
        dict_index = 1
        list_index = 0
        country_code_pattern = r'\b[A-Z]{3}\b'
        athlete_dict = {}
        
        while list_index < len(athletes_words):
            word = athletes_words[list_index]

            # Checking if the current word is a country code
            match_country = re.search(country_code_pattern, word)

            # I could split up the if statement, but if chosen to make it stay like this
            if match_country:

                # Sometimes other words can look like country codes, this is why i run this code:
                if list_index < 2 or word not in country_codes:
                    list_index += 1
                    continue

                #elif word not in country_codes:
                #    print(word)
                #   list_index += 1
                #  continue

                # here we get the athlete
                athlete = athletes_words[:list_index + 1]

                # Delete him from the list, so we dont iterate over him again
                del athletes_words[:list_index + 1]

                # Make him an dictionary
                athlete_obj = {
                    "Lastname": athlete[0].lower(),
                    "Firstname": athlete[-2].lower(),
                    "CountryCode": athlete[-1],
                    "Rank": dict_index
                }

                #Update the athlete dict
                athlete_dict[dict_index] = athlete_obj

                # Reset eerything for the next run
                dict_index += 1
                list_index = 0
                continue

            list_index += 1

        return athlete_dict
    

    def updating_date(self):
        today = date.today()

        if self.season == "2024_2025":
            with open(historical_rankings, 'w') as file:
                
                # Getting the date the pdf was downloaded
                pdf_date = json_data[self.season][self.category]["date"]

                # Turning the date string into a datetime object
                datetime_date = datetime.strptime(pdf_date,'%Y-%m-%d')
                
                # Calculating the days between today and the last download
                time_difference = datetime.today() - datetime_date
                days_difference = time_difference.days

                if (days_difference >= 7):
                    download_pdf(self.category)
                    print("Auto updating PDF to not miss changes in the ranking")

                    # Setting the last date downloaded to today
                    string_today = today.strftime("%Y-%m-%d")
                    json_data[self.season][self.category]["date"] = string_today
                
                file.seek(0)
                file.write(json.dumps(json_data))
    


    def set_up_reader(self):
        try:
            return PdfReader(self.pdf)
        except FileNotFoundError:
            download_pdf(self.category)
            print("Downloading ranking, because is it missing.")
            return PdfReader(self.pdf)


                
def read_pdf(category):
    # Construct the absolute path to the pdf directory within your package
    pdf_dir = os.path.join(current_dir, 'pdf')
    
    #Check if category exists
    if category in categories:
        file_path = os.path.join(pdf_dir, category + ".pdf")
        season = category.split(category[:-9], 1)[1]
        readpdf = ReadPdf(file_path, season, category)
        return readpdf.run()
    else:
        raise InvalidCategory(category, categories)

