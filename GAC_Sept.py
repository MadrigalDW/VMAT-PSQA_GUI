"""
Created on Tue May 11 14:17:42 2021
@author: weersim
"""
from mostRecent import mostRecentPDFs
from query_MosaiQ import query_mosaiq
import glob, pdfplumber, os.path, datetime

def getArcCheck(MRN, fieldIndexes, inputDate=''):
    
    print('Entering getArcCheck ...')
    
    pdfList = glob.glob('Q:\\IMRTQA/*' + MRN + '/**/*.pdf', recursive = True) # finds all pdfs in folder(s) with the MRN
    if inputDate != '':
        pdfList.extend(glob.glob('Q:\\IMRTQA\\2020 IMRT VMAT TBI/*' + MRN + '/**/*.pdf', recursive = True))
    
    # checks that there are pdfs in the target file, exits if not
    
    try:
        pdfList[0]
    except IndexError: # if there aren't any pdfs, checks for MosaiQ queries
        print('Trying mosaiq')
        QAfields = query_mosaiq(MRN)
        print('Program ran')
        try:
            QAfields[0]
            return "There are no PDFs for the patient you queried. Please manually check the Mosaiq queries."
        except:
            return 'There are no PDFs or QA fields for the MRN you searched.'
    try: # finds the most recent date
        mostRecentDate = '0000-00-00'  
        if inputDate == '':
            for pathName in pdfList:
                date = str(datetime.datetime.fromtimestamp(os.path.getmtime(pathName)))[0:10] # gets date the pdf was last modified
                # if the date of the current pdf is more recent than the current mostRecentDate, the date becomes the mostRecentDate
                # if the year is more recent than mostRecentDate or year is same and month is more recent or year and month are same and day is more recent
                if int(date[0:4]) > int(mostRecentDate[0:4]) or (int(date[0:4]) == int(mostRecentDate[0:4]) and int(date[5:7]) > int(mostRecentDate[5:7])) or (int(date[0:4]) == int(mostRecentDate[0:4]) and int(date[5:7]) == int(mostRecentDate[5:7]) and int(date[8:]) > int(mostRecentDate[8:])):
                    mostRecentDate = date
                
        else: # takes the most recent date from before the inputDate
            for pathName in pdfList:
                date = str(datetime.datetime.fromtimestamp(os.path.getmtime(pathName)))[0:10]
                ## TODO: simplify ## 
                # if the year is earlier than input year, or year is same and month is earlier than input year, or year and month are same and day is earlier or same as input day
                if int(date[0:4]) < int(inputDate[0:4]) or (int(date[0:4]) == int(inputDate[0:4]) and int(date[5:7]) < int(inputDate[5:7])) or (int(date[0:4]) == int(inputDate[0:4]) and int(date[5:7]) == int(inputDate[5:7]) and int(date[8:]) <= int(inputDate[8:])):
                    # if the year is more recent than mostRecentDate or year is same and month is more recent or year and month are same and day is more recent
                    if int(date[0:4]) > int(mostRecentDate[0:4]) or (int(date[0:4]) == int(mostRecentDate[0:4]) and int(date[5:7]) > int(mostRecentDate[5:7])) or (int(date[0:4]) == int(mostRecentDate[0:4]) and int(date[5:7]) == int(mostRecentDate[5:7]) and int(date[8:]) > int(mostRecentDate[8:])):
                        mostRecentDate = date
    except:
        print('Date sorting error')
        return 'Sorry, there was an error selecting the PDFs.'   # error occurs when there's an error finding the mostRecentDate       
    
    
    # if it does not find a field ID in the parsed PDFs, exclude those from the list
    twoPages = False # used for differences in old vs. new formatting
    valuesDict = {} # dictionary that will be returned
    removeList = [] # pdfs to remove from pdfList
    for pathName in pdfList:
        fieldBool = False
        with pdfplumber.open(pathName) as pdf: # uses pdfplumber to extract text from the pdf
            firstPage = pdf.pages[0]
            fullStr = firstPage.extract_text() # string of text from pdf
        if '% Passed' in fullStr: # only takes later part of string if it's ArcCheck, to ensure there isn't a false positive for the beam set indexes
            strList = fullStr.split('% Passed')
            fullStr = strList[1]
        if 'IQM Report Summary:' not in fullStr:
            for item in fieldIndexes: # checking that the field index is in the pdf; if it isn't, we don't want to read it
                if item in fullStr:
                    fieldBool = True
                elif '\n(y,x) cm\n' in fullStr: 
                    # double checking that if there are letters mashed in between parts of the field index eg. N A1o.1tes, it is still counted for reading
                    strList = fullStr.split('\n(y,x) cm\n')
                    strList2 = strList[1].split('\n')
                    keyPart = strList2[0]
                    keyPart = keyPart.replace('N', '', 1)
                    removeLetters = [' ', 'o', 't', 'e', 's']
                    for letter in removeLetters:
                        keyPart = keyPart.replace(letter, '')
                    if item in keyPart:
                        fieldBool = True
            if not fieldBool:
                removeList.append(pathName)
        else:
            # if IQM in fullStr, must check there aren't more recent pdfs
            date = str(datetime.datetime.fromtimestamp(os.path.getmtime(pathName)))[0:10]
            if date != mostRecentDate:
                removeList.append(pathName)
    

    
    for pathName in removeList: # removing the pdfs we don't want to run through from pdfList
        pdfList.remove(pathName)
    
    if type(pdfList) == str:
        return pdfList
    
    
    for pathName in pdfList: # runs through each pdf in pdfList
        #print(pathName)
        with pdfplumber.open(pathName) as pdf: # uses pdfplumber to extract text from the pdf
            firstPage = pdf.pages[0]
            fullStr = firstPage.extract_text()
            if len(pdf.pages) == 2:
                secondPage = pdf.pages[1]
                fullStr = fullStr + secondPage.extract_text()
        
        if 'ArcCHECK' not in fullStr:
            if 'IQM Report Summary:' in fullStr: # checks if file is IQM
                valuesDict['pathName'] = pathName
                valuesDict['IQM'] = 'Most recent file is IQM Report Summary. Please click "Open PDFs" to check files manually.'
                return valuesDict
            else:
                for item in fieldIndexes: # if the file isn't IQM or ArcCheck, it's Delta4
                    if item in fullStr:
                        Delta4 = {} # build Delta4 dictionary with necessary values
                        
                        # extracting values from Delta 4 pdf
                        strList = fullStr.split(' cGy')
                        str1 = strList[2][:17]
                        str1List = str1.split('%')
                        if '' in str1List:
                            str1List.remove('')
                        str1 = ''
                        listList = [str1List]
                        strList2 = [str1]
                        
                        if len(strList) >= 4:
                            str2 = strList[3][:17]
                            str2List = str2.split('%')
                            listList.append(str2List)
                            str2 = ''
                            strList2.append(str2)
                        if len(strList) >= 5:
                            str3 = strList[4][:17]
                            str3List = str3.split('%')
                            listList.append(str3List)
                            str3 = ''
                            strList2.append(str3)
                        if len(strList) >= 6:
                            str4 = strList[5][:17]
                            str4List = str4.split('%')
                            listList.append(str4List)
                            str4 = ''
                            strList2.append(str4)
                        
                        for i, x in enumerate(listList):
                            for j, y in enumerate(str1List):
                                strList2[i] = strList2[i] + listList[i][j] + '\t' # compile results in a list
                        
                        percentList = fullStr.split('%\n')
                        beamSet = percentList[1][0]
                        keyName = 'Delta4' + item
                        Delta4[beamSet] = strList2 # add values for pdf in dict using beamset as key
                        Delta4['pathName'] = pathName # add pathname
                        valuesDict[keyName] = Delta4 # add Delta4 dict under keyName of 'Delta4' and beam set index
                        break
                    else:
                        continue
                continue
        # parse the ArcCheck PDFs now
        if len(pdf.pages) == 1: # runs parse1page if pdf is 1 page long
            pdfKey, pdfValues = parse1page(pathName, pdf, fullStr)
            valuesDict[pdfKey] = pdfValues
            fullStr1 = fullStr
            twoPages = False
        elif len(pdf.pages) == 2: # runs parse2pages if pdf is 2 pages long
            fullStr = fullStr + pdf.pages[1].extract_text()
            pdfKey, pdfValues = parse2pages(pathName, pdf, fullStr)
            valuesDict[pdfKey] = pdfValues
            fullStr1 = fullStr
            twoPages = True
        else:
            return 'The ArcCheck PDF is more than two pages long. Please manually check documents.'

    try: # checks that there was an ArcCheck PDF that ran through; if not, sends error message
        fullStr1[0]
    except UnboundLocalError:
        return "There are no ArcCheck PDFs in the patient file you searched."
     
    # adds extra information. different versions for old vs. new formats    
    if twoPages:
        # add values which are consistent to all pdfs to the dictionary
        splitList = ['Patient Name ', 'Patient ID ', '\nQA Date ']
        keyList = ['Patient Name', 'Patient ID', 'Plan Date']
        
        for x, split in enumerate(splitList):
            strList = fullStr1.split(split)
            strList2 = strList[1].split('\n')
            valuesDict[keyList[x]] = strList2[0]
        
        strList = fullStr1.split('(DTA/Gamma using ')
        strList2 = strList[1].split(' ')
        valuesDict['DTA Analysis Mode'] = strList2[0] 
    else:
        # add values which are consistent to all pdfs to the dictionary
        splitList = ['Patient Name  : ', 'Patient ID  : ', 'Plan Date  : ', 'Energy  : ']
        keyList = ['Patient Name', 'Patient ID', 'Plan Date', 'Energy']
        
        for x, split in enumerate(splitList):
            strList = fullStr1.split(split)
            strList2 = strList[1].split('\n')
            valuesDict[keyList[x]] = strList2[0]
        
        strList = fullStr1.split('*DTA/Gamma is using ')
        strList2 = strList[1].split(' ')
        valuesDict['DTA Analysis Mode'] = strList2[0]
    
    # return dictionary
    return valuesDict

