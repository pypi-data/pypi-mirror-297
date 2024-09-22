from finfo.PDF_reader import read_pdf, country_codes, categories

class FIE:

    def __init__(self, category) -> None:
        self.fencers = read_pdf(category)
        print(self.fencers)


    def find_fencer_by_rank(self, rank):
        if len(self.fencers) < rank or rank == 0:
            raise "No such rank"
        else:
            return self.fencers.get(rank)
        

    def find_fencer_by_name(self, firstname, lastname):
        for inside_dict in self.fencers.values():
            if firstname and lastname in inside_dict.values():
                return inside_dict
        return (f"no such fencer named: {firstname} {lastname}")
    

    def all_athletes(self):
        return self.fencers
    

    def get_all_fencers_from_country(self, countrycode):
        fencers_from_country = []
        
        if countrycode not in country_codes:
            raise "not a valid countrycode"
        
        for insidedict in self.fencers.values():
            if insidedict["CountryCode"] == countrycode:
                fencers_from_country.append(insidedict)
            else:
                continue
        return fencers_from_country


def all_fencing_categories():
        return categories

def all_valid_countrycodes():
        return country_codes
