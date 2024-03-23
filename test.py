import csv

column_index = 4

# Set to store unique terms
unique_terms = set()

with open("databases/dados_diaespecial.csv", "r") as file:
    csv_reader = csv.reader(file)

    # Skip the header row if it exists
    next(csv_reader)

    # Iterate through each row and add the term from the specified column to the set
    for row in csv_reader:
        row = row[0].split(";")
        unique_terms.add(row[column_index])

for term in unique_terms:
    print(term)
