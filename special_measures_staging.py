import pandas as pd
import numpy as np

from datetime import datetime, timedelta

#Switch function
def switch(x):
    return {
        'Control': 'Stringent measures: Broader-scale actions and restrictions across multiple sectors to control the spread. Restrictions are the most severe available before widescale business or organizational closings.',
        'Prevent': 'Standard measures: Capacity limits in various public settings where people gather. Highest-risk settings stay closed.',
        'Protect': 'Strengthened measures: Stronger targeted enforcement, fines and more education to limit the spread. Public health measures for high-risk settings.',
        'Restrict': 'Intermediate measures: Stronger actions, restrictions and enforcement while avoiding closures.',
        'Lockdown': 'Maximum measures: Widescale actions and restrictions, including closures, to stop or slow the spread.?We will consider declaring a state of emergency.',
        'Stay-at-home': 'Until your region returns to the colour-coded framework, the shutdown and stay-at-home orders still apply in your area.'
    }.get(x, 'No description available')



ontario_measures = pd.read_csv("response_framework_raw.csv", sep=',')

ontario_measures.head()


special_measures_dimension = pd.DataFrame(columns=['speacial_measures_surrogate_key','status','region', 'description','isFederal', 'start_date','end_date'])



start_date = datetime(2020, 9, 1).date()
end_date = datetime(2020, 12, 31).date()
isFederal = False

for skey, row in ontario_measures.iterrows():
    curr_date =pd.to_datetime(row['start_date']).date() 

    phu = row['Reporting_PHU']
    matches = ["durham", "halton", "peel", "york", "toronto", "ottawa"]#list of regions

    #if(any(x in phu.lower() for x in matches) ):
    for x in matches:
        if(x in phu.lower()):

            if(curr_date >= start_date and curr_date <= end_date):

                description = switch(row['Status_PHU'])#find the description for the current status
    
                ontario_measures_row = [skey + 100]#surrogate key
                ontario_measures_row.append(row['Status_PHU'])#title
                ontario_measures_row.append(x)#put only the region
                ontario_measures_row.append(description)
                ontario_measures_row.append(isFederal) 
                ontario_measures_row.append(curr_date)
                ontario_measures_row.append(pd.to_datetime(row['end_date']).date() )
                special_measures_dimension.loc[len(special_measures_dimension)] = ontario_measures_row


special_measures_dimension.head()

#federal_measures = pd.read_csv("response_framework.csv", sep=';')
#federal_measures.head()


# for idx, row in federal_measures.iterrows():
#     curr_date = row['start_date']
#     curr_date = datetime.strptime(curr_date,'%Y-%m-%d')

#     phu = row['title']
#     matches = ["durham", "halton", "peel", "york", "toronto", "ottawa"]

#     if(any(x in phu.lower() for x in matches) ):
#         if(curr_date >= start_date and curr_date <= end_date):

            
#             federal_measures_row = [idx + 100]#surrogate key
#             federal_measures_row.append(row['title'])
#             federal_measures_row.append(row['status'])
#             federal_measures_row.append(row['description'])
#             federal_measures_row.append(row['isFederal']) 
#             federal_measures_row.append(curr_date)
#             federal_measures_row.append(row['end_date'])
#             special_measures_dimension.loc[len(special_measures_dimension)] = federal_measures_row



special_measures_dimension.fillna(0, inplace = True)

special_measures_dimension.to_csv("special_measures_dimension.csv",index=False)