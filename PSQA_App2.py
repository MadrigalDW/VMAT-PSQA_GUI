"""
Created on Fri Jul 30 12:20:32 2021
@author: weersim
"""
import clr, os, webbrowser, glob, subprocess, pyperclip
clr.AddReference("wpf\PresentationFramework")
from System.IO import StreamReader
from System import ComponentModel, Uri
from System.Windows import Window, LogicalTreeHelper, RoutedEventHandler, MessageBox
from System.Windows.Markup import XamlReader
from System.Windows.Media.Imaging import BitmapImage, BitmapCacheOption
from System.Windows.Media import Brushes
from System.Windows.Input import Key
from System.Threading import ApartmentState, Thread, ThreadStart

from GAC import getArcCheck, getArcCheck2
from GI import getImages, deltaImage
from query_MosaiQ import query_mosaiq
from mira_rest.mosaiq_qa import get_field_info, get_site_info


class TestWindow(Window): 
    def __init__(self):
        ### import XAML code from external file
        stream = StreamReader('gui_2.xaml') # expects a path name! 
        self.testwindow = XamlReader.Load(stream.BaseStream)
        
        # ImageMagick warning
        imfolder = glob.glob('C:/Program Files/ImageMagick*', recursive = True)
        if imfolder:
            print('ImageMagick is installed!')
        else:
            MessageBox.Show('To view images, please install ImageMagick and Ghost Script.') # if image magick and ghost script aren't installed, displays a message warning user they need both to view images
        
        # initializing buttons and boxes
        self.MRNinputboxinXAML = LogicalTreeHelper.FindLogicalNode(self.testwindow, "MRNinput")
        self.dateInputboxinXAML = LogicalTreeHelper.FindLogicalNode(self.testwindow, "dateInput")
        self.MRNinputboxinXAML.KeyDown +=  RoutedEventHandler(self.MRN_entered)
        self.dateInputboxinXAML.KeyDown +=  RoutedEventHandler(self.MRN_entered)
        
        self.getExcelbuttoninXAML = LogicalTreeHelper.FindLogicalNode(self.testwindow, "getExcel")
        self.getExcelbuttoninXAML.Click +=  RoutedEventHandler(self.getExcelClick)
        
        openVMATbuttoninXAML = LogicalTreeHelper.FindLogicalNode(self.testwindow, "openVMAT")
        openVMATbuttoninXAML.Click +=  RoutedEventHandler(self.openVMATClick)
        
        self.openPDFbuttoninXAML = LogicalTreeHelper.FindLogicalNode(self.testwindow, "openPDF")
        self.openPDFbuttoninXAML.Click +=  RoutedEventHandler(self.openPDFClick)
        
        infobuttoninXAML = LogicalTreeHelper.FindLogicalNode(self.testwindow, "infoButton")
        infobuttoninXAML.Click +=  RoutedEventHandler(self.infoClick)
        
        resetbuttoninXAML = LogicalTreeHelper.FindLogicalNode(self.testwindow, "reset")
        resetbuttoninXAML.Click +=  RoutedEventHandler(self.resetClick)
        
        self.PDFinputboxinXAML = LogicalTreeHelper.FindLogicalNode(self.testwindow, "PDFinput")
        self.teamBoxinXAML = LogicalTreeHelper.FindLogicalNode(self.testwindow, "teamBox")
        self.teamBoxinXAML.SelectionChanged +=  RoutedEventHandler(self.teamEntered)
        
        self.criteriaBoxinXAML = LogicalTreeHelper.FindLogicalNode(self.testwindow, "criteriaBox")
        self.siteBoxinXAML = LogicalTreeHelper.FindLogicalNode(self.testwindow, "siteBox")
        self.siteBoxinXAML.SelectionChanged +=  RoutedEventHandler(self.siteEntered)
        
        ButtoninXAML = LogicalTreeHelper.FindLogicalNode(self.testwindow, "button1") 
        ButtoninXAML.Click +=  RoutedEventHandler(self.button_Click)
        self.testwindow.Closing += ComponentModel.CancelEventHandler(self.MyWindow_Closing) 

    def teamEntered(self, sender, e):
        # based on the team selected, activates/deactivates the necessary buttons/boxes
        # also adds combo box options when combo box is activated
        print(self.teamBoxinXAML.SelectedItem)
        self.siteBoxinXAML.IsEnabled = True
        self.siteBoxinXAML.Items.Clear()
        self.criteriaBoxinXAML.Items.Clear()
        self.criteriaBoxinXAML.IsEnabled = False
        if self.teamBoxinXAML.SelectedItem.ToString() == 'System.Windows.Controls.ComboBoxItem: Team 1':
            itemList = ['Complex Palliative', 'Oligomets', 'T1 - H&N - Nasopharynx', 'T1 - H&N - Bilateral Necks   ', 'T1 - H&N - Unilateral', 'T1- H&N - Early Glottis', 'T1 - H&N - Oral/Nasal Cavity', 'T1 - H&N - Other ', 'T1 - Skin - H&N or Scalp', 'T1 - Skin - Axilla or Groin', 'T1 - Endocrine - Pituitary', 'T1- Endocrine - Thyroid', 'T1 - Eye', 'T1 - Eye - Choroidal Melanoma']
            for item in itemList:
                self.siteBoxinXAML.Items.Add(item)
            
        elif self.teamBoxinXAML.SelectedItem.ToString() == 'System.Windows.Controls.ComboBoxItem: Team 2':
            itemList = ['Complex Palliative', 'Oligomets', 'T2 - Liver', 'T2 - Pancreas', 'T2 - Esophagus', 'T2 - Stomach', 'T2 - Celiac Plexus', 'T2 - Lung', 'T2 - Lung SBRT', 'T2 - Thymoma', 'T2 - Cardiac SBRT ', 'T2 - Other']
            for item in itemList:
                self.siteBoxinXAML.Items.Add(item)
            
        elif self.teamBoxinXAML.SelectedItem.ToString() == 'System.Windows.Controls.ComboBoxItem: Team 3':
             itemList = ['Complex Palliative', 'Oligomets', 'T3 - Prostate', 'T3 - Prostate + Nodes - Phase 1', 'T3 - Prostate + Nodes - Phase 2', 'T3 - Prostate Bed', 'T3 - Prostate Bed + Nodes - Phase 1', 'T3 - Prostate Bed + Nodes - Phase 2', 'T3 - Bladder - Phase 1 (and Palliative)', 'T3 - Bladder - Phase 2', 'T3 - Bladder - Phase 3', 'T3 - Bladder + Nodes - Phase 1', 'T3 - Bladder + Nodes - Phase 2', 'T3 - Kidney', 'T3 - Seminoma', 'T3 - Anal Canal - Single Phase (with SIB)', 'T3 - Anal Canal - Phase 1', 'T3 - Anal Canal - Phase 2', 'T3 - Anal Canal - Phase 3', 'T3 - Rectum', 'T3 - Post-Op Endometrium/Cervix', 'T3 - Intact-Cervix (and Intact-Uterus)', 'T3 - Vulva - Phase 1 (and Single Phase)', 'T3 - Vulva - Phase 2', 'T3 - Gyne Sequential Nodal Boost', 'T3 - Other']  
             for item in itemList:
                 self.siteBoxinXAML.Items.Add(item)
            
        elif self.teamBoxinXAML.SelectedItem.ToString() == 'System.Windows.Controls.ComboBoxItem: Team 4':
             itemList = ['Complex Palliative', 'Oligomets', 'T4 - CNS Brain', 'T4 - CNS Other', 'T4 - CSI', 'T4 - Spine SBRT', 'T4 - Sarcoma - Upper Limb ', 'T4 - Sarcoma - RetroSarcoma/Abdomen/Pelvis', 'T4 - Sarcoma - Lower Limb/Groin', 'T4 - Sarcoma - Chestwall', 'T4 - Sarcoma - Dupuytrens (Hand)', 'T4 - Sarcoma - Morbus Ledderhose (Foot)', 'T4 - Lymphoma - Head&Neck', 'T4 - Lymphoma - ModMantle', 'T4 - Lymphoma - Pelvis', 'T4 - Lymphoma - Abdomen', 'T4 - Paeds', 'T4 - Other']
             for item in itemList:
                 self.siteBoxinXAML.Items.Add(item)
                 
        elif self.teamBoxinXAML.SelectedItem.ToString() == 'System.Windows.Controls.ComboBoxItem: Team MRL': 
             self.siteBoxinXAML.IsEnabled = False
             self.MRNinputboxinXAML.IsEnabled = True
             self.dateInputboxinXAML.IsEnabled = True
             self.criteriaBoxinXAML.IsEnabled = True
             self.criteriaBoxinXAML.Items.Add('Prostate, Bladder, Pelvic Oligomets')
             self.criteriaBoxinXAML.Items.Add('Liver, Pancreas, Kidney')
    
    def siteEntered(self, sender, e):
        self.MRNinputboxinXAML.IsEnabled = True
        self.dateInputboxinXAML.IsEnabled = True
        self.criteriaBoxinXAML.Items.Clear()
        if self.teamBoxinXAML.SelectedItem.ToString() == 'System.Windows.Controls.ComboBoxItem: Team 2' or self.teamBoxinXAML.SelectedItem.ToString() == 'System.Windows.Controls.ComboBoxItem: Team 3' or self.teamBoxinXAML.SelectedItem.ToString() == 'System.Windows.Controls.ComboBoxItem: Team MRL':
            self.criteriaBoxinXAML.IsEnabled = True
        else:
            self.criteriaBoxinXAML.IsEnabled = False
        if self.siteBoxinXAML.SelectedItem == 'Complex Palliative':
            self.criteriaBoxinXAML.Items.Add('Complex Palliative')
            self.criteriaBoxinXAML.Text = 'Complex Palliative'
            
        elif self.siteBoxinXAML.SelectedItem == 'Oligomets':
            self.criteriaBoxinXAML.Items.Add('Oligomets')
            self.criteriaBoxinXAML.Text = 'Oligomets'
        else:
            if self.teamBoxinXAML.SelectedItem.ToString() == 'System.Windows.Controls.ComboBoxItem: Team 2':
                criteriaList = ['Lung SBRT, Other', 'Stomach, Pancreas, Esophagus, Liver, Locally Advanced Lung']
                for item in criteriaList:
                    self.criteriaBoxinXAML.Items.Add(item)
                    
            elif self.teamBoxinXAML.SelectedItem.ToString() == 'System.Windows.Controls.ComboBoxItem: Team 3':
                criteriaList = ['Without elective nodes', 'With electives nodes or h-f Bladder, Kidney SBRT']
                for item in criteriaList:
                    self.criteriaBoxinXAML.Items.Add(item)
        
    
    def MRN_entered(self,sender,e):
        if e.Key == Key.Return:
            MRN = self.MRNinputboxinXAML.Text
            date = self.dateInputboxinXAML.Text
            if MRN == '' or MRN == ' ':
                MessageBox.Show('Please enter an MRN')
            elif date == '' or date == ' ':
                MessageBox.Show('Please enter a date')
            else:
                # calling reset to clear by default
                self.resetAuto(sender, e)
                # running the function to get the display
                print('The MRN is ', MRN, '\nThe date is ', date, '\n')
                self.getPDFImagesClick(sender, e, MRN, date)
                # activating other buttons
                self.getExcelbuttoninXAML.IsEnabled = True
                self.openPDFbuttoninXAML.IsEnabled = True
                self.PDFinputboxinXAML.IsEnabled = True
    
    
    def getPDFImagesClick(self, sender, e, MRN, inputDate):
        # add specific exceptions if input is invalid or there's an error creating the output array
        try:
            int(MRN)
        except:
            print('Not int')
            MessageBox.Show("Please enter a valid MRN.")
            return None
        try:
            if self.teamBoxinXAML.Text == 'Team MRL':
                m = BuildList2(MRN, inputDate)
                print('Team MRL')
            else:
                m = BuildList(MRN, inputDate, self.siteBoxinXAML.Text)
            self.mDictionary = m.dictionary
            if type(m.dictionary) == str:
               MessageBox.Show(m.dictionary) 
               return None    
        except:
            MessageBox.Show("Sorry, there was an error retrieving the PDF values.")
            return None
        # if case is IQM, displays IQM message in message box
        if 'IQM' in m.dictionary:
            MessageBox.Show(m.dictionary['IQM'])
            return None
        # tries creating image dict, outputs error message if unsuccessful
        try:
            self.QAfields = m.QAfields
            fieldIndexes = m.fieldIndexes
            if 'pdfList' in m.dictionary:
                im = Images(MRN, fieldIndexes, m.pdfList)
            else:
                im = Images(MRN, fieldIndexes, [])
            
            if type(im.imageDict) != str:
                images = im.images
                self.imageList = images
        except:
            MessageBox.Show("An error occured creating the images.")
            return None
        
        # displays patient name from GAC dictionary
        self.NameboxinXAML = LogicalTreeHelper.FindLogicalNode(self.testwindow, 'PatientName')
        self.NameboxinXAML.Text = 'Patient Name: ' + m.dictionary['Patient Name']
        # variable initialization
        self.imNameList = ['Testimage', 'Image2', 'Image3', 'Image4', 'Image5', 'Image6', 'Image7', 'Image8', 'Image9', 'Image10', 'Image11', 'Image12', 'Image13', 'Image14', 'Image15', 'Image16', 'Image17', 'Image18', 'Image19', 'Image20']
        self.resultList = ['ResultDisplay', 'ResultDisplay2', 'ResultDisplay3', 'ResultDisplay4', 'ResultDisplay5', 'ResultDisplay6', 'ResultDisplay7', 'ResultDisplay8', 'ResultDisplay9', 'ResultDisplay10', 'ResultDisplay11', 'ResultDisplay12', 'ResultDisplay13', 'ResultDisplay14', 'ResultDisplay15', 'ResultDisplay16', 'ResultDisplay17', 'ResultDisplay18', 'ResultDisplay19', 'ResultDisplay20']
        
        # displays each passrate with the minimum passrate for each image
        # font is red or green based on whether passrate is adequate (passFailFont)
        for i, passrate in enumerate(m.passrateList):
            j = int(i/2)
            if (i % 2) == 0:
                relativity = 0
                passFail = self.passFailFont(sender, e, m.passrateList[i], relativity, MRN, self.QAfields[j])
                ResultsboxinXAML = LogicalTreeHelper.FindLogicalNode(self.testwindow, self.resultList[i])
                ResultsboxinXAML.Text = m.keyList[i] + ' Passrate: '+str(passrate)+ '%   (Minimum: ' + str(self.minPass) + ')'
                
                if passFail:
                    ResultsboxinXAML.Foreground = Brushes.Green
                else:
                    ResultsboxinXAML.Foreground = Brushes.Red
            else:
                relativity = 1
                passFail = self.passFailFont(sender, e, m.passrateList[i], relativity, MRN, self.QAfields[j])
                ResultsboxinXAML = LogicalTreeHelper.FindLogicalNode(self.testwindow, self.resultList[i])
                ResultsboxinXAML.Text = m.keyList[i] + ' Passrate: '+str(passrate)+'%    (Minimum: ' + str(self.minPass) + ')'
                
                if passFail:
                    ResultsboxinXAML.Foreground = Brushes.Green
                else:
                    ResultsboxinXAML.Foreground = Brushes.Red
            i = i + 1
        
        try:
            if type(im.imageDict) != str:
                for i, image in enumerate(images):
                    # displays images, running through each "spot" in the grid using imNameList and resultList
                    # uses bitmap cache to avoid issues with overwriting images
                    bitmap = BitmapImage()
                    bitmap.BeginInit()
                    bitmap.UriSource = Uri(image)
                    bitmap.CacheOption = BitmapCacheOption.OnLoad
                    bitmap.EndInit()
                    ImageinXAML = LogicalTreeHelper.FindLogicalNode(self.testwindow, self.imNameList[i])
                    ImageinXAML.Source = bitmap
                    # delete the bitmap object to clear cache and prevent previous images being displayed
                    bitmap = None
            elif im.imageDict != 'To view images, please install ImageMagick and Ghost Script.':
                MessageBox.Show(im.imageDict)
        except IndexError:
            MessageBox.Show('The number of PDFs exceeds the application limit.') # Limit of 10 rows, based on xaml file
        
        # builds header array using Measurements data array   
        displayArray = m.dataArray
        self.dataArray = displayArray
        if self.teamBoxinXAML.Text != 'Team MRL':
            displayOut = 'MRN \t\tQA Unit \t\tMeasurement Date \tLinac Type \tBeam Set Index \tBeam Energy \tDose/Fraction \tArc 1 MU \tArc 2 MU \tArc 3 MU \tArc 4 MU\n'
            i = 0            
            for item in displayArray:
                if i < 13:
                    if i == 6:
                        pass
                    elif i == 3:
                        displayOut = displayOut + '\t'
                    else:
                        if len(str(item)) < 8:
                            displayOut = displayOut + str(item) + '\t\t'
                        else:
                            displayOut = displayOut + str(item) + '\t'
                    i = i + 1
                if item == '\n' or '\n' in str(item):
                    displayOut = displayOut + str(item)
                    i = 0 
            displayOut = displayOut + '\n-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------'
        else:
            displayOut = 'MRN \t\tUnit \t\tArcCheck Date \tPlan Name \tDose/Fraction \t# of Beams \tTotal Plan MU \t[absolute] \t[relative] \t3D or 2D Analysis?\n'
            for item in displayArray:
                if item == '' or item == ' ':
                    pass
                elif len(str(item)) < 7 or str(item) == 'Agility':
                    displayOut = displayOut + str(item) + '\t\t'
                else:
                    displayOut = displayOut + str(item) + '\t'
                    i = i + 1
            displayOut = displayOut + '\n--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------'
        
        self.ExcelboxinXAML = LogicalTreeHelper.FindLogicalNode(self.testwindow, 'excelInfo')
        self.ExcelboxinXAML.Text = displayOut
        
        # if case is Delta4, displays Delta4 pdf above AC images and displays a message box 
        self.deltaList = ['Delta4Im1', 'Delta4Im2', 'Delta4Im3']
        i = 0
        message = False
        for key in m.dictionary:
            if 'Delta4' in key:
                if type(im.imageDict) != str:
                    imageName = deltaImage(m.dictionary[key]['pathName'])
                    bitmap = BitmapImage()
                    bitmap.BeginInit()
                    bitmap.UriSource = Uri(imageName)
                    bitmap.CacheOption = BitmapCacheOption.OnLoad
                    bitmap.EndInit()
                    ImageinXAML = LogicalTreeHelper.FindLogicalNode(self.testwindow, self.deltaList[i])
                    ImageinXAML.Source = bitmap
                    bitmap = None
                    i = i + 1
                message = True
        
        if message:
            MessageBox.Show('Most recent file is Delta4. Please click "Open PDFs" to manually check documents.')
        # displays extra warning when necessary
        if 'warning' in self.QAfields:
            MessageBox.Show(self.QAfields['warning'])
        if self.teamBoxinXAML.Text == 'Team 2' or self.teamBoxinXAML.Text == 'Team 3' or self.teamBoxinXAML.Text == 'Team MRL':
            if self.criteriaBoxinXAML.Text == '':
                MessageBox.Show('QA criteria has not been selected. Minimum passrates may not be accurate.')
            
    def passFailFont(self, sender, e, passrate, relativity, MRN, QAfield):
        fieldInfo = get_field_info(MRN, QAfield['fieldId'])
        ifPass = True
        self.minPass = 0.0
        x = self.teamBoxinXAML.Text
        y = self.criteriaBoxinXAML.Text
        
        # initializing pass thresholds based on team criteria
        if x == 'Team 1':
            if relativity == 0:
                if fieldInfo['machineType'] == 'Agility':
                    self.minPass = 75.0
                else:     
                    self.minPass = 83.0
            else:
                if fieldInfo['machineType'] == 'Agility':
                    self.minPass = 90.0
                else:     
                    self.minPass = 95.0       
        elif x == 'Team 2':
            if relativity == 1:
                if y == 'Complex Palliative':
                    self.minPass = 90.0
                else:
                    self.minPass = 95.0
            else:
                if y == 'Lung SBRT, Other' or y == 'Oligomets':
                    self.minPass = 76.0
                elif y == 'Complex Palliative':
                    self.minPass = 75.0
                else:
                    self.minPass = 80.0
        elif x == 'Team 3':
            if relativity == 1:
                if y == 'Complex Palliative':
                    self.minPass = 90.0
                else:
                    self.minPass = 95.0
            else:
                if y == 'With electives nodes or h-f Bladder, Kidney SBRT':
                    self.minPass = 83.0
                elif y == 'Complex Palliative':
                    self.minPass = 75.0
                elif y == 'Oligomets':
                    self.minPass = 76.0
                else:
                    self.minPass = 88.0
        elif x == 'Team 4':
            if relativity == 0:
                if fieldInfo['machineType'] == 'Agility' or fieldInfo['isFff']:
                    self.minPass = 75.0
                else:
                    self.minPass = 85.0
            else:
                if fieldInfo['machineType'] == 'Agility' or fieldInfo['isFff']:
                    self.minPass = 90.0
                else:
                    self.minPass = 95.0
        elif x == 'Team MRL':
            if relativity == 1:
                self.minPass = 95.0
            else:
                if y == 'Prostate, Bladder, Pelvic Oligomets':
                    self.minPass = 88.0
                elif y == 'Liver, Pancreas, Kidney':
                    self.minPass = 80.0
        # checks if passrate is larger than chosen threshold        
        if passrate < self.minPass:
            ifPass = False
        # returns pass boolean
        return ifPass

    
    def getExcelClick(self, sender, e):
        MRN = self.MRNinputboxinXAML.Text
        if MRN == '':
            MessageBox.Show("Please enter an MRN.")
            return None
        
        # add specific exceptions for if input is invalid or there's an error creating the output array
        try:
            int(MRN)
        except:
            MessageBox.Show("Please enter a valid MRN.")
            return None
        
        try:
            dataArray = self.dataArray
            dictionary = self.mDictionary
        except:
            try:
                if self.teamBoxinXAML.Text == 'Team MRL':
                    m = BuildList2(MRN, '')
                else:
                    m = BuildList(MRN, self.siteBoxinXAML.Text)
                if type(m.dictionary) == str:
                   MessageBox.Show(m.dictionary) 
                   return None
            except:
                MessageBox.Show("Sorry, there was an error retrieving the PDF values.")
                return None
            
            # builds output string by adding each item in data array to string with tab
            dataArray = m.dataArray
            dictionary = m.dictionary
        
        out = ''
        i = 0
        if self.teamBoxinXAML.Text == 'Team MRL':
            for data in dataArray:
                if data != '\n' and data != '\t':
                    i = i + 1
                    out = out + str(data) + '\t'
                else:
                    out = out + str(data)
                    i = 0
        else:
            for data in dataArray:
                if data != '\n' and data != '\t':
                    i = i + 1
                    out = out + str(data) + '\t'
                    if i == 3 or i == 5:
                        out = out + '\t'
                else:
                    out = out + str(data)
                    i = 0
        print(out)
        pyperclip.copy(out)
        # displays messagebox showing values are copied to clipboard
        if 'Delta4' in dictionary:
            MessageBox.Show('The values have been copied to your clipboard.\n\nMost recent file is Delta4. Please click "Open PDFs" to manually check documents.')
                
        
    def openVMATClick(self, sender, e):
        # opens link to VMAT document in Microsoft Edge/a browser
        webbrowser.open('https://universityhealthnetwork.sharepoint.com/sites/RMP/Delivery/Forms/AllItems.aspx?id=%2Fsites%2FRMP%2FDelivery%2FVMAT%20Measurement%20QA%20Review%20Procedure%2Epdf&parent=%2Fsites%2FRMP%2FDelivery')


    def openPDFClick(self, sender, e):
        pdfName = self.PDFinputboxinXAML.Text
        MRN = self.MRNinputboxinXAML.Text
        if MRN == '':
            MessageBox.Show("Please enter an MRN.")
            return None
        # add exception for if input isn't an int
        try:
            int(MRN)
        except:
            MessageBox.Show("Please enter a valid MRN.")
            return None
        # get pathnames w MRN and check list exists
        pdfList = glob.glob('Q:\\IMRTQA/*' + MRN + '/**/*.pdf', recursive = True)
        try:
            pdfList[0]
        except IndexError:
            MessageBox.Show("There are no PDFs in the patient file you searched.")
            return None
        # if an IQM case, opens folder automatically
        for pdf in pdfList:
            if 'IQM' in pdf:
                path = pdf.split(MRN)
                path = '"' + path[0] + MRN + '"'
                subprocess.Popen('explorer ' + path)
                return None
            
        if pdfName == 'All' or pdfName == 'ALL' or pdfName == 'all':
            # user wants to open all, runs through each pathname and opens each
            for pdf in pdfList:
                try:
                    webbrowser.open_new(pdf)
                except:
                    pass
        elif pdfName == '':
            # user leaves box blank, opens folder
            pdf1 = pdfList[0]
            path = pdf1.split(MRN)
            path = '"' + path[0] + MRN + '"'
            subprocess.Popen('explorer ' + path)
        else:
            try:
                # opens both PDFs under beam set and arc number
                i = 0
                for pdf in pdfList:
                    if pdfName in pdf[-7:-3]:
                        # if the input matches the beamset in the pathname, it opens the file
                        webbrowser.open_new(pdf)
                        i = i + 1
                if i == 0:
                    MessageBox.Show("Sorry, the name you entered was invalid.")
            except:
                MessageBox.Show("Sorry, the name you entered was invalid.")
        

    def infoClick(self, sender, e):
        # displays info string in a message box
        string = 'Team Selection\nTo use the PSQA GUI, start by selecting your team. This will activate other options depending on your team. For teams 1 to 4, select the treatment site. For teams 2, 3, and MRL, select the QA criteria. For team MRL, you will have the option to type the plan name or a unique part of the plan name (eg. â€œProBadT02â€ or â€œT02â€) in the textbox to the right of the dropdown menus. If you donâ€™t type in the plan name, the GUI will default to choosing the most recent plan in the patient folder.\nFinally, type in the MRN and hit Enter to view the ArcCheck images.\n\nGet Excel Values\nClicking this button will copy the Excel sheet values to your clipboard.\n\nOpen VMAT Doc\nThis button opens the VMAT document in a web browser.\n\nOpen PDFs\nThis button opens the ArcCheck PDFs for the given patient MRN. To open the folder to the PDFs, leave the textbox blank. To open all of the PDFs, type "All". To open PDFs of a specific beam set and arc number, type the corresponding name in the textbox, eg. "A1" or "C2".\n\nClear\nClick the Clear button in between entering new MRNs to clear display items and dropdown selections.'
        MessageBox.Show(string, "Information")


    def resetClick(self, sender, e):
        pyperclip.copy('')
        MRN = self.MRNinputboxinXAML.Text
        if MRN != '':
            try:
                images = self.imageList
                try:
                    i = 0
                    for image in images:
                        # deletes each image from drive and removes them from display
                        ImageinXAML = LogicalTreeHelper.FindLogicalNode(self.testwindow, self.imNameList[i])
                        ImageinXAML.Source = None
                        
                        i = i + 1
                        os.remove(image) 
                    for delta in self.deltaList:
                        ImageinXAML = LogicalTreeHelper.FindLogicalNode(self.testwindow, delta)
                        ImageinXAML.Source = None
                except:
                    print('Images could not be deleted.\t', i)
            except:
                pass
            try:
                self.resultList[0]
                try:
                    for result in self.resultList:
                        ResultsboxinXAML = LogicalTreeHelper.FindLogicalNode(self.testwindow, result)
                        ResultsboxinXAML.Text = None
                    
                    self.ExcelboxinXAML.Text = None
                    self.NameboxinXAML.Text = None
                except:
                    print('Results could not be cleared')
            except:
                pass     
        try:
            # blanks out buttons/boxes
            self.MRNinputboxinXAML.Text = None
            self.dateInputboxinXAML.Text = None
            self.criteriaBoxinXAML.Text = None
            self.siteBoxinXAML.Text = None
            self.PDFinputboxinXAML.Text = None
        except:
            print('MRN not deleted')
        self.getExcelbuttoninXAML.IsEnabled = False
        self.openPDFbuttoninXAML.IsEnabled = False
        self.PDFinputboxinXAML.IsEnabled = False
        
    def resetAuto(self, sender, e):
        pyperclip.copy('')
        MRN = self.MRNinputboxinXAML.Text
        if MRN != '':
            try:
                images = self.imageList
                try:
                    i = 0
                    for image in images:
                        # deletes each image from drive and removes them from display
                        ImageinXAML = LogicalTreeHelper.FindLogicalNode(self.testwindow, self.imNameList[i])
                        ImageinXAML.Source = None
                        
                        i = i + 1
                        os.remove(image) 
                    for delta in self.deltaList:
                        ImageinXAML = LogicalTreeHelper.FindLogicalNode(self.testwindow, delta)
                        ImageinXAML.Source = None
                except:
                    print('Images could not be deleted.')
            except:
                pass
            try:
                self.resultList[0]
                try:
                    for result in self.resultList:
                        ResultsboxinXAML = LogicalTreeHelper.FindLogicalNode(self.testwindow, result)
                        ResultsboxinXAML.Text = None
                    
                    self.ExcelboxinXAML.Text = None
                    self.NameboxinXAML.Text = None
                    self.PDFinputboxinXAML.Text = None
                    self.MRLinputboxinXAML.Text = None
                except:
                    print('Results could not be cleared')
            except:
                pass 
        
         
               
    def button_Click(self, sender, e):
        self.testwindow.Close() # closes window when Exit button is clicked
        
    def MyWindow_Closing(self, sender, e):
        # deletes images as window is closing, regardless of closing method
        try:
            MRN = self.MRNinputboxinXAML.Text
        except:
            MRN = ''
        if MRN != '':
            try:
                images = self.imageList
                try:
                    images[0]
                except:
                    print('No images')
                    self.testwindow.DialogResult = False 
                    return None
                for image in images:
                    os.remove(image)
                print('Images deleted')
            except:
                print('Images could not be deleted.')
        else:
            print('No MRN')
        self.testwindow.DialogResult = False
        
        

    
