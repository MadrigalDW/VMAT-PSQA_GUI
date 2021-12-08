# -*- coding: utf-8 -*-
# PLEASE NOTE: this code looks absolutely disgusting, but it gets the job done. The formatting of these pdfs was horrible to work with, which is part of the reason for the disgustingness
import pdfplumber, glob, re
import pandas as pd
    
def getValues(folder, year):
    MRNlist = []
    noData = []
    removeList = []

    pdfList = glob.glob('Q:\\Brachy Patients GYN\\' + folder + '\\' + year + '\\**\\*.pdf', recursive = True)
    
    # checks that there are pdfs in the target file, exits if not
    try:
        pdfList[0]
    except IndexError:
        print('There are no files in the folder you searched for.')
        return None
    
    print('pdfList length:', len(pdfList))
    
    for pathName in pdfList:
        tempList = re.findall(r'\d+', pathName)
        for num in tempList:
            if len(num) == 7:
                if num not in noData:
                    noData.append(num)
                    
    # creates removeList of pdfs without target string in the pdf and removes them from noData
    for pathName in pdfList:
        string = ''
        with pdfplumber.open(pathName) as pdf: # uses pdfplumber to extract text from the pdf
            page = pdf.pages[0]
            string = page.extract_text()

        if string:
            if 'PHYSICAL - BIOLOGICAL DOCUMENTATION OF GYNAECOLOGICAL HDR BT' in string:
                tempList = re.findall(r'\d+', pathName)
                for num in tempList:
                    if num in noData:
                        noData.remove(num)
                    if len(num) == 7:
                        if num not in MRNlist:
                            MRNlist.append(num)
            else:
                removeList.append(pathName)
        else:
            removeList.append(pathName)
    
    # removes removeList pdfs from main list       
    for pathName in removeList:
        pdfList.remove(pathName)
    
    newPDFlist = []
    for MRN in MRNlist:
        #select only final fraction
        tempList = []
        elseList = []
        isFour = False
        for pdf in pdfList:
            if MRN in pdf:
                tempList.append(pdf)
        for pathName in tempList:
            if 'fx4' in pathName or 'Fx4' in pathName or 'FX4' in pathName or 'fX4' in pathName:
                newPDFlist.append(pathName)
                isFour = True
            else:
                elseList.append(pathName)
        if not isFour:
            for pathName in elseList:
                if 'fx3' in pathName or 'Fx3' in pathName or 'FX3' in pathName or 'fX3' in pathName:
                    newPDFlist.append(pathName)
    
    noData.insert(0, 'No Brachy Data')
    print('pdfList length:', len(newPDFlist))
    print('noData:', noData)
    
    outList = [['MRN', 'Patient Name', '# of Fx','Fx 1 Date', 'Fx 2 Date', 'Fx 3 Date', 'Fx 4 Date', 'Total Dose', 'Applicator Type 1', 'Applicator Type 2', 'Applicator Type 3', 'Applicator Type 4', 'Applicator Dimension 1', 'Applicator Dimension 2', 'Applicator Dimension 3', 'Applicator Dimension 4', 'TRAK 1','TRAK 2','TRAK 3','TRAK 4', 'GTV_T_res [cm3] 1', 'GTV_T_res [cm3] 2', 'GTV_T_res [cm3] 3', 'GTV_T_res [cm3] 4', 'GTV_T_res [cm3] mean', 'GTV_T_res [cm3] stddev', 'GTV_T_res D100 iso 1', 'GTV_T_res D100 iso 2', 'GTV_T_res D100 iso 3', 'GTV_T_res D100 iso 4', 'GTV_T_res D100 iso BT', 'GTV_T_res D100 iso BT+EBT', 'GTV_T_res D90 iso 1', 'GTV_T_res D90 iso 2', 'GTV_T_res D90 iso 3', 'GTV_T_res D90 iso 4', 'GTV_T_res D90 iso BT', 'GTV_T_res D90 iso BT+EBT', 'GTV_T_res D98 iso 1', 'GTV_T_res D98 iso 2', 'GTV_T_res D98 iso 3', 'GTV_T_res D98 iso 4', 'GTV_T_res D98 iso BT', 'GTV_T_res D98 iso BT+EBT', 'GTV_T_res V100 iso 1', 'GTV_T_res V100 iso 2', 'GTV_T_res V100 iso 3', 'GTV_T_res V100 iso 4', 'GTV_T_res V100 iso BT', 'GTV_T_res V100 iso BT+EBT', 'CTV_T_HR [cm3] 1', 'CTV_T_HR [cm3] 2', 'CTV_T_HR [cm3] 3', 'CTV_T_HR [cm3] 4', 'CTV_T_HR [cm3] mean', 'CTV_T_HR [cm3] stddev', 'CTV_T_HR D100 iso 1', 'CTV_T_HR D100 iso 2', 'CTV_T_HR D100 iso 3', 'CTV_T_HR D100 iso 4', 'CTV_T_HR D100 iso BT', 'CTV_T_HR D100 iso BT+EBT', 'CTV_T_HR D90 iso 1', 'CTV_T_HR D90 iso 2', 'CTV_T_HR D90 iso 3', 'CTV_T_HR D90 iso 4', 'CTV_T_HR D90 iso BT', 'CTV_T_HR D90 iso BT+EBT', 'CTV_T_HR D98 iso 1', 'CTV_T_HR D98 iso 2', 'CTV_T_HR D98 iso 3', 'CTV_T_HR D98 iso 4', 'CTV_T_HR D98 iso BT', 'CTV_T_HR D98 iso BT+EBT', 'CTV_T_HR V100 iso 1', 'CTV_T_HR V100 iso 2', 'CTV_T_HR V100 iso 3', 'CTV_T_HR V100 iso 4', 'CTV_T_HR V100 iso BT', 'CTV_T_HR V100 iso BT+EBT', 'CTV_T_IR [cm3] 1', 'CTV_T_IR [cm3] 2', 'CTV_T_IR [cm3] 3', 'CTV_T_IR [cm3] 4', 'CTV_T_IR [cm3] mean', 'CTV_T_IR [cm3] stddev', 'CTV_T_IR D100 iso 1', 'CTV_T_IR D100 iso 2', 'CTV_T_IR D100 iso 3', 'CTV_T_IR D100 iso 4', 'CTV_T_IR D100 iso BT', 'CTV_T_IR D100 iso BT+EBT', 'CTV_T_IR D90 iso 1', 'CTV_T_IR D90 iso 2', 'CTV_T_IR D90 iso 3', 'CTV_T_IR D90 iso 4', 'CTV_T_IR D90 iso BT', 'CTV_T_IR D90 iso BT+EBT', 'CTV_T_IR D98 iso 1', 'CTV_T_IR D98 iso 2', 'CTV_T_IR D98 iso 3', 'CTV_T_IR D98 iso 4', 'CTV_T_IR D98 iso BT', 'CTV_T_IR D98 iso BT+EBT', 'CTV_T_IR V50 iso 1', 'CTV_T_IR V50 iso 2', 'CTV_T_IR V50 iso 3', 'CTV_T_IR V50 iso 4', 'CTV_T_IR V50 iso BT', 'CTV_T_IR V50 iso BT+EBT', 'Sigmoid [cm3] 1', 'Sigmoid [cm3] 2', 'Sigmoid [cm3] 3', 'Sigmoid [cm3] 4', 'Sigmoid [cm3] mean', 'Sigmoid [cm3] stddev', 'Sigmoid 0,1cm3 1', 'Sigmoid 0,1cm3 2', 'Sigmoid 0,1cm3 3', 'Sigmoid 0,1cm3 4', 'Sigmoid 0,1cm3 BT', 'Sigmoid 0,1cm3 BT+EBT', 'Sigmoid 1cm3 1', 'Sigmoid 1cm3 2', 'Sigmoid 1cm3 3', 'Sigmoid 1cm3 4', 'Sigmoid 1cm3 BT', 'Sigmoid 1cm3 BT+EBT', 'Sigmoid 2cm3 1', 'Sigmoid 2cm3 2', 'Sigmoid 2cm3 3', 'Sigmoid 2cm3 4', 'Sigmoid 2cm3 BT', 'Sigmoid 2cm3 BT+EBT', 'Rectum [cm3] 1', 'Rectum [cm3] 2', 'Rectum [cm3] 3', 'Rectum [cm3] 4', 'Rectum [cm3] mean', 'Rectum [cm3] stddev', 'Rectum 0,1cm3 1', 'Rectum 0,1cm3 2', 'Rectum 0,1cm3 3', 'Rectum 0,1cm3 4', 'Rectum 0,1cm3 BT', 'Rectum 0,1cm3 BT+EBT', 'Rectum 1cm3 1', 'Rectum 1cm3 2', 'Rectum 1cm3 3', 'Rectum 1cm3 4', 'Rectum 1cm3 BT', 'Rectum 1cm3 BT+EBT', 'Rectum 2cm3 1', 'Rectum 2cm3 2', 'Rectum 2cm3 3', 'Rectum 2cm3 4', 'Rectum 2cm3 BT', 'Rectum 2cm3 BT+EBT', 'SmallBowel [cm3] 1', 'SmallBowel [cm3] 2', 'SmallBowel [cm3] 3', 'SmallBowel [cm3] 4', 'SmallBowel [cm3] mean', 'SmallBowel [cm3] stddev', 'SmallBowel 0,1cm3 1', 'SmallBowel 0,1cm3 2', 'SmallBowel 0,1cm3 3', 'SmallBowel 0,1cm3 4', 'SmallBowel 0,1cm3 BT', 'SmallBowel 0,1cm3 BT+EBT', 'SmallBowel 1cm3 1', 'SmallBowel 1cm3 2', 'SmallBowel 1cm3 3', 'SmallBowel 1cm3 4', 'SmallBowel 1cm3 BT', 'SmallBowel 1cm3 BT+EBT', 'SmallBowel 2cm3 1', 'SmallBowel 2cm3 2', 'SmallBowel 2cm3 3', 'SmallBowel 2cm3 4', 'SmallBowel 2cm3 BT', 'SmallBowel 2cm3 BT+EBT', 'Bladder [cm3] 1', 'Bladder [cm3] 2', 'Bladder [cm3] 3', 'Bladder [cm3] 4', 'Bladder [cm3] mean', 'Bladder [cm3] stddev', 'Bladder 0,1cm3 1', 'Bladder 0,1cm3 2', 'Bladder 0,1cm3 3', 'Bladder 0,1cm3 4', 'Bladder 0,1cm3 BT', 'Bladder 0,1cm3 BT+EBT', 'Bladder 1cm3 1', 'Bladder 1cm3 2', 'Bladder 1cm3 3', 'Bladder 1cm3 4', 'Bladder 1cm3 BT', 'Bladder 1cm3 BT+EBT', 'Bladder 2cm3 1', 'Bladder 2cm3 2', 'Bladder 2cm3 3', 'Bladder 2cm3 4', 'Bladder 2cm3 BT', 'Bladder 2cm3 BT+EBT', 'LT Ureter [cm3] 1', 'LT Ureter [cm3] 2', 'LT Ureter [cm3] 3', 'LT Ureter [cm3] 4', 'LT Ureter [cm3] mean', 'LT Ureter [cm3] stddev', 'LT Ureter 0,1cm3 1', 'LT Ureter 0,1cm3 2', 'LT Ureter 0,1cm3 3', 'LT Ureter 0,1cm3 4', 'LT Ureter 0,1cm3 BT', 'LT Ureter 0,1cm3 BT+EBT', 'LT Ureter 1cm3 1', 'LT Ureter 1cm3 2', 'LT Ureter 1cm3 3', 'LT Ureter 1cm3 4', 'LT Ureter 1cm3 BT', 'LT Ureter 1cm3 BT+EBT', 'LT Ureter 2cm3 1', 'LT Ureter 2cm3 2', 'LT Ureter 2cm3 3', 'LT Ureter 2cm3 4', 'LT Ureter 2cm3 BT', 'LT Ureter 2cm3 BT+EBT', 'RT Ureter [cm3] 1', 'RT Ureter [cm3] 2', 'RT Ureter [cm3] 3', 'RT Ureter [cm3] 4', 'RT Ureter [cm3] mean', 'RT Ureter [cm3] stddev', 'RT Ureter 0,1cm3 1', 'RT Ureter 0,1cm3 2', 'RT Ureter 0,1cm3 3', 'RT Ureter 0,1cm3 4', 'RT Ureter 0,1cm3 BT', 'RT Ureter 0,1cm3 BT+EBT', 'RT Ureter 1cm3 1', 'RT Ureter 1cm3 2', 'RT Ureter 1cm3 3', 'RT Ureter 1cm3 4', 'RT Ureter 1cm3 BT', 'RT Ureter 1cm3 BT+EBT', 'RT Ureter 2cm3 1', 'RT Ureter 2cm3 2', 'RT Ureter 2cm3 3', 'RT Ureter 2cm3 4', 'RT Ureter 2cm3 BT', 'RT Ureter 2cm3 BT+EBT', 'VaginalWall LATE [cm3] 1', 'VaginalWall LATE [cm3] 2', 'VaginalWall LATE [cm3] 3', 'VaginalWall LATE [cm3] 4', 'VaginalWall LATE [cm3] mean', 'VaginalWall LATE [cm3] stddev', 'VaginalWall LATE 0,1cm3 1', 'VaginalWall LATE 0,1cm3 2', 'VaginalWall LATE 0,1cm3 3', 'VaginalWall LATE 0,1cm3 4', 'VaginalWall LATE 0,1cm3 BT', 'VaginalWall LATE 0,1cm3 BT+EBT', 'VaginalWall LATE 1cm3 1', 'VaginalWall LATE 1cm3 2', 'VaginalWall LATE 1cm3 3', 'VaginalWall LATE 1cm3 4', 'VaginalWall LATE 1cm3 BT', 'VaginalWall LATE 1cm3 BT+EBT', 'VaginalWall LATE 2cm3 1', 'VaginalWall LATE 2cm3 2', 'VaginalWall LATE 2cm3 3', 'VaginalWall LATE 2cm3 4', 'VaginalWall LATE 2cm3 BT', 'VaginalWall LATE 2cm3 BT+EBT', 'VaginalWall EARLY [cm3] 1', 'VaginalWall EARLY [cm3] 2', 'VaginalWall EARLY [cm3] 3', 'VaginalWall EARLY [cm3] 4', 'VaginalWall EARLY [cm3] mean', 'VaginalWall EARLY [cm3] stddev', 'VaginalWall EARLY 0,1cm3 1', 'VaginalWall EARLY 0,1cm3 2', 'VaginalWall EARLY 0,1cm3 3', 'VaginalWall EARLY 0,1cm3 4', 'VaginalWall EARLY 0,1cm3 BT', 'VaginalWall EARLY 0,1cm3 BT+EBT', 'VaginalWall EARLY 1cm3 1', 'VaginalWall EARLY 1cm3 2', 'VaginalWall EARLY 1cm3 3', 'VaginalWall EARLY 1cm3 4', 'VaginalWall EARLY 1cm3 BT', 'VaginalWall EARLY 1cm3 BT+EBT', 'VaginalWall EARLY 2cm3 1', 'VaginalWall EARLY 2cm3 2', 'VaginalWall EARLY 2cm3 3', 'VaginalWall EARLY 2cm3 4', 'VaginalWall EARLY 2cm3 BT', 'VaginalWall EARLY 2cm3 BT+EBT', 'PT ICRURV Point 1', 'PT ICRURV Point 2', 'PT ICRURV Point 3', 'PT ICRURV Point 4', 'PT ICRURV Point BT', 'PT ICRURV Point BT + EBT', 'PT A Left 1', 'PT A Left 2', 'PT A Left 3', 'PT A Left 4', 'PT A Left BT', 'PT A Left BT + EBT', 'PT A Right 1', 'PT A Right 2', 'PT A Right 3', 'PT A Right 4', 'PT A Right BT', 'PT A Right BT + EBT']]
    for pathName in newPDFlist:
        string = ''
        dictionary = {}
        
        tempList = re.findall(r'\d+', pathName)
        for num in tempList:
            if len(num) == 7:
                dictionary['MRN'] = num
                print(num)
        
        with pdfplumber.open(pathName) as pdf: # uses pdfplumber to extract text from the pdf
            pages = pdf.pages[:]
            for page in pages:
                string = string + '\n' + page.extract_text()
        
        if 'MRN' not in dictionary:
            strList = string.split('PATIENT ,  ID-number ')
            if len(strList) == 1:
                strList = string.split('PATIENT ,  ID-number')
            strList2 = strList[1].split('\n')
            strList3 = strList2[0].split(' ')
            for item in strList3:
                try:
                    dictionary['MRN'] = int(item)
                except:
                    pass
        if 'MRN' not in dictionary:
            print('pathName not in:\t', pathName)
            dictionary['MRN'] = ''
            
        strList = string.split('PATIENT ,  ID-number ')
        try:
            strList2 = strList[1].split('\n')
            strList3 = strList2[0].split(' ')
            isInt = False
            for m, item in enumerate(strList3):
                try:
                    f = int(item)
                    s = ' '
                    tempString1 = s.join(strList3[0:m])
                    isInt = True
                except:
                    pass
            
            if not isInt:
                dictionary['patientName'] = strList2[0]
            else:
                dictionary['patientName'] = tempString1
        except:
            dictionary['patientName'] = ''
        
        strList = string.split('date ')
        if len(strList) > 1:
            if 'dose values in Gy' in strList[1]:
                strList2 = strList[1].split(' dose values in Gy')
            else:
                strList2 = strList[1].split('\n')
            strList3 = strList2[0].split(' ')
            while len(strList3) < 4:
                strList3.append('')
            if len(strList3) > 4:
                strList3 = strList3[:4]
            dictionary['dates'] = strList3
        else:
            dictionary['dates'] = ['', '', '', '']
        
        strList = string.split('total dose ')
        strList2 = strList[1].split(' ')
        dictionary['totalDose'] = strList2[0]
        
        strList = string.split('applicator(s): type ')
        strList2 = strList[1].split('\n')
        appType1 = strList2[0].split(' ')
        appType = []
        for type1 in appType1:
            if type1 != 'BT' and type1 != 'EBT' and type1 != '+':
                appType.append(type1)
        dictionary['appType'] = appType
        
        strList = string.split('applicator(s): dimensions')
        strList2 = strList[1].split('\n')
        dictionary['appDim'] = strList2[0].split(' ')
        
        if 'TRAK' in string:
            strList = string.split('TRAK ')
            strList2 = strList[1].split('\n')
            dictionary['TRAK'] = strList2[0].split(' ')
        else:
            dictionary['TRAK'] = ['', '', '', '']
        
        strList = string.split('\n') 
        strList = strList[17:]
        listList = []
        tempList = []
        first = True
        for i, x in enumerate(strList):
            y = x.split(' ')
            if (len(y) < 3 and 'iso' not in y) or (len(y[0]) != 1 and 'cm3' not in y[0] and 'iso' not in y):
                if not first:
                    listList.append(tempList)
                    tempList = [x]
                else:
                    tempList = [x]
                    first = False
            else:
                tempList.append(x)
        listList.append(tempList)
        
        for lst in listList:
            #create sub dictionary for each mini table to add with table header as key
            subDictionary = {}
            for element in lst:
                if '[cm3]' in element or 'iso' in element or 'volume' in element or '[a/b=' in element or 'ï›ï¡ï€¯ï¢ï€½ï€±' in element or '\uf05b\uf061' in element or '[Î±/Î²=' in element:
                    subList = element.split(' ')
                    
                    if 'iso' in element:
                        if element == 'iso':
                            continue
                        s = ' '
                        tempString = s.join(subList[0:3])
                    elif lst[0] == 'PT A':
                        if 'left' not in subDictionary:
                            tempString = 'left'
                        else:
                            tempString = 'right'
                    else:
                        if element == '[cm3]':
                            continue
                        tempString = element[:5]
                    
                    try:
                        q = float(subList[-7])
                        lineList = subList[-7:-3]
                        lineList.extend(subList[-2:])
                        
                        if str(lineList[3]) == '0.0' or str(lineList[3]) == '0.00':
                            lineList[3] = ''
                        subDictionary[tempString] = lineList
                    except:
                        try:
                            q = float(subList[-6])
                            if str(subList[-3]) == '0.0' or str(subList[-3]) == '0.00':
                                subList[-3] = ''
                            
                            subDictionary[tempString] = subList[-6:]
                        except:
                            lineList = subList[-5:-2]
                            lineList.append('')
                            lineList.extend(subList[-2:])
                            
                            try:
                                if str(lineList[3]) == '0.0' or str(lineList[3]) == '0.00':
                                    lineList[3] = ''
                            except:
                                print('Line list: ', lineList)
                                print('Element: ', element)
                                print('lst[0]: ', lst[0])
                                return None
                            
                            subDictionary[tempString] = lineList
                    
                    if '[cm3]' in element:
                        if 'Vagina' in lst[0]:
                            subDictionary['LE'] = subList[1]  
            dictionary[lst[0]] = subDictionary 
        
        outputList = dictionaryToOutputList(dictionary)
        outList.append(outputList)
    for item in noData:
        try:
            outList.append([float(item)])
        except:
            outList.append([item])
    
    fileName = 'N:\\Weersink\\Brachy_HDR\\ForMadrigal\\Extraction Results\\Dose Extraction ' + folder + '-' + year + '.xlsx'
    
    df = pd.DataFrame(outList)
    new_header = df.iloc[0]     # grab the first row for the header
    df = df[1:]                 # take the data less the header row
    df.columns = new_header     # set the header row as the df header
    df.to_excel(fileName, sheet_name=(folder[:24]))




