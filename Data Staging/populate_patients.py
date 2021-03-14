import csv
import psycopg2

conn = psycopg2.connect(database='group_16', user='yourUsername', password='yourPassword', host='web0.eecs.uottawa.ca', port= '15432')

l = []
patient_id = 1

with open('conposcovidloc.csv', newline = '') as csvfile:
    sr = csv.reader(csvfile, delimiter = ',', quotechar = '"')
    for row in sr:
        if row[9] == '':
            row[9] = 'n'
        else:
            row[9] = 'y'
    
        if ((row[3].startswith('2020-09') or row[3].startswith('2020-10') or row[3].startswith('2020-11') or row[3].startswith('2020-12')) and ((row[13].startswith('Ottawa') or row[13].startswith('Toronto') or row[13].startswith('Mississauga') or row[13].startswith('Newmarket')))):
            l.append([patient_id, row[6], row[5], row[7], row[9], row[8], row[11], row[13], row[1], row[2], row[3], row[4]])
            patient_id += 1

fields = ['patient_key', 'gender', 'age_group', 'acquisition_group', 'outbreak_related', 'outcome', 'reporting_phu', 'reporting_phu_city', 'onset_date', 'reported_date', 'test_date', 'specimen_date']
with open('patients.csv', 'w') as f:
    write = csv.writer(f)
    write.writerow(fields)
    write.writerows(l)

cur = conn.cursor()

for item in l:
    cur.execute("INSERT INTO data_mart.patient_dimension (patient_key, gender, age_group, acquisition_group, outbreak_related, outcome, reporting_phu, reporting_phu_city, onset_date, reported_date, test_date, specimen_date) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                (item[0], item[1], item[2], item[3], item[4], item[5], item[6], item[7], item[8], item[9], item[10], item[11]))

conn.commit()
cur.close()
conn.close()