class BuildList:
    def __init__(self, MRN, date, site):
        # get QAfields, field indexes, and dictionary from separate modules
        self.QAfields = query_mosaiq(MRN, date)
        self.fieldIndexes = []
        for QAfield in self.QAfields:
            self.fieldIndexes.append(QAfield['fieldLabel'])
        print(self.fieldIndexes)
        self.dictionary = getArcCheck(MRN, self.fieldIndexes, date)
        
        # check if case is IQM; if it is, make the dictionary the IQM string and exit
        if 'IQM' in self.dictionary:
            temp = self.dictionary['IQM']
            self.dictionary = temp
            return None
        
        # if dictionary is string, there is an exceptional case to be handled further in above functions
        # program skips array creation
        if type(self.dictionary) == str:
            pass
        else:
            # creating output array
            self.dataArray = [self.dictionary['Patient ID'], 0, self.dictionary['Plan Date'], 0, 0, 0, str(site), ' MV', 0, 0, 0, 0, 0]
            self.passrateList = []
            self.keyList = [] 
            self.qaDictList = []
             
            # sort list of dictionaries by field indexes
            self.qaDictList = sorted(self.QAfields, key = lambda i: i['fieldLabel'])
            i = 0                   # used for correct indexing of field label & beam meter set
            fieldLabelIndex = 5     # used to track when a new row is needed
            
            for QAfield in self.qaDictList: # goes through each QA field in order of field indexes
                # initializes field & site info    
                field_info = get_field_info(MRN, QAfield['fieldId'])
                siteInfo = get_site_info(QAfield['siteSetId'])
                
                # adds QA field data to list if it hasn't already been added 
                if self.dataArray[1] == 0: 
                    self.dataArray[1] = QAfield['machineName']
                    self.dataArray[2] = QAfield['treatmentTime'][0:10]
                    self.dataArray[5] = QAfield['fieldLabel'][0]
                    self.dataArray[8] = siteInfo['treatmentDose']
                    
                    if field_info['machineType'] == 'Ix':
                        self.dataArray[4] = 'Truebeam'
                    else:
                        self.dataArray[4] = field_info['machineType']
                    if field_info['isFff']:
                        self.dataArray[7] = str(field_info['beamEnergy']) + ' MV FFF'
                    else:
                        self.dataArray[7] = str(field_info['beamEnergy']) + ' MV'
                
                
                if self.dataArray[fieldLabelIndex ] != QAfield['fieldLabel'][0]: # if the field letter of the QA field being run doesn't match the letter for the current row, add a new row
                    i = 0
                    # adding new row to list
                    if field_info['isFff']:
                        self.dataArray.extend(('\n', self.dictionary['Patient ID'], QAfield['machineName'], QAfield['treatmentTime'][0:10], 0, 0, QAfield['fieldLabel'][0], str(site), str(field_info['beamEnergy']) + ' MV FFF', siteInfo['treatmentDose'], 0, 0, 0, 0))
                    else:
                        self.dataArray.extend(('\n', self.dictionary['Patient ID'], QAfield['machineName'], QAfield['treatmentTime'][0:10], 0, 0, QAfield['fieldLabel'][0], str(site), str(field_info['beamEnergy']) + ' MV', siteInfo['treatmentDose'], 0, 0, 0, 0))
                    
                    # setting object indexes based on the length of the list
                    fieldLabelIndex = len(self.dataArray) - 8
                    beamSetIndex = len(self.dataArray) - 4 - i
                    # adding machine type    
                    if field_info['machineType'] == 'Ix':
                        self.dataArray[fieldLabelIndex-1] = 'Truebeam'
                    else:
                        self.dataArray[fieldLabelIndex-1] = field_info['machineType']
                    # adding beam meter set for each beam
                    if self.dataArray[beamSetIndex] == 0:
                        self.dataArray[beamSetIndex] = field_info['beamMeterset']
                    else:
                        self.dataArray[beamSetIndex + 1] = field_info['beamMeterset']
                else:
                    beamSetIndex = len(self.dataArray) - 4 - i
                    i = i + 1
                    
                    # if the last element of the data list is a list, remove it (this is so Delta4 values won't be repeated)
                    if type(self.dataArray[-1]) == list:
                        self.dataArray.remove(self.dataArray[-1])
                    # adding beam meter set for each beam
                    if self.dataArray[beamSetIndex] == 0:
                        if self.dataArray[beamSetIndex - 1] == 0:
                            self.dataArray[beamSetIndex - 1] = field_info['beamMeterset']
                        else:
                            self.dataArray[beamSetIndex] = field_info['beamMeterset']
                    else:
                        self.dataArray[beamSetIndex + 1] = field_info['beamMeterset']
                    
                keys = ['AD-', 'RD-']
                for key1 in keys: 
                    key = key1 + QAfield['fieldLabel']
                    try:
                        self.dataArray.append(self.dictionary[key]['% Passed']) # adding % passrates to end of data list
                        self.passrateList.append(self.dictionary[key]['% Passed']) # adding % passrates to end of passrate list (used for image display)
                        self.keyList.append(key) # adding keys to key list (used for image display)
                    except:
                        MessageBox.Show('There is a mismatch between PDF beam sets and MosaiQ beam sets. Please manually check PDFs.')
                        raise Exception  # to stop the above message from repeating and keep the display blank
                
                for key in self.dictionary:
                    if 'Delta4' in key: # looks for Delta4 keys in dict
                        if QAfield['fieldLabel'][0] in self.dictionary[key]:                        # matches field letter to correct Delta4 case
                            self.dataArray.append(self.dictionary[key][QAfield['fieldLabel'][0]])   # adds Delta4 results to data list
                            i = i + len(self.dictionary[key][QAfield['fieldLabel'][0]])             # for correct indexing of inserted elements
                
            for index, data in enumerate(self.dataArray):
                if type(data) == list:
                    # adds Delta4 results as individual items, with tabs before depending on number of cases ie. if there is 1 case, there will be 2 passrates and 6 tabs are needed, if there are 2 cases there are 4 passrates and 4 tabs are needed
                    if len(data) == 1:
                        data2 = '\t \t \t \t \t \t '
                    elif len(data) == 2:
                        data2 = '\t \t \t \t '
                    elif len(data) == 3:
                        data2 = '\t \t '
                    else:
                        data2 = ''
                    for element in data:
                        data2 = data2 + element
                    self.dataArray[index] = data2
                if data == 0 or data == '0':
                    self.dataArray[index] = ' ' # replaces zeros in list with blank items

                    