def getCompiledValues(folder):
    pdfList = glob.glob('N:\\Weersink\\Brachy_HDR\\ForMadrigal\\GYNE_PDFs\\' + folder + '\\**\\*.pdf', recursive = True)
    
    # checks that there are pdfs in the target file, exits if not
    try:
        pdfList[0]
    except IndexError:
        print('There are no files in the folder you searched for.')
        return None
    
    print('pdfList length:', len(pdfList))
    removeList = []
    for pathName in pdfList:
        string = ''
        with pdfplumber.open(pathName) as pdf: # uses pdfplumber to extract text from the pdf
            pages = pdf.pages[:]
            page = pages[0]
            if page.extract_text():
                string = string + '\n' + page.extract_text()
        
        if 'PHYSICAL - BIOLOGICAL DOCUMENTATION OF GYNAECOLOGICAL HDR BT' not in string:
            removeList.append(pathName)
    
    for pathName in removeList:
        pdfList.remove(pathName)
    
    outList = [['MRN', 'Patient Name', '# of Fx','Fx 1 Date', 'Fx 2 Date', 'Fx 3 Date', 'Fx 4 Date', 'Total Dose', 'Applicator Type 1', 'Applicator Type 2', 'Applicator Type 3', 'Applicator Type 4', 'Applicator Dimension 1', 'Applicator Dimension 2', 'Applicator Dimension 3', 'Applicator Dimension 4', 'TRAK 1','TRAK 2','TRAK 3','TRAK 4', 'GTV_T_res [cm3] 1', 'GTV_T_res [cm3] 2', 'GTV_T_res [cm3] 3', 'GTV_T_res [cm3] 4', 'GTV_T_res [cm3] mean', 'GTV_T_res [cm3] stddev', 'GTV_T_res D100 iso 1', 'GTV_T_res D100 iso 2', 'GTV_T_res D100 iso 3', 'GTV_T_res D100 iso 4', 'GTV_T_res D100 iso BT', 'GTV_T_res D100 iso BT+EBT', 'GTV_T_res D90 iso 1', 'GTV_T_res D90 iso 2', 'GTV_T_res D90 iso 3', 'GTV_T_res D90 iso 4', 'GTV_T_res D90 iso BT', 'GTV_T_res D90 iso BT+EBT', 'GTV_T_res D98 iso 1', 'GTV_T_res D98 iso 2', 'GTV_T_res D98 iso 3', 'GTV_T_res D98 iso 4', 'GTV_T_res D98 iso BT', 'GTV_T_res D98 iso BT+EBT', 'GTV_T_res V100 iso 1', 'GTV_T_res V100 iso 2', 'GTV_T_res V100 iso 3', 'GTV_T_res V100 iso 4', 'GTV_T_res V100 iso BT', 'GTV_T_res V100 iso BT+EBT', 'CTV_T_HR [cm3] 1', 'CTV_T_HR [cm3] 2', 'CTV_T_HR [cm3] 3', 'CTV_T_HR [cm3] 4', 'CTV_T_HR [cm3] mean', 'CTV_T_HR [cm3] stddev', 'CTV_T_HR D100 iso 1', 'CTV_T_HR D100 iso 2', 'CTV_T_HR D100 iso 3', 'CTV_T_HR D100 iso 4', 'CTV_T_HR D100 iso BT', 'CTV_T_HR D100 iso BT+EBT', 'CTV_T_HR D90 iso 1', 'CTV_T_HR D90 iso 2', 'CTV_T_HR D90 iso 3', 'CTV_T_HR D90 iso 4', 'CTV_T_HR D90 iso BT', 'CTV_T_HR D90 iso BT+EBT', 'CTV_T_HR D98 iso 1', 'CTV_T_HR D98 iso 2', 'CTV_T_HR D98 iso 3', 'CTV_T_HR D98 iso 4', 'CTV_T_HR D98 iso BT', 'CTV_T_HR D98 iso BT+EBT', 'CTV_T_HR V100 iso 1', 'CTV_T_HR V100 iso 2', 'CTV_T_HR V100 iso 3', 'CTV_T_HR V100 iso 4', 'CTV_T_HR V100 iso BT', 'CTV_T_HR V100 iso BT+EBT', 'CTV_T_IR [cm3] 1', 'CTV_T_IR [cm3] 2', 'CTV_T_IR [cm3] 3', 'CTV_T_IR [cm3] 4', 'CTV_T_IR [cm3] mean', 'CTV_T_IR [cm3] stddev', 'CTV_T_IR D100 iso 1', 'CTV_T_IR D100 iso 2', 'CTV_T_IR D100 iso 3', 'CTV_T_IR D100 iso 4', 'CTV_T_IR D100 iso BT', 'CTV_T_IR D100 iso BT+EBT', 'CTV_T_IR D90 iso 1', 'CTV_T_IR D90 iso 2', 'CTV_T_IR D90 iso 3', 'CTV_T_IR D90 iso 4', 'CTV_T_IR D90 iso BT', 'CTV_T_IR D90 iso BT+EBT', 'CTV_T_IR D98 iso 1', 'CTV_T_IR D98 iso 2', 'CTV_T_IR D98 iso 3', 'CTV_T_IR D98 iso 4', 'CTV_T_IR D98 iso BT', 'CTV_T_IR D98 iso BT+EBT', 'CTV_T_IR V50 iso 1', 'CTV_T_IR V50 iso 2', 'CTV_T_IR V50 iso 3', 'CTV_T_IR V50 iso 4', 'CTV_T_IR V50 iso BT', 'CTV_T_IR V50 iso BT+EBT', 'Sigmoid [cm3] 1', 'Sigmoid [cm3] 2', 'Sigmoid [cm3] 3', 'Sigmoid [cm3] 4', 'Sigmoid [cm3] mean', 'Sigmoid [cm3] stddev', 'Sigmoid 0,1cm3 1', 'Sigmoid 0,1cm3 2', 'Sigmoid 0,1cm3 3', 'Sigmoid 0,1cm3 4', 'Sigmoid 0,1cm3 BT', 'Sigmoid 0,1cm3 BT+EBT', 'Sigmoid 1cm3 1', 'Sigmoid 1cm3 2', 'Sigmoid 1cm3 3', 'Sigmoid 1cm3 4', 'Sigmoid 1cm3 BT', 'Sigmoid 1cm3 BT+EBT', 'Sigmoid 2cm3 1', 'Sigmoid 2cm3 2', 'Sigmoid 2cm3 3', 'Sigmoid 2cm3 4', 'Sigmoid 2cm3 BT', 'Sigmoid 2cm3 BT+EBT', 'Rectum [cm3] 1', 'Rectum [cm3] 2', 'Rectum [cm3] 3', 'Rectum [cm3] 4', 'Rectum [cm3] mean', 'Rectum [cm3] stddev', 'Rectum 0,1cm3 1', 'Rectum 0,1cm3 2', 'Rectum 0,1cm3 3', 'Rectum 0,1cm3 4', 'Rectum 0,1cm3 BT', 'Rectum 0,1cm3 BT+EBT', 'Rectum 1cm3 1', 'Rectum 1cm3 2', 'Rectum 1cm3 3', 'Rectum 1cm3 4', 'Rectum 1cm3 BT', 'Rectum 1cm3 BT+EBT', 'Rectum 2cm3 1', 'Rectum 2cm3 2', 'Rectum 2cm3 3', 'Rectum 2cm3 4', 'Rectum 2cm3 BT', 'Rectum 2cm3 BT+EBT', 'SmallBowel [cm3] 1', 'SmallBowel [cm3] 2', 'SmallBowel [cm3] 3', 'SmallBowel [cm3] 4', 'SmallBowel [cm3] mean', 'SmallBowel [cm3] stddev', 'SmallBowel 0,1cm3 1', 'SmallBowel 0,1cm3 2', 'SmallBowel 0,1cm3 3', 'SmallBowel 0,1cm3 4', 'SmallBowel 0,1cm3 BT', 'SmallBowel 0,1cm3 BT+EBT', 'SmallBowel 1cm3 1', 'SmallBowel 1cm3 2', 'SmallBowel 1cm3 3', 'SmallBowel 1cm3 4', 'SmallBowel 1cm3 BT', 'SmallBowel 1cm3 BT+EBT', 'SmallBowel 2cm3 1', 'SmallBowel 2cm3 2', 'SmallBowel 2cm3 3', 'SmallBowel 2cm3 4', 'SmallBowel 2cm3 BT', 'SmallBowel 2cm3 BT+EBT', 'Bladder [cm3] 1', 'Bladder [cm3] 2', 'Bladder [cm3] 3', 'Bladder [cm3] 4', 'Bladder [cm3] mean', 'Bladder [cm3] stddev', 'Bladder 0,1cm3 1', 'Bladder 0,1cm3 2', 'Bladder 0,1cm3 3', 'Bladder 0,1cm3 4', 'Bladder 0,1cm3 BT', 'Bladder 0,1cm3 BT+EBT', 'Bladder 1cm3 1', 'Bladder 1cm3 2', 'Bladder 1cm3 3', 'Bladder 1cm3 4', 'Bladder 1cm3 BT', 'Bladder 1cm3 BT+EBT', 'Bladder 2cm3 1', 'Bladder 2cm3 2', 'Bladder 2cm3 3', 'Bladder 2cm3 4', 'Bladder 2cm3 BT', 'Bladder 2cm3 BT+EBT', 'LT Ureter [cm3] 1', 'LT Ureter [cm3] 2', 'LT Ureter [cm3] 3', 'LT Ureter [cm3] 4', 'LT Ureter [cm3] mean', 'LT Ureter [cm3] stddev', 'LT Ureter 0,1cm3 1', 'LT Ureter 0,1cm3 2', 'LT Ureter 0,1cm3 3', 'LT Ureter 0,1cm3 4', 'LT Ureter 0,1cm3 BT', 'LT Ureter 0,1cm3 BT+EBT', 'LT Ureter 1cm3 1', 'LT Ureter 1cm3 2', 'LT Ureter 1cm3 3', 'LT Ureter 1cm3 4', 'LT Ureter 1cm3 BT', 'LT Ureter 1cm3 BT+EBT', 'LT Ureter 2cm3 1', 'LT Ureter 2cm3 2', 'LT Ureter 2cm3 3', 'LT Ureter 2cm3 4', 'LT Ureter 2cm3 BT', 'LT Ureter 2cm3 BT+EBT', 'RT Ureter [cm3] 1', 'RT Ureter [cm3] 2', 'RT Ureter [cm3] 3', 'RT Ureter [cm3] 4', 'RT Ureter [cm3] mean', 'RT Ureter [cm3] stddev', 'RT Ureter 0,1cm3 1', 'RT Ureter 0,1cm3 2', 'RT Ureter 0,1cm3 3', 'RT Ureter 0,1cm3 4', 'RT Ureter 0,1cm3 BT', 'RT Ureter 0,1cm3 BT+EBT', 'RT Ureter 1cm3 1', 'RT Ureter 1cm3 2', 'RT Ureter 1cm3 3', 'RT Ureter 1cm3 4', 'RT Ureter 1cm3 BT', 'RT Ureter 1cm3 BT+EBT', 'RT Ureter 2cm3 1', 'RT Ureter 2cm3 2', 'RT Ureter 2cm3 3', 'RT Ureter 2cm3 4', 'RT Ureter 2cm3 BT', 'RT Ureter 2cm3 BT+EBT', 'VaginalWall LATE [cm3] 1', 'VaginalWall LATE [cm3] 2', 'VaginalWall LATE [cm3] 3', 'VaginalWall LATE [cm3] 4', 'VaginalWall LATE [cm3] mean', 'VaginalWall LATE [cm3] stddev', 'VaginalWall LATE 0,1cm3 1', 'VaginalWall LATE 0,1cm3 2', 'VaginalWall LATE 0,1cm3 3', 'VaginalWall LATE 0,1cm3 4', 'VaginalWall LATE 0,1cm3 BT', 'VaginalWall LATE 0,1cm3 BT+EBT', 'VaginalWall LATE 1cm3 1', 'VaginalWall LATE 1cm3 2', 'VaginalWall LATE 1cm3 3', 'VaginalWall LATE 1cm3 4', 'VaginalWall LATE 1cm3 BT', 'VaginalWall LATE 1cm3 BT+EBT', 'VaginalWall LATE 2cm3 1', 'VaginalWall LATE 2cm3 2', 'VaginalWall LATE 2cm3 3', 'VaginalWall LATE 2cm3 4', 'VaginalWall LATE 2cm3 BT', 'VaginalWall LATE 2cm3 BT+EBT', 'VaginalWall EARLY [cm3] 1', 'VaginalWall EARLY [cm3] 2', 'VaginalWall EARLY [cm3] 3', 'VaginalWall EARLY [cm3] 4', 'VaginalWall EARLY [cm3] mean', 'VaginalWall EARLY [cm3] stddev', 'VaginalWall EARLY 0,1cm3 1', 'VaginalWall EARLY 0,1cm3 2', 'VaginalWall EARLY 0,1cm3 3', 'VaginalWall EARLY 0,1cm3 4', 'VaginalWall EARLY 0,1cm3 BT', 'VaginalWall EARLY 0,1cm3 BT+EBT', 'VaginalWall EARLY 1cm3 1', 'VaginalWall EARLY 1cm3 2', 'VaginalWall EARLY 1cm3 3', 'VaginalWall EARLY 1cm3 4', 'VaginalWall EARLY 1cm3 BT', 'VaginalWall EARLY 1cm3 BT+EBT', 'VaginalWall EARLY 2cm3 1', 'VaginalWall EARLY 2cm3 2', 'VaginalWall EARLY 2cm3 3', 'VaginalWall EARLY 2cm3 4', 'VaginalWall EARLY 2cm3 BT', 'VaginalWall EARLY 2cm3 BT+EBT', 'PT ICRURV Point 1', 'PT ICRURV Point 2', 'PT ICRURV Point 3', 'PT ICRURV Point 4', 'PT ICRURV Point BT', 'PT ICRURV Point BT + EBT', 'PT A Left 1', 'PT A Left 2', 'PT A Left 3', 'PT A Left 4', 'PT A Left BT', 'PT A Left BT + EBT', 'PT A Right 1', 'PT A Right 2', 'PT A Right 3', 'PT A Right 4', 'PT A Right BT', 'PT A Right BT + EBT']]
    for pathName in pdfList:
        string = ''
        dictionary = {}
        
        tempList = re.findall(r'\d+', pathName)
        for num in tempList:
            if len(num) == 7:
                dictionary['MRN'] = num
                print(num)
        
        with pdfplumber.open(pathName) as pdf: # uses pdfplumber to extract text from the pdf
            pages = pdf.pages[:]
            for page in pages:
                if page.extract_text():
                    string = string + '\n' + page.extract_text()
        
        if 'MRN' not in dictionary:
            strList = string.split('PATIENT ,  ID-number ')
            if len(strList) == 1:
                strList = string.split('PATIENT ,  ID-number')
            
            strList2 = strList[1].split('\n')
            strList3 = strList2[0].split(' ')
            for item in strList3:
                try:
                    dictionary['MRN'] = int(item)
                except:
                    pass
        if 'MRN' not in dictionary:
            print('MRN not in:\t', pathName)
            dictionary['MRN'] = ''
            
        strList = string.split('PATIENT ,  ID-number ')
        try:
            strList2 = strList[1].split('\n')
            strList3 = strList2[0].split(' ')
            isInt = False
            for m, item in enumerate(strList3):
                try:
                    f = int(item)
                    s = ' '
                    tempString1 = s.join(strList3[0:m])
                    isInt = True
                except:
                    pass
            
            if not isInt:
                dictionary['patientName'] = strList2[0]
            else:
                dictionary['patientName'] = tempString1
        except:
            dictionary['patientName'] = ''
        
        strList = string.split('date ')
        if len(strList) > 1:
            if 'dose values in Gy' in strList[1]:
                strList2 = strList[1].split(' dose values in Gy')
            else:
                strList2 = strList[1].split('\n')
            strList3 = strList2[0].split(' ')
            while len(strList3) < 4:
                strList3.append('')
            if len(strList3) > 4:
                strList3 = strList3[:4]
            dictionary['dates'] = strList3
        else:
            dictionary['dates'] = ['', '', '', '']
        
        strList = string.split('total dose ')
        strList2 = strList[1].split(' ')
        dictionary['totalDose'] = strList2[0]
        
        strList = string.split('applicator(s): type ')
        strList2 = strList[1].split('\n')
        appType1 = strList2[0].split(' ')
        appType = []
        for type1 in appType1:
            if type1 != 'BT' and type1 != 'EBT' and type1 != '+':
                appType.append(type1)
        dictionary['appType'] = appType
        
        strList = string.split('applicator(s): dimensions')
        strList2 = strList[1].split('\n')
        dictionary['appDim'] = strList2[0].split(' ')
        
        if 'TRAK' in string:
            strList = string.split('TRAK ')
            strList2 = strList[1].split('\n')
            dictionary['TRAK'] = strList2[0].split(' ')
        else:
            dictionary['TRAK'] = ['', '', '', '']
        if type(dictionary['TRAK']) == dict:
            dictionary['TRAK'] = ['', '', '', '']
        
        strList = string.split('\n') 
        strList = strList[17:]
        listList = []
        tempList = []
        first = True
        for i, x in enumerate(strList):
            y = x.split(' ')
            if (len(y) < 3 and 'iso' not in y) or (len(y[0]) != 1 and 'cm3' not in y[0] and 'iso' not in y and 'Left' not in y and 'Right' not in y and 'ICRU Point' not in y):
                if not first:
                    listList.append(tempList)
                    tempList = [x]
                else:
                    tempList = [x]
                    first = False
            else:
                tempList.append(x)
        listList.append(tempList)
        
        for lst in listList:
            if lst == ['Fx1']:
                print(lst)
                break
            #create sub dictionary for each mini table to add with table header as key
            subDictionary = {}
            for element in lst:
                if '[cm3]' in element or 'iso' in element or 'volume' in element or '[a/b=' in element or 'ï›ï¡ï€¯ï¢ï€½ï€±' in element or '\uf05b\uf061' in element or '[Î±/Î²=' in element:
                    subList = element.split(' ')
                    
                    for i, item in enumerate(subList):
                        if '%' in item:
                            subList[i] = item.replace('%', '')
                    
                    if 'iso' in element:
                        if element == 'iso':
                            continue
                        s = ' '
                        tempString = s.join(subList[0:3])
                    elif lst[0] == 'PT A':
                        if 'left' not in subDictionary:
                            tempString = 'left'
                        else:
                            tempString = 'right'
                    elif 'Left' in lst[0] or 'LEFT' in lst[0]:
                        tempString = 'left'
                        lst.insert(0, 'PT A1')
                    elif 'Right' in lst[0] or 'RIGHT' in lst[0]:
                        tempString = 'right'
                        lst.insert(0, 'PT A2')
                    else:
                        if element == '[cm3]':
                            continue
                        tempString = element[:5]
                    
                    try:
                        if len(subList) == 5:
                            lineList = subList[1:]
                            lineList.extend(('', ''))
                            subDictionary[tempString] = lineList
                            continue
                    
                        q = float(subList[-7])
                        lineList = subList[-7:-3]
                        lineList.extend(subList[-2:])
                        
                        if str(lineList[3]) == '0.0' or str(lineList[3]) == '0.00':
                            lineList[3] = ''
                        subDictionary[tempString] = lineList
                    except:
                        try:
                            q = float(subList[-6])
                            if str(subList[-3]) == '0.0' or str(subList[-3]) == '0.00':
                                subList[-3] = ''
                            
                            subDictionary[tempString] = subList[-6:]
                        except:
                            lineList = subList[-5:-2]
                            lineList.append('')
                            lineList.extend(subList[-2:])
                            
                            try:
                                if str(lineList[3]) == '0.0' or str(lineList[3]) == '0.00':
                                    lineList[3] = ''
                            except:
                                print('Line list: ', lineList)
                                print('Element: ', element)
                                print('lst[0]: ', lst[0])
                                return None
                            
                            subDictionary[tempString] = lineList
                    
                    if '[cm3]' in element:
                        if 'Vagina' in lst[0]:
                            subDictionary['LE'] = subList[1]  
            dictionary[lst[0]] = subDictionary
        #print(dictionary)
        
        outputList = dictionaryToOutputList(dictionary)
        outList.append(outputList)
    
    fileName = 'N:\\Weersink\\Brachy_HDR\\ForMadrigal\\Extraction Results\\Dose Extraction ' + folder + '.xlsx'
    
    df = pd.DataFrame(outList)
    new_header = df.iloc[0]     # grab the first row for the header
    df = df[1:]                 # take the data less the header row
    df.columns = new_header     # set the header row as the df header
    df.to_excel(fileName, sheet_name=(folder[:24]))


