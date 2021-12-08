"""
Created on Wed May 12 15:58:11 2021
@author: weersim
"""

def getImages(MRN, fieldIndexes, pdfList):
    import glob, pdfplumber, tempfile
    from decimal import Decimal
    
    if not pdfList:
        pdfList = glob.glob('Q:\\IMRTQA/*' + MRN + '/**/*.pdf', recursive = True) # finds all pdfs in folder(s) with the MRN
        pdfList.extend(glob.glob('Q:\\IMRTQA\\2020 IMRT VMAT TBI/*' + MRN + '/**/*.pdf', recursive = True))
    
        # checks that there are pdfs in the target file, exits if not
        try:
            pdfList[0]
        except IndexError:
            return "There are no PDFs in the patient file you searched."
        removeList = []
        for pathName in pdfList:
            fieldBool = False
            with pdfplumber.open(pathName) as pdf: # uses pdfplumber to extract text from the pdf
                firstPage = pdf.pages[0]
                fullStr = firstPage.extract_text()
            # in order to uniquely find the field index in fullStr, make fullStr shorter
            if '% Passed' in fullStr:
                strList = fullStr.split('% Passed')
                fullStr = strList[1]
            if 'IQM Report Summary:' not in fullStr:
                for item in fieldIndexes:
                    if item in fullStr:# checking that the field index is in the pdf; if it isn't, we don't want to read it
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
        for pathName in removeList:
            pdfList.remove(pathName)
    
    
    
    
    imagesDict = {}
    m = 0
    for pathName in pdfList: # runs through each pdf in pdfList
        with pdfplumber.open(pathName) as pdf: # uses pdfplumber to extract text from the pdf
            # extracting values for use
            firstPage = pdf.pages[0]
            fullStr = firstPage.extract_text()
            pageImages = firstPage.images
            pageHeight = firstPage.height
            # checking the pdf is the correct document
            if 'ArcCHECK' not in fullStr:
                continue
            # takes info from pdf to build pdf name
            if 'Absolute Dose Comparison' in fullStr:
                letter1 = 'A'
            elif 'Relative Comparison' in fullStr:
                letter1 = 'R'
            else:
                print('PDF Error')
            
            try:
                if len(pdf.pages) == 2:
                    strList = fullStr.split('Notes\n')
                    strList2 = strList[1].split('\n')
                    keyPart = strList2[0]
                else:
                    strList = fullStr.split('\n(y,x) cm\n')
                    strList2 = strList[1].split('\n')
                    keyPart = strList2[0]
                    keyPart = keyPart.replace('N', '', 1)
                    removeLetters = [' ', 'o', 't', 'e', 's']
                    for letter in removeLetters:
                        keyPart = keyPart.replace(letter, '')
                
                if keyPart == '' and len(pdfList) == 2:
                    pdfName = letter1 + 'D'
                elif keyPart == '' and len(pdfList) > 2:
                    keyPart = str(m)
                    pdfName = letter1 + 'D-' + keyPart
                else:
                    pdfName = letter1 + 'D-' + keyPart
            except:
                pdfName = letter1 + 'D'
            m = m + 1
            if len(pdf.pages) == 2:
                try:
                    secondPage = pdf.pages[1]
                    image = pageImages[2]
                    imageBox = (image['x0'], pageHeight - image['y1'], image['x1'], pageHeight - image['y0'])
                    pageCrop = secondPage.crop(imageBox)
                    imageObj = pageCrop.to_image(resolution = 200)
                except:
                    print('Image attempt failed')
                    return 'To view images, please install ImageMagick and Ghost Script.'
            else:
                try:
                    # selecting correct image and cropping page to get image object
                    image = pageImages[2]
                    imageBox = (image['x0'] + Decimal(100), pageHeight - image['y1'], image['x1'], pageHeight - image['y0'])
                    pageCrop = firstPage.crop(imageBox)
                    imageObj = pageCrop.to_image(resolution = 200)
                except:
                    print('Image attempt failed')
                    return 'To view images, please install ImageMagick and Ghost Script.'
            # creating image path name
            tempPath = tempfile.gettempdir() + '\\' + pdfName + '.jpg'
            # saving to temp folder - probably take out or change path
            imageObj.save(tempPath)
            # adding image pathname to dictionary for pdf
            imagesDict[pdfName] = tempPath
           
    if not bool(imagesDict):
        raise UnboundLocalError
    
    return imagesDict


def deltaImage(pathName):
    import pdfplumber
    
    with pdfplumber.open(pathName) as pdf:
       # extracting values for use
       firstPage = pdf.pages[0]  
    try:
        imageObj = firstPage.to_image(resolution = 300)
    except:
        print('Attempt failed')
        return 'To view images, please install ImageMagick and Ghost Script.'
    
    imageObj.save(r'Q:\\VMAT QA Project\\Madrigals Code\\Images\\Delta4.jpg')    
    return 'Q:\\VMAT QA Project\\Madrigals Code\\Images\\Delta4.jpg'