class BuildList2:
    def __init__(self, MRN, date):
        # retrieving QAfields & ACdictionary
        self.QAfields = query_mosaiq(MRN, date)
        self.fieldIndexes = []
        for QAfield in self.QAfields:
            self.fieldIndexes.append(QAfield['fieldLabel'])
        self.dictionary = getArcCheck2(MRN, '', self.fieldIndexes)
        self.pdfList = self.dictionary['pdfList']
        
        if type(self.dictionary) == str: # check if dict is str for exception handling
            pass
        else:
            totalMU = 0.0
            for QAfield in self.QAfields:
                fieldInfo = get_field_info(MRN, QAfield['fieldId'])
                siteInfo = get_site_info(QAfield['siteSetId'])
                totalMU = totalMU + fieldInfo['beamMeterset'] # get total MU by adding MU from each field
                DPF = siteInfo['treatmentDose'] # get dose/fraction. stays same each time
                
            # getting plan name from pathName
            pathName = self.dictionary['AD']['pathName']
            pathList = pathName.split(MRN + '\\')
            pathList2 = pathList[1].split('\\')
            planName = pathList2[0]
            # initialize output array
            self.dataArray = [self.dictionary['Patient ID'], self.QAfields[0]['machineName'], self.dictionary['Plan Date'], 0, 0, planName, 0, DPF, len(self.QAfields), totalMU]
            self.passrateList = []
            self.keyList = ['AD', 'RD']
            # add passrates
            for key in self.keyList:
                if key in self.dictionary:
                    self.dataArray.append(self.dictionary[key]['% Passed'])
                    self.passrateList.append(self.dictionary[key]['% Passed'])
            # add on DTA analysis mode
            self.dataArray.extend((0, 0, self.dictionary['DTA Analysis Mode']))  
            # replace zeros with empty cells
            for i, data in enumerate(self.dataArray):
                if data == 0 or data == '0':
                    self.dataArray[i] = ' '
            

