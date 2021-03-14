import csv
import psycopg2
import time

conn = psycopg2.connect(database='group_16', user='', password='', host='web0.eecs.uottawa.ca', port= '15432')

daysofweek = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']

weeknumber = 36
wkctr = 1

did = 1
l = []

i = 1
#day:sept
while i < 31:
    if i < 22:
        l.append([i, 'September', daysofweek[wkctr], weeknumber, False, False, 'Summer', did, 9])
        i += 1
        did += 1
        wkctr += 1
        if wkctr == 7:
            weeknumber += 1
            wkctr = 0
    else:
        l.append([i, 'September', daysofweek[wkctr], weeknumber, False, False, 'Fall', did, 9])
        i += 1
        did += 1
        wkctr += 1
        if wkctr == 7:
            weeknumber += 1
            wkctr = 0

    
#day:oct
q = 1
while q < 32:
    l.append([q, 'October', daysofweek[wkctr], weeknumber, False, False, 'Fall', did, 10])
    q += 1
    did += 1
    wkctr += 1
    if wkctr == 7:
        weeknumber += 1
        wkctr = 0

#day:nov
w = 1
while w < 31:
    l.append([w, 'November', daysofweek[wkctr], weeknumber, False, False, 'Fall', did, 11])
    w += 1
    did += 1
    wkctr += 1
    if wkctr == 7:
        weeknumber += 1
        wkctr = 0

#day:dec
e = 1
while e < 32:
    if e < 21:
        l.append([e, 'December', daysofweek[wkctr], weeknumber, False, False, 'Fall', did, 12])
        e += 1
        did += 1
        wkctr += 1
        if wkctr == 7:
           weeknumber += 1
           wkctr = 0
    else:
        l.append([e, 'December', daysofweek[wkctr], weeknumber, False, False, 'Winter', did, 12])
        e += 1
        did += 1
        wkctr += 1
        if wkctr == 7:
            weeknumber += 1
            wkctr = 0

#setting weekends
#sept
l[4][4] = True
l[5][4] = True

l[11][4] = True
l[12][4] = True

l[18][4] = True
l[19][4] = True

l[25][4] = True
l[26][4] = True

#oct
l[32][4] = True
l[33][4] = True

l[39][4] = True
l[40][4] = True

l[46][4] = True
l[47][4] = True

l[53][4] = True
l[54][4] = True

#nov
l[67][4] = True
l[68][4] = True

l[74][4] = True
l[75][4] = True

l[81][4] = True
l[82][4] = True

l[88][4] = True
l[89][4] = True

#dec
l[95][4] = True
l[96][4] = True

l[102][4] = True
l[103][4] = True

l[109][4] = True
l[110][4] = True

l[116][4] = True
l[117][4] = True

#setting holidays
#labour day
l[6][5] = True

#thanksgiving
l[41][5] = True

#halloween
l[60][5] = True

#rememberance day
l[71][5] = True

#christmas eve
l[114][5] = True

#christmas day
l[115][5] = True

#boxing day
l[116][5] = True

#new years eve
l[121][5] = True


cur = conn.cursor()

for item in l:
    cur.execute("INSERT INTO data_mart.test_date_dimension (test_date_key, month, day_of_week, week_in_year, weekend, holiday, season, day, number_of_month) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)", (item[7], item[1], item[2], item[3], item[4], item[5], item[6], item[0], item[8]))

conn.commit()
cur.close()
conn.close()