def parse1page(pathName, pdf, fullStr):
    # takes info from pdf to build pdf name, create empty dictionary for individual pdf
        if 'Absolute Dose Comparison' in fullStr:
            letter1 = 'A'
        elif 'Relative Comparison' in fullStr:
            letter1 = 'R'
        else:
            print(pathName)
            print('PDF Error')
        
        strList = fullStr.split('\n(y,x) cm\n')
        strList2 = strList[1].split('\n')
        keyPart = strList2[0] # takes line that has the beam set index in it
        keyPart = keyPart.replace('N', '', 1)
        removeLetters = [' ', 'o', 't', 'e', 's']
        for letter in removeLetters: # removes excess letters
            keyPart = keyPart.replace(letter, '')
        
        if keyPart == '' and 'Notes' in fullStr: # if beam set is on line below 'Notes', extracts that instead
            strList = fullStr.split('Notes\n')
            strList2 = strList[1].split('\n')
            keyPart = strList2[0]
            if ' ' in keyPart:
                keyPart = keyPart.replace(' ', '')
        if keyPart == '':
            keyPart = 'Nothing'
            
        if keyPart not in pathName:
            print('Warning: Beam set index in PDF does not match PDF name.\nBeam set index:\t', keyPart, '\nPath name:\t\t', pathName, '\n')
        
        pdfKey = letter1 + 'D-' + keyPart # name which will serve as key when adding PDF dict to full dictionary
        pdfValues = {} # dictionary with PDF values
        
        # these 4 try/except statements check for the correct threshold values, and stop the program if they're not there
        thresholdCorrect = True
        try:
            fullStr.index('Difference (%)  : 3.0')
        except:
            thresholdCorrect = False
            return "Percent difference is incorrect. Please manually check documents."
        try:
            fullStr.index('Distance (mm)  : 2.0')
        except:
            thresholdCorrect = False
            return "Comparison distance is incorrect. Please manually check documents."
        try:
            fullStr.index('Threshold (%)  : 10.0')
        except:
            thresholdCorrect = False
            return "Threshold percent is incorrect. Please manually check documents."
        if pdfKey[0] == 'A':
            try:
                fullStr.index('Use Global %  : No')
            except:
                thresholdCorrect = False
                raise Exception("Global % should be set to No.")
        
        # by splitting the string directly before and after the desired value, we get the % pass rate
        strList = fullStr.split('% Passed  : ') 
        strList2 = strList[1].split('\n')
        numOut = float(strList2[0])
        
        pdfValues['% Passed'] = numOut
        pdfValues["Parameters"] = thresholdCorrect
        pdfValues['pathName'] = pathName
        
        splitList = ['SSD  : ', 'SDD  : ', 'Depth  : ', 'Total Points  : ', 'Passed  : ', 'Failed  : ']
        keyList = ['SSD', 'SDD', 'Depth', 'Total Points', 'Passed', 'Failed']
        
        for x, split in enumerate(splitList):
            strList = fullStr.split(split)
            strList2 = strList[1].split('\n')
            pdfValues[keyList[x]] = strList2[0]
        
        return pdfKey, pdfValues

