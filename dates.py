# -*- coding: utf-8 -*-
from datetime import date, timedelta
import pandas as pd
import os, datetime, re

def getMRNs(dateRange):
    if len(dateRange) > 10:
        date1 = dateRange[:10]
        day1 = int(date1[-2:])
        month1 = int(date1[-5:-3])
        year1 = int(date1[:4])
        sdate = date(year1, month1, day1)
        
        date2 = dateRange[11:]
        day2 = int(date2[-2:])
        month2 = int(date2[-5:-3])
        year2 = int(date2[:4])
        edate = date(year2, month2, day2)
        folderList = []
        
        dateRange = pd.date_range(sdate,edate-timedelta(days=1),freq='d')
        for name in os.listdir('Q:\\IMRTQA'):
            fullName = os.path.join('Q:\\IMRTQA', name)
            if os.path.isdir(fullName):
                pathDate = str(datetime.datetime.fromtimestamp(os.path.getmtime(fullName)))
                for Date in dateRange:
                    if pathDate[:10] == str(Date)[:10]:
                        folderList.append(fullName)
        
        MRNlist = []
        for folder in folderList:
            numList = re.findall(r'\d+', folder)
            for num in numList:
                if len(str(num)) == 7:
                    MRNlist.append(str(num))
        
        return MRNlist
    else:
        day = int(dateRange[8:10])
        month = int(dateRange[5:7])
        year = int(dateRange[:4])
        editDate = str(date(year, month, day))
        
        folderList = []
        for name in os.listdir('Q:\\IMRTQA'):
            fullName = os.path.join('Q:\\IMRTQA', name)
            if os.path.isdir(fullName):
                pathDate = str(datetime.datetime.fromtimestamp(os.path.getmtime(fullName)))
                if pathDate[:10] == editDate:
                    folderList.append(fullName)
        
        MRNlist = []
        for folder in folderList:
            numList = re.findall(r'\d+', folder)
            for num in numList:
                if len(str(num)) == 7:
                    MRNlist.append(str(num))
        
        return MRNlist
        
            
if __name__ == '__main__':    
    dateRange = '2021/06/05-2021/06/10'
    Date = '2021/06/07'
    
    getMRNs(Date)
