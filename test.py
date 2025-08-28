import csv
import random
from names_dataset import NameDataset
from unidecode import unidecode

class NameGenerator:
    def __init__(self):
        self.dataset = NameDataset(load_first_names=True, load_last_names=True)
        # Build dict: country -> first names by gender
        self.first_names_by_country = self._load_first_names()
        # Build dict: country -> last names
        self.last_names_by_country = self._load_last_names()

    def _load_first_names(self):
        result = {}
        top_names_dict = self.dataset.get_top_names(n=500)
        for country, gender_names in top_names_dict.items():
            names_dict = {}
            for gender in ['F', 'M']:
                names_list = gender_names.get(gender, [])
                cleaned = [unidecode(n).strip() for n in names_list if unidecode(n).strip().replace(' ', '').isalpha()]
                if cleaned:
                    names_dict[gender] = cleaned
            if names_dict:
                result[country] = names_dict
        return result

    def _load_last_names(self):
        result = {}
        last_names_dict = self.dataset.get_top_names(n=500, use_first_names=False)
        for country, names_list in last_names_dict.items():
            cleaned = [unidecode(n).strip() for n in names_list if unidecode(n).strip().replace(' ', '').isalpha()]
            if cleaned:
                result[country] = cleaned
        return result

    def generate_name(self):
        countries = list(self.first_names_by_country.keys())
        weights = [85 if c == 'AU' else 15 for c in countries]
        country = random.choices(countries, weights=weights, k=1)[0]

        # Choose gender
        gender = random.choice(['F', 'M'])
        first_name_list = self.first_names_by_country[country].get(gender)
        if not first_name_list:  # fallback if no names for gender in country
            first_name_list = self.first_names_by_country[country]['M'] + self.first_names_by_country[country]['F']

        last_name_list = self.last_names_by_country.get(country, [])
        if not last_name_list:
            last_name_list = ["Smith"]  # fallback

        first = random.choice(first_name_list)
        last = random.choice(last_name_list)
        return first, last, gender, country  # <-- include country

    def generate_csv(self, filename='random_names.csv', count=100):
        with open(filename, mode='w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['firstName', 'lastName', 'gender', 'country'])
            writer.writeheader()
            for _ in range(count):
                first, last, gender, country = self.generate_name()  # unpack country too
                writer.writerow({'firstName': first, 'lastName': last, 'gender': gender, 'country': country})
        print(f"Generated {count} names in {filename}")


if __name__ == "__main__":
    gen = NameGenerator()
    gen.generate_csv('random_names.csv', count=100)