def parse2pages(pathName, pdf, fullStr):
        # takes info from pdf to build pdf name, create empty dictionary for individual pdf
        if 'Absolute Dose Comparison' in fullStr:
            letter1 = 'A'
        elif 'Relative Comparison' in fullStr:
            letter1 = 'R'
        else:
            print(pathName)
            print('PDF Error')
        
        strList = fullStr.split('Notes\n')
        strList2 = strList[1].split('\n')
        keyPart = strList2[0]
        
        if keyPart == '':
            keyPart = 'Nothing'
        
        if keyPart not in pathName:
            print('Warning: Beam set index in PDF does not match PDF name.')
        
        pdfKey = letter1 + 'D-' + keyPart # name which will serve as key when adding PDF dict to full dictionary
        pdfValues = {} # dictionary with PDF values
        
        # these 3 if statements check for the correct threshold values, and stop the program if they're not there
        thresholdCorrect = True
        try:
            fullStr.index('Difference (%) 3.0')
        except:
            thresholdCorrect = False
            return "Percent difference is incorrect. Please manually check documents."
        try:
            fullStr.index('Distance (mm) 2.0')
        except:
            thresholdCorrect = False
            return "Comparison distance is incorrect. Please manually check documents."
        try:
            fullStr.index('Threshold (%) 10.0')
        except:
            thresholdCorrect = False
            return "Threshold percent is incorrect. Please manually check documents."
        if pdfKey[0] == 'A':
            try:
                fullStr.index('Use Global (%) No')
            except:
                thresholdCorrect = False
                raise Exception("Global % should be set to No.")
        
        # by splitting the string directly before and after the desired value, we get the % pass rate
        strList = fullStr.split('Pass (%) ') 
        strList2 = strList[1].split('\n')
        numOut = float(strList2[0])
        
        pdfValues['% Passed'] = numOut
        pdfValues["Parameters"] = thresholdCorrect
        pdfValues['pathName'] = pathName
        
        splitList = ['Total Points ', 'Pass ', 'Fail ']
        keyList = ['Total Points', 'Passed', 'Failed']
        
        for x, split in enumerate(splitList):
            strList = fullStr.split(split)
            strList2 = strList[1].split('\n')
            pdfValues[keyList[x]] = strList2[0]
        
        strList = fullStr.split('Pass ')
        strList2 = strList[2].split('\n')
        pdfValues['Passed'] = strList2[0]
        
        return pdfKey, pdfValues
        
    


