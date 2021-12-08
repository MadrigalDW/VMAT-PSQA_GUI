"""
Created on Tue Jun  1 22:10:06 2021
@author: weersim
"""
import pdfplumber, os.path, time

def mostRecentPDFs(pdfList, fieldIndexes, inputDate=''):
    # makes list of only ArcCheck, Delta4, & IQM pdfs
    pdfList2 = []
    for pathName in pdfList:
        if pathName not in pdfList2:
            pdfList2.append(pathName)
    
    ACpdfList = []
    strList = []
    for pathName in pdfList2: 
        with pdfplumber.open(pathName) as pdf: 
            firstPage = pdf.pages[0]
            fullStr = firstPage.extract_text()
        i = 0
        if 'ArcCHECK' in fullStr:
            ACpdfList.append(pathName)
            strList.append(fullStr)
        elif 'IQM Report Summary:' in fullStr:
            ACpdfList.append(pathName)
            strList.append(fullStr)
        else:
            for item in fieldIndexes:
                if item in fullStr:
                    ACpdfList.append(pathName)
                    strList.append(fullStr)
                    i = 1
                    print('Delta4 Added!')
                    break
            if i == 0:
                print(pathName, '\tNot added')
    
    mostRecentDate = '0000-00-00'
    secondMostRecentDate = '0000-00-00'
    
    # creates list of dates each ArcCheck pdf is created
    date_dict = {'Jan':'01', 'Feb':'02', 'Mar':'03', 'Apr':'04', 'May':'05', 'Jun': '06', 'Jul': '07', 'Aug':'08', 'Sep':'09', 'Oct':'10', 'Nov':'11', 'Dec':'12'}
    pdfDict = {}
    
    for pdf in ACpdfList:
        tempDate = time.ctime(os.path.getctime(pdf))
        tempList = tempDate.split(' ')
        if len(tempList[3]) == 1:
            day = '0' + tempList[3]
            year = tempList[5]
        else:
            day = tempList[2]
            year = tempList[4]

        date = year + '-' + date_dict[tempList[1]] + '-' + day
        pdfDict[pdf] = date
        
        if inputDate == '':
            if int(date[0:4]) > int(mostRecentDate[0:4]):
                mostRecentDate = date
            elif int(date[0:4]) == int(mostRecentDate[0:4]):
                if int(date[5:7]) > int(mostRecentDate[5:7]):
                    mostRecentDate = date
                elif int(date[5:7]) == int(mostRecentDate[5:7]):
                    if int(date[8:]) > int(mostRecentDate[8:]):
                        secondMostRecentDate = mostRecentDate
                        mostRecentDate = date
                    elif secondMostRecentDate == '0000-00-00':
                        secondMostRecentDate = date
        else:
            pass
        
    i = 0            
    for pdf in pdfDict:
        if pdfDict[pdf] != mostRecentDate:
            ACpdfList.remove(pdf) 
            temp = strList[i]
            strList.remove(temp)
        else:
            i = i + 1
    
    for fullStr in strList:
        if 'ArcCHECK' not in fullStr:
            for pdf in pdfDict:
                if pdfDict[pdf] == secondMostRecentDate:
                    ACpdfList.append(pdf)
    
    return ACpdfList

def mostRecentQueries(QAfields, inputDate=''):
    mostRecentDate = '0000-00-00'  
    if inputDate == '':
        for QAfield in QAfields:
            date = QAfield['treatmentTime'][0:10]
            if int(date[0:4]) > int(mostRecentDate[0:4]):
                mostRecentDate = date
            elif int(date[0:4]) == int(mostRecentDate[0:4]):
                if int(date[5:7]) > int(mostRecentDate[5:7]):
                    mostRecentDate = date
                elif int(date[5:7]) == int(mostRecentDate[5:7]):
                    if int(date[8:]) > int(mostRecentDate[8:]):
                        mostRecentDate = date
    else:
        for QAfield in QAfields:
            date = QAfield['treatmentTime'][0:10]
            
            if int(date[0:4]) > int(mostRecentDate[0:4]) and int(date[0:4]) <= int(inputDate[0:4]):
                if int(date[0:4]) < int(inputDate[0:4]):
                    mostRecentDate = date
                else:
                    if int(date[5:7]) < int(inputDate[5:7]):
                        mostRecentDate = date
                    elif int(date[5:7]) == int(inputDate[5:7]) and int(date[8:]) <= int(inputDate[8:]):
                        mostRecentDate = date
            elif int(date[0:4]) == int(mostRecentDate[0:4]) and int(date[0:4]) <= int(inputDate[0:4]):
                if int(date[5:7]) > int(mostRecentDate[5:7]):
                    if int(date[0:4]) < int(inputDate[0:4]):
                        mostRecentDate = date
                    else:
                        if int(date[5:7]) < int(inputDate[5:7]): 
                            mostRecentDate = date
                        elif int(date[5:7]) == int(inputDate[5:7]):
                            if int(date[8:]) <= int(inputDate[8:]):
                                mostRecentDate = date
                elif int(date[5:7]) == int(mostRecentDate[5:7]) and int(date[5:7]) <= int(inputDate[5:7]):
                    if int(date[8:]) > int(mostRecentDate[8:]) and int(date[8:]) <= int(inputDate[8:]):
                            mostRecentDate = date
            
    print(mostRecentDate)            
    # selects only QA fields from the most recent date               
    QAfieldsSelected = []
    labelList = []
    removeList = []
    for QAfield in QAfields:
        date = QAfield['treatmentTime'][0:10]
        if date == mostRecentDate:
            QAfieldsSelected.append(QAfield)
            
    for QAfield in QAfieldsSelected:
        if QAfield['fieldLabel'] in labelList:
            removeList.append(QAfield)
        else:
            labelList.append(QAfield['fieldLabel']) 
    
    for QAfield in removeList:
        QAfieldsSelected.remove(QAfield)
    
    return QAfieldsSelected