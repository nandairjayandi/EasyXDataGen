from names_dataset import NameDataset
import random
from unidecode import unidecode
import csv

ds = NameDataset(load_first_names=True, load_last_names=True)

def random_name(gender='F', country_alpha2='US'):
    top_names = ds.get_top_names(
        n=100,
        use_first_names=True,
        country_alpha2=country_alpha2,
        gender=gender
    )

    if country_alpha2 not in top_names or gender not in top_names[country_alpha2]:
        raise Exception(f"No top names for {gender} in {country_alpha2}")
    first_candidates = top_names[country_alpha2][gender]
    first_name = unidecode(random.choice(first_candidates)).strip()

    last_top = ds.get_top_names(n=100, use_first_names=False, country_alpha2=country_alpha2)
    if country_alpha2 not in last_top:
        raise Exception(f"No last names for {country_alpha2}")
    last_candidates = last_top[country_alpha2]
    last_name = unidecode(random.choice(last_candidates)).strip()

    return first_name, last_name, gender, country_alpha2

def random_age():
    return random.randint(18, 65)

def random_id(digit=6):
    return ''.join(str(random.randint(0, 9)) for _ in range(digit))

def generate_emp_csv(filename='employees.csv', rows=100):
    countries = ['US', 'SA', 'IN', 'FR', 'MX', 'CN']
    weights = [55, 10, 10, 5, 10, 10]

    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['First Name', 'Last Name', 'Gender', 'Country', 'Age', 'Employee ID'])

        for _ in range(rows):
            gender = random.choice(['M', 'F'])
            country = random.choices(countries, weights=weights, k=1)[0]
            first, last, gender, country = random_name(gender=gender, country_alpha2=country)
            age = random_age()
            empid = random_id()
            writer.writerow([first, last, gender, country, age, empid])

if __name__ == "__main__":
    generate_emp_csv(rows=100)
    print("CSV generated with random employees.")