def getArcCheck2(MRN, planName, fieldIndexes, inputDate=''):
    pdfList = glob.glob('Q:\\IMRTQA/*' + MRN + '/**/*' + planName + '*/**/*.pdf', recursive = True) # finds all pdfs in folder(s) with the MRN
    
    # checks that there are pdfs in the target file, exits if not
    try:
        pdfList[0]
    except IndexError:
        return "There are no PDFs in the patient file you searched."
    
    if planName == '':
        pdfList = mostRecentPDFs(pdfList, fieldIndexes, inputDate)
        if type(pdfList) == str:
            return pdfList
    else:
        if len(pdfList) > 2:
            return 'Plan name is not unique.'
    
    valuesDict = {}
    twoPages = False
    for pathName in pdfList: # runs through each pdf in pdfList
        with pdfplumber.open(pathName) as pdf: # uses pdfplumber to extract text from the pdf
            firstPage = pdf.pages[0]
            fullStr = firstPage.extract_text()
            if len(pdf.pages) >= 2:
                fullStr = fullStr + pdf.pages[1].extract_text()
        
        if 'ArcCHECK' not in fullStr:
            continue
        
        if len(pdf.pages) == 1:
            pdfKey, pdfValues = parse1MRL(pathName, pdf, fullStr)
            valuesDict[pdfKey] = pdfValues
            fullStr1 = fullStr
            twoPages = False
        elif len(pdf.pages) == 2:
            pdfKey, pdfValues = parse2MRL(pathName, pdf, fullStr)
            valuesDict[pdfKey] = pdfValues
            fullStr1 = fullStr
            twoPages = True
        else:
            return 'The ArcCheck PDF is more than two pages long. Please manually check documents.'
    
    try:
        fullStr1[0]
    except UnboundLocalError:
        raise UnboundLocalError
        
    # adds extra information. different versions for old vs. new formats    
    if twoPages:
        # add values which are consistent to all pdfs to the dictionary
        splitList = ['Patient Name ', 'Patient ID ', '\nQA Date ']
        keyList = ['Patient Name', 'Patient ID', 'Plan Date']
        
        for x, split in enumerate(splitList):
            strList = fullStr1.split(split)
            strList2 = strList[1].split('\n')
            valuesDict[keyList[x]] = strList2[0]
        
        strList = fullStr1.split('(DTA/Gamma using ')
        strList2 = strList[1].split(' ')
        valuesDict['DTA Analysis Mode'] = strList2[0] 
    else:
        # add values which are consistent to all pdfs to the dictionary
        splitList = ['Patient Name  : ', 'Patient ID  : ', 'Plan Date  : ', 'Energy  : ']
        keyList = ['Patient Name', 'Patient ID', 'Plan Date', 'Energy']
        
        for x, split in enumerate(splitList):
            strList = fullStr1.split(split)
            strList2 = strList[1].split('\n')
            valuesDict[keyList[x]] = strList2[0]
        
        strList = fullStr1.split('*DTA/Gamma is using ')
        strList2 = strList[1].split(' ')
        valuesDict['DTA Analysis Mode'] = strList2[0]
    valuesDict['pdfList'] = pdfList
    
    # return dictionary
    return valuesDict