def dictionaryToOutputList(dictionary):
    # getting number of doses based on numbers in CTV-HR [cm3] - or GTV [cm3] if CTV-HR is not in the dictionary
    for key in dictionary:
        if 'CTV' in key and 'HR' in key:
            try:
                if dictionary[key]['[cm3]'][3] == '':
                    doseNum = 3
                else:
                    doseNum = 4
            except:
                doseNum = ''
                print(dictionary[key])
        elif 'GTV' in key:
            try:
                if dictionary[key]['[cm3]'][3] == '':
                    doseNum = 3
                else:
                    doseNum = 4
            except:
                doseNum = ''
                print(dictionary[key])
        else:
            doseNum = ''
    
    # initializing the pdfs output list
    outputList = [dictionary['MRN'], dictionary['patientName'], doseNum]
    outputList.extend(dictionary['dates'])
    outputList.append(dictionary['totalDose'])
    
    parametersList = ['appType', 'appDim', 'TRAK']
    for parameter in parametersList:
        if len(dictionary[parameter]) > 4:
            outputList.extend(dictionary[parameter][:4])
        else:
            while len(dictionary[parameter]) < 4:
                try:
                    dictionary[parameter].append('')
                except:
                    dictionary[parameter] = ['', '', '', '']
            outputList.extend(dictionary[parameter])
    
    blankList1 = ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '']
    blankList2 = ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '']
    
    # add each table to list, using sections of the header names always present to identify the key, then adding each line one by one
    # if the table is not present, empty strings are added in their place
    headerList1 = [['GTV', ''], ['CTV', 'HR'], ['CTV', 'IR']]
    for headerList in headerList1:
        inDict = False  
        cm3added = False
        for key in dictionary:
            if headerList[0] in key and headerList[1] in key:
                try:
                    outputList.extend(dictionary[key]['[cm3]'])
                    if len(dictionary[key]['[cm3]']) == 4:
                        outputList.extend(['', ''])
                except:
                    outputList.extend(['', '', '', '', '', ''])
                cm3added = True
                
                try:
                    outputList.extend(dictionary[key]['D 100 iso'])
                    outputList.extend(dictionary[key]['D 90 iso'])
                    if 'D 98 iso' in dictionary[key]:
                        outputList.extend(dictionary[key]['D 98 iso'])
                    else:
                        outputList.extend(['', '', '', '', '', ''])
                    if 'V 50 ' in dictionary[key]:
                        outputList.extend(dictionary[key]['V 50 '])
                    else:
                        outputList.extend(dictionary[key]['V 100'])
                    inDict = True
                except:
                    try:
                        outputList.extend(dictionary[key]['D 100'])
                        outputList.extend(dictionary[key]['D 90 '])
                        if 'D 98 ' in dictionary[key]:
                            outputList.extend(dictionary[key]['D 98 '])
                        else:
                            outputList.extend(['', '', '', '', '', ''])
                        if 'V 50 ' in dictionary[key]:
                            outputList.extend(dictionary[key]['V 50 '])
                        else:
                            outputList.extend(dictionary[key]['V 100'])
                        inDict = True
                    except:
                        print(headerList[0], ' ', headerList[1], ' KeyError')
                        print(dictionary[key])
        if not inDict:
            outputList.extend(blankList1)
        if not cm3added:
            outputList.extend(['', '', '', '', '', ''])
    
    inDict = False 
    cm3added = False
    for key in dictionary:
        if 'Sigmoid' in key:
            try:
                outputList.extend(dictionary[key]['[cm3]'])
            except:
                outputList.extend(['', '', '', '', '', ''])
            cm3added = True
            try:
                outputList.extend(dictionary[key]['0,1cm3 - Diso'])
                outputList.extend(dictionary[key]['1cm3 - Diso'])
                outputList.extend(dictionary[key]['2cm3 - Diso'])
                inDict = True
            except:
                try:
                    outputList.extend(dictionary[key]['0,1cm'])
                    outputList.extend(dictionary[key]['1cm3 '])
                    outputList.extend(dictionary[key]['2cm3 '])
                    inDict = True
                except:
                    print('Sigmoid KeyError')
                    print(dictionary[key])
    if not inDict:
        outputList.extend(blankList2)
    if not cm3added:
        outputList.extend(['', '', '', '', '', ''])
        
    inDict = False    
    cm3added = False
    for key in dictionary:
        if ('Rectum' in key or 'Rctum' in key) and 'ICRU' not in key:
            try:
                outputList.extend(dictionary[key]['[cm3]'])
            except:
                outputList.extend(['', '', '', '', '', ''])
            cm3added = True
            try:
                outputList.extend(dictionary[key]['0,1cm3 - Diso'])
                outputList.extend(dictionary[key]['1cm3 - Diso'])
                outputList.extend(dictionary[key]['2cm3 - Diso'])
                inDict = True
            except KeyError:
                try:
                    outputList.extend(dictionary[key]['0,1cm'])
                    outputList.extend(dictionary[key]['1cm3 '])
                    outputList.extend(dictionary[key]['2cm3 '])
                    inDict = True
                except:
                    print('Rectum KeyError')
                    print(dictionary[key])      
    if not inDict:
        outputList.extend(blankList2)
    if not cm3added:
        outputList.extend(['', '', '', '', '', ''])
    
    headerList2 = [['Small', 'Bowel'], ['Bladder', ''], ['LT', 'Ureter'], ['RT', 'Ureter']]
    for headerList in headerList2:
        inDict = False     
        cm3added = False 
        for key in dictionary:
            if headerList[0] in key and headerList[1] in key:
                try:
                    outputList.extend(dictionary[key]['[cm3]'])
                except:
                    outputList.extend(['', '', '', '', '', ''])
                cm3added = True
                try:
                    outputList.extend(dictionary[key]['0,1cm3 - Diso'])
                    outputList.extend(dictionary[key]['1cm3 - Diso'])
                    outputList.extend(dictionary[key]['2cm3 - Diso'])
                    inDict = True
                except:
                    try:
                        outputList.extend(dictionary[key]['0,1cm'])
                        outputList.extend(dictionary[key]['1cm3 '])
                        outputList.extend(dictionary[key]['2cm3 '])
                        inDict = True
                    except:
                        print(headerList[0], headerList[1], 'KeyError')
                        print(dictionary[key])
        if not inDict:
            outputList.extend(blankList2)
        if not cm3added:
            outputList.extend(['', '', '', '', '', ''])
    
    stageList = ['LATE', 'EARL'] 
    for stage in stageList:
        inDict = False   
        cm3added = False   
        for key in dictionary:
            if 'Vagina' in key:
                if stage in dictionary[key]['LE']:
                    try:
                        outputList.extend(dictionary[key]['[cm3]'])
                    except:
                        outputList.extend(['', '', '', '', '', ''])  
                    cm3added = True
                    try:
                        outputList.extend(dictionary[key]['0,1cm3 - Diso'])
                        outputList.extend(dictionary[key]['1cm3 - Diso'])
                        try:
                            outputList.extend(dictionary[key]['2cm3 - Diso'])
                        except:
                            outputList.extend(['', '', '', '', '', ''])
                        inDict = True
                    except:
                        try:
                            outputList.extend(dictionary[key]['0,1cm'])
                            outputList.extend(dictionary[key]['1cm3 '])
                            try:
                                outputList.extend(dictionary[key]['2cm3 '])
                            except:
                                outputList.extend(['', '', '', '', '', ''])
                            inDict = True
                        except:
                            print('Vaginal Wall KeyError')
                            print(dictionary[key])
        if not inDict:
            outputList.extend(blankList2)
        if not cm3added:
            outputList.extend(['', '', '', '', '', ''])
    
    inDict = False    
    for key in dictionary:
        if 'ICRU' in key and 'Rectum' not in key and 'Rctum' not in key:
            try:
                outputList.extend(dictionary[key]['ICRU Point -'])
                inDict = True
            except KeyError:
                print('ICRU KeyError')
    if not inDict:
        outputList.extend(['', '', '', '', '', ''])
    
    inDict = False    
    for key in dictionary:
        if 'PT A' in key:
            if key == 'PT A1':
                try:
                    outputList.extend(dictionary[key]['left'])
                    inDict = True
                except:
                    print('PT A: ', dictionary[key])
            elif key == 'PT A2':
                try:
                    outputList.extend(dictionary[key]['right'])
                    inDict = True
                except:
                    print('PT A: ', dictionary[key])
            try:
                outputList.extend(dictionary[key]['left'])
                outputList.extend(dictionary[key]['right'])
                inDict = True
            except:
                print('PT A: ', dictionary[key])
    if not inDict:
        outputList.extend(['', '', '', '', '', '', '', '', '', '', '', ''])
    
    for i, item in enumerate(outputList):
        try:
            outputList[i] = float(item)
        except:
            pass
        
    return outputList
        
   
if __name__ == '__main__':   
    # INSTRUCTIONS
    
    # If you want to get values from the normal file explorer, use getValues
    # If you want to get values from a compiled folder, use getCompiledValues

    # To run the code, have the function name uncommented 
    # NOTE: only have the one that you want to use uncommented, otherwise you'll be waiting longer than you need to
    # Have the appropriate folder name and (if applicable) year. Make sure they are strings
    # Hit run
    # The Excel file will be written to ForMadrigal\Extraction Results
    # Enjoy!
    
    #getValues('Gynae_R&T', '2014')
    getCompiledValues('Brachy_Template')
    