class Images:
    def __init__(self, MRN, fieldIndexes, pdfList):
        # retrieve list of image pathnames created by getImages function
        self.imageDict = getImages(MRN, fieldIndexes, pdfList)
        
        if type(self.imageDict) == str:
            print(self.imageDict)
            pass
        else:
            # sort alphanumerically with lambda fn?
            self.images = []
            letterArray1 = ['A', 'R']
            letterArray2 = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
            numArray = ['1', '2', '3', '4']
            
            for letter2 in letterArray2:
                for num in numArray:
                    for letter1 in letterArray1:
                        key = letter1 + 'D-' + letter2 + num
                        if key in self.imageDict:
                            self.images.append(self.imageDict[key])       
            try:
                self.images[0]
            except:
                # if case is MRL, add based on AD/RD only
                try:
                    keyList = ['AD', 'RD']
                    for key in keyList:
                        self.images.append(self.imageDict[key])
                except:
                    for key in self.imageDict:
                        self.images.append(self.imageDict[key])
    

def app_thread():
    #thr = Thread.CurrentThread
    dialog = TestWindow().testwindow # how can we access dialog inside the TestWindow class or the event handler?
    dialog.ShowDialog()

if __name__== '__main__':
    thread = Thread(ThreadStart(app_thread))
    thread.SetApartmentState(ApartmentState.STA)
    thread.Start()
    thread.Join()