def parse1MRL(pathName, pdf, fullStr):
     # takes info from pdf to build pdf name, create empty dictionary for individual pdf
        if 'Absolute Dose Comparison' in fullStr:
            pdfKey = 'AD'
        elif 'Relative Comparison' in fullStr:
            pdfKey = 'RD'
        else:
            print('PDF Error')
        
        pdfValues = {}
        
        # these 3 if statements check for the correct threshold values, and stop the program if they're not there
        thresholdCorrect = True
        try:
            fullStr.index('Difference (%)  : 3.0')
        except:
            thresholdCorrect = False
            return "Percent difference is incorrect. Please manually check documents."
        try:
            fullStr.index('Distance (mm)  : 2.0')
        except:
            thresholdCorrect = False
            return "Comparison distance is incorrect. Please manually check documents."
        try:
            fullStr.index('Threshold (%)  : 10.0')
        except:
            thresholdCorrect = False
            return "Threshold percent is incorrect. Please manually check documents."
        if pdfKey[0] == 'A':
            try:
                fullStr.index('Use Global %  : No')
            except:
                thresholdCorrect = False
                raise Exception("Global % should be set to No.")
        
        # by splitting the string directly before and after the desired value, we get the % pass rate
        strList = fullStr.split('% Passed  : ') 
        strList2 = strList[1].split('\n')
        numOut = float(strList2[0])
        
        pdfValues['% Passed'] = numOut
        pdfValues["Parameters"] = thresholdCorrect
        pdfValues['pathName'] = pathName
        
        splitList = ['SSD  : ', 'SDD  : ', 'Depth  : ', 'Total Points  : ', 'Passed  : ', 'Failed  : ']
        keyList = ['SSD', 'SDD', 'Depth', 'Total Points', 'Passed', 'Failed']
        
        for x, split in enumerate(splitList):
            strList = fullStr.split(split)
            strList2 = strList[1].split('\n')
            pdfValues[keyList[x]] = strList2[0]
            
        return pdfKey, pdfValues
            
