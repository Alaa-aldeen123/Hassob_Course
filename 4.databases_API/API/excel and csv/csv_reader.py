import csv

actors= [
    {'id':1,'first_name':'ahmed','last_name':'nader'},
    {'id':2,'first_name':'ahmed','last_name':'nader'},
    {'id':3,'first_name':'ahmed','last_name':'nader'},
]
with open('csv2.csv', 'w', newline='') as csvfile:
    fieldheaders = ['id','first_name','last_name']
    writer = csv.DictWriter(csvfile, fieldnames=fieldheaders)
    writer.writeheader()
    writer.writerow({'id':1,'first_name':'ahmed','last_name':'nader'})
    writer.writerows(actors)


with open('csv2.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)

    for row in reader:
        print(row)
