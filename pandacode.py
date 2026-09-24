import pandas  as pd 
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

data = {
    'Visitor_ID': [f'V{1000 + i}' for i in range(20)],
    'Name': ['ABHISHEK SANDEEP      ZADE     ', 'ARNAV AJAY DESHPANDE.. ', '.. .. ASHWINI LALCHAND MUNDAWARE/ ', 'GAYATRI SURESH GAIKWAD', 'HARSHADA GANESH CHAUDHARI',
             'VA%$#@IBHAVI HARISHWAR PATIL', np.nan, 'VISHAKHA PUNDLIK JADHAV', 'YASH BHARAT SOLUNKE/', 'VIVEK SANTOSH KHANDWE',
             'VISHAKHA PUNDLIK JADHAV', 'Tanushree chhanwal', 'Shruti jaiswal', 'Shriyash Sulakhe', 'YASH BHARAT SOLUNKE',
             np.nan, 'ARNAV AJAY DESHPANDE', 'RUTUJA SANTOSH THOTE', 'ROHIT DILIP BILWAL', 'RITESH SHIVAJI BAIRAGI'],
    'Age': [25, 23, 22, np.nan, 21, 25, 24, 24, 28, np.nan,
            22, 23, 25, 27, 25, 30, 31, 26, 19, 19],
    'Ticket_Price': [500, 750, 500, 1000, np.nan, 500, 700, 650, 750, 1000,
                      500, 800, np.nan, 750, 500, 700, 900, 850, 750, np.nan],
    'Check_In_Time': ['10:00 AM', '10:30 AM', '11:00 AM', '11:30 AM', np.nan,
                       '10:00 AM', '12:00 PM', '12:30 PM', '01:00 PM', '01:30 PM',
                       '11:00 AM', '02:00 PM', np.nan, '02:30 PM', '10:00 AM',
                       '12:00 PM', '03:00 PM', '03:30 PM', '04:00 PM', np.nan],
    'City':['Delhi','Aurangabad', 'Mumbai','Bombay','New Delhi','NDL','Chennai','Chenai','Chennaai','Bangalore',
            'Delhi','Pune', 'New Delhi','Bombay','New Delhi','NDL','Indore','Bangalore','Ujjain','Bangalore'],
    'State': ['Delhi','Maharastra', 'Maharastra','Maharastra','Delhi','Delhi','Tamilnadu','Tamilnadu','Tamilnadu','Karnataka',
            'Delhi','Maharastra', 'Delhi','Maharastra','Delhi','Delhi','Madhya Pradesh','Karnataka','Madhya Pradesh','Karnataka']
}

df=pd.DataFrame(data)
# print(df)

# df.to_csv('visitor_data.csv', index=False)
print(df.Age.count())

df['Name']= df['Name'].str.replace(r'[^a-zA-Z\s]', '', regex=True)

print(df.head(15))