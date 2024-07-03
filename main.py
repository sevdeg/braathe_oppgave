from tabulate import tabulate
import redis
import json

#Legger til data
my_data = [
    [1, 'Ella Pia', 1996],
    [2, 'Petter Havn', 2000],
    [3, 'Sevde oguz', 2000]
]

#Legger til overskrift på tabellen
headers = ['ID', 'Navn Etternavn', 'År']

#Kobler til Redis serveren
r = redis.Redis(host='localhost', port=6379)

# Sletter tidligere data i redis
r.delete('employees')

#Lagrer dataene i en Redis Liste med en for løkke som JSON strings
for employee in my_data:
    r.rpush('employees', json.dumps(employee))

#Henter ut dataene fra Redis listen
r_data = r.lrange('employees', 0, -1)
data_redis = [json.loads(data) for data in r_data]

#Skriver ut data fra redis
print("Data fra Redis liste:")
for idx, employee in enumerate(data_redis):
    print(f"employee {idx+1}: {employee}")

#Printer ut tabellen
print("\nTabell med tabulate:")
print(tabulate(my_data, headers=headers, tablefmt="pretty"))