def parse2MRL(pathName, pdf, fullStr):
     # takes info from pdf to build pdf name, create empty dictionary for individual pdf
        if 'Absolute Dose Comparison' in fullStr:
            pdfKey = 'AD'
        elif 'Relative Comparison' in fullStr:
            pdfKey = 'RD'
        else:
            print('PDF Error')
        
        pdfValues = {}
        
        # these 3 if statements check for the correct threshold values, and stop the program if they're not there
        thresholdCorrect = True
        try:
            fullStr.index('Difference (%) 3.0')
        except:
            thresholdCorrect = False
            return "Percent difference is incorrect. Please manually check documents."
        try:
            fullStr.index('Distance (mm) 2.0')
        except:
            thresholdCorrect = False
            return "Comparison distance is incorrect. Please manually check documents."
        try:
            fullStr.index('Threshold (%) 10.0')
        except:
            thresholdCorrect = False
            return "Threshold percent is incorrect. Please manually check documents."
        if pdfKey[0] == 'A':
            try:
                fullStr.index('Use Global (%) No')
            except:
                thresholdCorrect = False
                raise Exception("Global % should be set to No.")
        
        # by splitting the string directly before and after the desired value, we get the % pass rate
        strList = fullStr.split('Pass (%) ') 
        strList2 = strList[1].split('\n')
        numOut = float(strList2[0])
        
        pdfValues['% Passed'] = numOut
        pdfValues["Parameters"] = thresholdCorrect
        pdfValues['pathName'] = pathName
        
        splitList = ['Total Points ', 'Pass ', 'Fail ']
        keyList = ['Total Points', 'Passed', 'Failed']
        
        for x, split in enumerate(splitList):
            strList = fullStr.split(split)
            strList2 = strList[1].split('\n')
            pdfValues[keyList[x]] = strList2[0]
            
        strList = fullStr.split('Pass ')
        strList2 = strList[2].split('\n')
        pdfValues['Passed'] = strList2[0]
            
        return pdfKey, pdfValues
    

def getPassRates(MRN, fieldIndex):
    #pdfList = glob.glob('Q:\\IMRTQA\\2019 IMRT VMAT TBI/*' + MRN + '/**/*.pdf', recursive = True)
    pdfList = glob.glob('Q:\\IMRTQA/*' + MRN + '/**/*.pdf', recursive = True) # finds all pdfs in folder(s) with the MRN
    try:
        pdfList[0]
    except IndexError:
        pdfList.extend(glob.glob('Q:\\IMRTQA\\2020 IMRT VMAT TBI/*' + MRN + '/**/*.pdf', recursive = True))
        try:
            pdfList[0]
        except:
            return None
    
    newPDFlist = []
    for pathName in pdfList:
        if str(fieldIndex) in pathName:
            newPDFlist.append(pathName)
    try:
        newPDFlist[0]
    except IndexError:
        pdfList = glob.glob('Q:\\IMRTQA\\2020 IMRT VMAT TBI/*' + MRN + '/**/*.pdf', recursive = True)
        for pathName in pdfList:
            if str(fieldIndex) in pathName:
                newPDFlist.append(pathName)
        try:
            newPDFlist[0]
        except:
            print(MRN, '\t', fieldIndex, ":\tNo PDFs found")
            return None
    
    passrates = {}
    for pathName in newPDFlist: # runs through each pdf in pdfList
        with pdfplumber.open(pathName) as pdf: # uses pdfplumber to extract text from the pdf
            firstPage = pdf.pages[0]
            fullStr = firstPage.extract_text()
        
        if 'ArcCHECK' not in fullStr:
            continue
        
        # takes info from pdf to build pdf name, create empty dictionary for individual pdf
        if 'Absolute Dose Comparison' in fullStr:
            letter = 'A'
        elif 'Relative Comparison' in fullStr:
            letter = 'R'
        else:
            print(pathName)
            print('PDF Error')   
        pdfKey = letter + 'D'
        
        # these 3 if statements check for the correct threshold values, and stop the program if they're not there
        try:
            fullStr.index('Difference (%)  : 3.0')
        except:
            print(MRN, fieldIndex, ": Percent difference is incorrect. Please manually check documents.")
        try:
            fullStr.index('Distance (mm)  : 2.0')
        except:
            print(MRN, fieldIndex, ": Comparison distance is incorrect. Please manually check documents.")
        try:
            fullStr.index('Threshold (%)  : 10.0')
        except:
            print(MRN, fieldIndex, ": Threshold percent is incorrect. Please manually check documents.")
        if pdfKey[0] == 'A':
            try:
                fullStr.index('Use Global %  : No')
            except:
                print(MRN, fieldIndex, ": Global % should be set to No.")
                
        # by splitting the string directly before and after the desired value, we get the % pass rate
        strList = fullStr.split('% Passed  : ') 
        strList2 = strList[1].split('\n')
        numOut = float(strList2[0])
        
        passrates[pdfKey] = numOut
        
    return passrates