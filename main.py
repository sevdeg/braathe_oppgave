from tabulate import tabulate
import redis
import json
from algoliasearch.search_client import SearchClient

#Legger til data
my_data = [
    {"ID": 1, "Navn Etternavn": 'Ella Pia',"År": 1996},
    {"ID": 2, "Navn Etternavn": 'Petter Havn',"År": 2000},
    {"ID":3,"Navn Etternavn": 'Sevde Oguz',"År": 2000}
]

#Konverterer til en liste av lister
list = [[employee["ID"], employee["Navn Etternavn"], employee["År"]] for employee in my_data]

#Legger til overskrifter på tabellen
headers = ['ID', 'Navn Etternavn', 'År']

#Printer ut tabellen
print("\nTabell med tabulate:")
print(tabulate(list, headers=headers, tablefmt="pretty"))

#Kobler til Redis serveren
r = redis.Redis(host='localhost', port=6379)

# Sletter tidligere data i redis
r.delete('employees')

#Lagrer dataene i en Redis Liste med en for løkke som JSON strings
for employee in my_data:
    r.rpush('employees', json.dumps(employee))

#Skriver ut data fra redis
print("\nData fra Redis liste:")
for index, data in enumerate(r.lrange('employees',0,-1)):
    employee_dict = json.loads(data)
    print(f"employee {index+1}: {employee_dict}")

#Algolia tilkobling
client = SearchClient.create('RRKOZQ1G6S', '1e8d734876b3e43dac50c6e2bf47e1bf')
index = client.init_index('employees')
obj_id = [{"objectID": str(index+1), **employee} for index, employee in enumerate(my_data)]
index.save_objects(obj_id)

#Søk år
search_year = 1996
results = index.search('', {
    'filters': f'År = {search_year}'
})

#Skrive ut søke med tabulate
search = results['hits']
res_table = [[employee['ID'], employee['Navn Etternavn'], employee['År']] for employee in search]

print(f"\nResultat av søking ved år {search_year}: ")
print(tabulate(res_table, headers=headers, tablefmt="pretty"))