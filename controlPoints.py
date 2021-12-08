# -*- coding: utf-8 -*-
"""
Created on Thu Jun 17 14:31:51 2021
@author: weersim
"""
from mira_rest.mosaiq_qa import get_qa_records, get_field_info, get_site_info
from GAC import getPassRates
import matplotlib.pyplot as plt
import time, math

def mqControlPoints(MRN, fieldIndexes):
    QAfields = get_qa_records(MRN)
    selectedFields = []
    
    for QAfield in QAfields:
        if QAfield['fieldLabel'] in fieldIndexes:
            selectedFields.append(QAfield)
    
    speedListList = [[5.80954792449, 5.80954792449, 5.80954792449, 5.80954792449, 5.80954792449, 5.80954792449, 5.80954792449, 5.80954792449, 5.80954792449, 5.80954792449, 5.80954792449, 5.80954792449, 5.80954792449, 5.80954792449, 5.80954792449, 5.80954792449, 5.80954792449, 5.80954792449, 5.80954792449, 5.80954792449, 5.80954792449, 5.80954792449, 5.80954792449, 5.80954792449, 5.80954792449, 5.80954792449, 5.80954792449, 5.80954792449, 5.80954792449, 5.80954792449,5.80954792449, 5.80954792449, 5.80954792449, 5.80954792449, 5.80954792449, 5.80954792449, 5.80954792449, 5.80954792449, 5.80954792449, 5.80954792449, 5.80954792449, 5.80954792449, 5.80954792449, 5.80954792449, 5.80954792449, 5.80954792449, 4.35716094337, 5.80954792449, 5.80954792449, 5.80954792449, 5.80954792449, 5.80954792449, 5.80954792449, 5.80954792449, 5.80954792449, 5.80954792449, 5.80954792449, 5.80954792449, 5.80954792449, 5.80954792449, 5.80954792449, 5.80954792449, 5.80954792449, 5.80954792449, 5.80954792449, 5.80954792449, 5.80954792449, 5.80954792449, 5.80954792449, 5.80954792449, 5.80954792449, 5.80954792449, 5.80954792449, 5.80954792449, 5.80954792449, 5.80954792449, 5.80954792449, 5.80954792449, 5.80954792449, 5.80954792449, 5.80954792449, 5.80954792449, 5.80954792449, 5.80954792449, 5.61413738718, 5.17339558743, 5.80954792449, 5.80954792449, 5.80954792449, 5.80954792449, 5.80954792449, 5.80954792449, 5.80954792449, 5.80954792449, 5.80954792449, 5.80954792449, 5.80954792449, 5.80954792449, 5.80954792449, 5.80954792449, 5.80954792449, 5.80954792449, 5.80954792449, 5.80954792449, 5.80954792449, 5.80954792449, 5.80954792449, 5.80954792449, 5.80954792449, 5.80954792449, 5.80954792449, 5.80954792449, 5.80954792449, 5.80954792449, 4.35720593569, 5.80954792449, 5.80954792449, 5.80954792449, 5.80954792449, 5.80954792449, 5.80954792449, 5.80954792449, 5.80954792449, 5.80954792449, 5.80954792449, 5.80954792449, 5.80954792449, 5.80954792449, 5.80954792449, 5.80954792449, 5.80954792449, 5.80954792449, 5.80954792449, 5.80954792449, 5.80954792449, 5.80954792449, 5.80954792449, 5.80954792449, 5.80954792449, 5.80954792449, 5.80954792449, 5.80954792449, 5.80954792449, 5.80954792449, 5.80954792449, 5.80954792449, 5.80954792449, 5.80954792449, 5.80954792449, 5.80954792449, 5.80954792449, 5.80954792449, 5.80954792449, 5.80954792449, 5.80954792449, 5.80954792449, 5.80954792449, 5.80954792449, 5.80954792449, 5.80954792449, 5.80954792449, 5.80954792449, 5.80954792449, 5.80954792449, 5.80954792449, 5.80954792449, 5.80954792449, 5.80954792449, 5.80954792449, 5.80954792449, 5.80954792449, 5.80954792449, 5.80954792449, 5.80954792449, 5.80954792449, 5.80954792449, 5.80954792449, 5.80954792449, 4.45750130090], [5.811355302, 5.811355302, 5.811355302, 5.811355302, 5.811355302, 5.811355302, 5.811355302, 5.811355302, 5.811355302, 5.811355302, 5.811355302, 5.811355302, 5.811355302, 5.811355302, 5.811355302, 5.811355302, 5.811355302, 5.811355302, 5.811355302, 5.811355302, 5.811355302, 5.811355302, 5.811355302, 5.811355302, 5.811355302, 4.920038732, 4.874151969, 5.62765253, 5.811355302, 5.811355302, 5.811355302, 5.811355302, 5.811355302, 5.811355302, 5.811355302, 5.811355302, 5.811355302, 5.811355302, 5.811355302, 5.811355302, 5.811355302, 4.988037528, 4.358233789, 3.338174179, 3.329279863, 4.359820374, 5.811355302, 5.811355302, 5.811355302, 5.811355302, 5.811355302, 5.811355302, 5.811355302, 5.811355302, 5.811355302, 5.811355302, 5.332464215, 4.056888872, 3.773886292, 4.989577734, 5.811355302, 5.811355302, 5.811355302, 5.811355302, 5.811355302, 5.811355302, 5.811355302, 5.811355302, 5.811355302, 5.811355302, 5.811355302, 5.811355302, 5.811355302, 5.811355302, 5.811355302, 5.811355302, 5.811355302, 5.811355302, 5.811355302, 5.811355302, 5.811355302, 5.811355302, 5.811355302, 5.811355302, 5.811355302, 5.811355302, 5.811355302, 5.811355302, 5.811355302, 5.811355302, 5.811355302, 5.811355302, 5.811355302, 5.811355302, 5.811355302, 5.811355302, 5.811355302, 5.811355302, 5.811355302, 5.811355302, 5.811355302, 5.811355302, 5.811355302, 5.811355302, 5.811355302, 5.811355302, 5.811355302, 5.811355302, 5.811355302, 5.811355302, 5.811355302, 5.811355302, 5.811355302, 5.811355302, 5.811355302, 5.811355302, 5.811355302, 5.811355302, 5.811355302, 5.811355302, 5.811355302, 5.811355302, 5.811355302, 5.811355302, 5.811355302, 5.811355302, 5.811355302, 5.72555695, 4.300560581, 3.815151943, 4.406469363, 5.811355302, 5.811355302, 5.811355302, 5.811355302, 5.811355302, 5.811355302, 5.811355302, 5.811355302, 5.811355302, 5.811355302, 5.811355302, 5.811355302, 5.811355302, 5.811355302, 5.811355302, 5.811355302, 5.811355302, 5.811355302, 5.811355302, 5.811355302, 5.811355302, 5.811355302, 5.811355302, 5.811355302, 5.811355302, 5.811355302, 5.811355302, 5.811355302, 5.811355302, 5.811355302, 5.811355302, 5.811355302, 5.811355302, 5.811355302, 5.811355302, 5.811355302, 5.811355302, 5.811355302, 5.811355302, 5.811355302, 5.811355302, 5.811355302, 5.811355302, 5.811355302, 5.811355302, 5.811355302, 5.811355302, 5.811355302]]
    for count, speedList in enumerate(speedListList):
        QAfield = selectedFields[count]
        print(QAfield['fieldLabel'])
        fieldInfo = get_field_info(MRN, QAfield['fieldId'])
        print(fieldInfo['beamMeterset'])
        #print(QAfield)
        #print(fieldInfo)
        #return None
        total = 0.0
        areaList = []
        
        maxSpeed = 0.0
        index = 0
        positionListList = []
        positionListListB = []
        gantryList = []
        
        for a, dictionary in enumerate(fieldInfo['mqControlPoints']):
            leafSetA = dictionary['leafSetA']
            leafSetB = dictionary['leafSetB']
            negLeafSetB = [-x for x in leafSetB]
            
            if a == 0:
                # jaw placement assumes leaves are 5 mm
                bottom = int(len(leafSetA)/2) - int(2 * dictionary['collimatorX1'])
                jawDistance = int(2 * dictionary['fieldX'])
                
                jawOpen = [False for i in range(bottom)]
                jawOpen.extend([True for j in range(jawDistance)])
                jawOpen.extend([False for k in range((len(leafSetA) - bottom - jawDistance))])
            
            #y = [i for i in range(len(leafSetA))]
              
            area = 0
            for i, value in enumerate(leafSetA):
                if a == 0:
                    positionListList.append([value])
                    positionListListB.append([negLeafSetB[i]])
                else:
                    positionListList[i].append(value)
                    positionListListB[i].append(negLeafSetB[i])
                if i == 0:
                    gantryList.append(dictionary['gantryAngle'])
                if jawOpen[i]:
                    diff = abs(value - negLeafSetB[i])
                    area = area + 0.5*diff
            
            area = round(area, 5)
            areaList.append(area)
            total = total + area
            point = dictionary['point']   
        
            '''
        #print(gantryList) 
        for i, angle in enumerate(gantryList):
            if angle == 1 and gantryList[i-1] == 3:
                newGantryList  = gantryList[i+1:] + gantryList[:i+1]
                forward = True
            elif angle == 1 and gantryList[i-1] == 359:
                newGantryList  = gantryList[i:] + gantryList[:i]
                forward = False
               
        for h, posList in enumerate(positionListList):
            posListB = positionListListB[h]
            for i, pos in enumerate(posList):
                if forward:
                    newPosList = posList[i+1:] + posList[:i+1]
                else:
                    newPosList = posList[i:] + posList[:i]
        
                
                
        flip = False
        if newGantryList[0] != 1:
            newGantryList.reverse()
            flip = True
        '''
        for i, angle in enumerate(gantryList):
            if angle == 1 and gantryList[i-1] == 3:
                gantryList1 = gantryList[i+1:] 
                gantryList2 =  gantryList[:i+1]
                
                gantryIndex = i + 1
                #forward = True
            elif angle == 1 and gantryList[i-1] == 359:
                gantryList1 = gantryList[i:] 
                gantryList2 =  gantryList[:i]
                
                gantryIndex = i
                #forward = False
        
        #newGantryList = gantryList
        
        maxSpeed = 0
        totalDistance = 0
        distanceList = []
        totalDistanceB = 0
        distanceListB = []
        for h, posList in enumerate(positionListList):
            posListB = positionListListB[h]
            prevPos = 0.0
            prevPosB = 0.0
            totalDifference = 0
            totalDifferenceB = 0
            
            if jawOpen[h]:
                spdList = []
                secSpeedList = []
                secSpeedListB = []
                
                for i, pos in enumerate(posList):
                    posB = posListB[i]
                    if i > 0 and i < (len(posList) - 1):
                        speed = (posList[i+1] - posList[i-1])/4
                        speedB = (posListB[i+1] - posListB[i-1])/4
                        secSpeed = speed * speedList[h]
                        secSpeedB = speedB * speedList[h]
                        spdList.append(speed)
                        secSpeedList.append(secSpeed)
                        secSpeedListB.append(secSpeedB)
                        
                        if prevPos != 0.0:
                            difference = abs(pos - prevPos)
                            totalDifference = totalDifference + difference
                            
                            differenceB = abs(posB - prevPosB)
                            totalDifferenceB = totalDifferenceB + differenceB
                        prevPos = pos 
                        prevPosB = posB
                totalDistance = totalDistance + totalDifference
                distanceList.append(totalDifference)
                
                totalDistanceB = totalDistanceB + totalDifferenceB
                distanceListB.append(totalDifferenceB)
                
                absListA = [abs(x) for x in secSpeedList]
                absListB = [abs(x) for x in secSpeedListB]
                if max(absListA) > maxSpeed:
                    maxSpeed = max(absListA)
                    index = h
                if max(absListB) > maxSpeed:
                    maxSpeed = max(absListB)
                    index = h
                
        
        mean = round((total/(point + 1)), 2)
        averageDis = round((totalDistance/len(distanceList)), 3)
        print('The mean area is:\t', mean, u'cm\u00B2 \nThe max area is:\t', max(areaList), u'cm\u00B2 at index', areaList.index(max(areaList)), '\nThe min area is:\t', min(areaList), u'cm\u00B2 at index', areaList.index(min(areaList)))
        print('\nThe max speed is:\t', round(maxSpeed, 3), 'cm/s at index', index) 
        print('\nThe mean distance is:\t', averageDis, 'cm\nThe max distance is:\t', round(max(distanceList), 3), 'cm\nThe min distance is:\t', round(min(distanceList), 3), 'cm\n')
        
        x = [i for i in range(len(distanceList))]
        fig, (ax0) = plt.subplots()
        ax0.plot(x, distanceList, 'o', color='mediumslateblue', label='A')
        ax0.plot(x, distanceListB, 'o', color='salmon', label='B')
        plt.xlabel('Gantry Index')
        plt.ylabel('Distance Travelled (cm)')
        plt.legend()
        plt.title('Distance Travelled of Gantry Leaves ' + QAfield['fieldLabel'])
        plt.show()

def areaVsUnits(graphTitle, MRNlist):
    tic = time.perf_counter()
    # lists of values to graph
    MUlist = []
    MUlistFFF = []
    MUtrue = []
    MUagility = []
    meanAreaList = []
    meanAreaListFFF = []
    meanAreaTrue = []
    meanAreaAgility = []
    maxList = []
    maxListFFF = []
    minList = []
    minListFFF = []
    maxAgility = []
    maxTrue = []
    minAgility = []
    minTrue = []
    stdevList = []
    stdevListFFF = []
    stdevAgility = []
    stdevTrue = []
    
    
    for MRN in MRNlist:
        QAfields = get_qa_records(MRN)
        fieldIndexes = []
        QAfieldsNew = []
        for QAfield in QAfields:
            time1 = QAfield['treatmentTime'][:4]
            if int(time1) > 2019:  
                if QAfield['fieldLabel'] not in fieldIndexes:
                    QAfieldsNew.append(QAfield)
                    fieldIndexes.append(QAfield['fieldLabel'])
        
        for QAfield in QAfieldsNew:
            fieldInfo = get_field_info(MRN, QAfield['fieldId'])
            siteInfo = get_site_info(QAfield['siteSetId'])
            try:
                if fieldInfo['isFff']:
                    MUlistFFF.append(fieldInfo['beamMeterset'])
                else:
                    MUlist.append(fieldInfo['beamMeterset'])
                    if fieldInfo['machineType'] == 'Agility' or 'Agility' in fieldInfo['machineType']:
                        MUagility.append(fieldInfo['beamMeterset'])
                    else:
                        MUtrue.append(fieldInfo['beamMeterset'])
            except:
                continue
            
            if siteInfo['totalDose'] != 2400.0 or siteInfo['fractions'] != 2:
                if fieldInfo['beamMeterset'] in MUlist:
                    MUlist.remove(fieldInfo['beamMeterset'])
                    if fieldInfo['beamMeterset'] in MUagility:
                        MUagility.remove(fieldInfo['beamMeterset'])
                    elif fieldInfo['beamMeterset'] in MUtrue:
                        MUtrue.remove(fieldInfo['beamMeterset'])
                elif fieldInfo['beamMeterset'] in MUlistFFF:
                    MUlistFFF.remove(fieldInfo['beamMeterset'])
                continue
            
            #if fieldInfo['beamMeterset'] < 3000.0:
             #   print(MRN, QAfield['fieldLabel'], fieldInfo['beamMeterset'])
            total = 0
            areaList = []
            
            for i, dictionary in enumerate(fieldInfo['mqControlPoints']):
                leafSetA = dictionary['leafSetA']
                leafSetB = dictionary['leafSetB']
                negLeafSetB = [-x for x in leafSetB]
                
                # jaw placement assumes leaves are 5 mm
                bottom = int(len(leafSetA)/2) - int(2 * dictionary['collimatorX1'])
                jawDistance = int(2 * dictionary['fieldX'])
                
                jawOpen = [False for i in range(bottom)]
                jawOpen.extend([True for j in range(jawDistance)])
                jawOpen.extend([False for k in range((len(leafSetA) - bottom - jawDistance))])
                
                area = 0
                for j, value in enumerate(leafSetA):  
                    if jawOpen[j]:
                        diff = abs(value - negLeafSetB[j])
                        area = area + 0.5*diff
                
                areaList.append(area)
                total = total + area
                point = dictionary['point']
            
            maxArea = round(max(areaList), 5)
            minArea = round(min(areaList), 5)
            #if maxArea > 25.0:
             #   print(MRN, QAfield['fieldLabel'], maxArea)
            
            mean = round((total/(point + 1)), 3)
            if fieldInfo['isFff']:
                meanAreaListFFF.append(mean)
                maxListFFF.append(round((maxArea - mean), 5))
                minListFFF.append(round((mean - minArea), 5))
            else:
                meanAreaList.append(mean)
                maxList.append(round((maxArea - mean), 5))
                minList.append(round((mean - minArea), 5))
                if fieldInfo['machineType'] == 'Agility' or 'Agility' in fieldInfo['machineType']:
                    meanAreaAgility.append(mean)
                    maxAgility.append(round((maxArea - mean), 5))
                    minAgility.append(round((mean - minArea), 5))
                else:
                    meanAreaTrue.append(mean)
                    maxTrue.append(round((maxArea - mean), 5))
                    minTrue.append(round((mean - minArea), 5))
            # calculating stdev
            diffTotal = 0
            for area in areaList:
                sqDiff = abs(area - mean) * abs(area - mean)
                diffTotal = diffTotal + sqDiff
            
            stdev = math.sqrt(diffTotal/(len(areaList) - 1))
            
            if fieldInfo['isFff']:
                stdevListFFF.append(stdev)
            else:
                stdevList.append(stdev)
                if fieldInfo['machineType'] == 'Agility' or 'Agility' in fieldInfo['machineType']:
                    stdevAgility.append(stdev)
                else:
                    stdevTrue.append(stdev)

    modulationList = [i/2400 for i in MUlist]
    modulationListFFF = [i/2400 for i in MUlistFFF]
    modulationTrue = [i/2400 for i in MUtrue]
    modulationAgility = [i/2400 for i in MUagility]           
    
    errorBars = [minList, maxList]
    errorBarsFFF = [minListFFF, maxListFFF]
    errorBarsAgility = [minAgility, maxAgility]
    errorBarsTrue = [minTrue, maxTrue]
    
    fig, (ax0) = plt.subplots()
    ax0.errorbar(meanAreaList, MUlist, xerr=errorBars, fmt='o', color='darkred', ecolor='salmon', label='6X')
    ax0.errorbar(meanAreaListFFF, MUlistFFF, xerr=errorBarsFFF, fmt='o', color='darkblue', ecolor='mediumslateblue', label='6FFF')
    plt.legend()
    plt.xlabel('Mean Segment Area (cm2)')
    plt.ylabel('# of Monitor Units')
    plt.title('MUs vs. Mean Segment Area 24/2 2020-21')
    plt.show()
    
    fig, (ax2) = plt.subplots()
    ax2.errorbar(meanAreaListFFF, MUlistFFF, xerr=errorBarsFFF, fmt='o', color='darkblue', ecolor='mediumslateblue', label='6FFF')
    plt.xlabel('Mean Segment Area (cm2)')
    plt.ylabel('# of Monitor Units')
    plt.title('MUs vs. Mean Segment Area 6FFF 24/2 2020-21')
    plt.show()
    
    fig, (ax3) = plt.subplots()
    ax3.errorbar(meanAreaAgility, MUagility, xerr=errorBarsAgility, fmt='o', color='darkred', ecolor='salmon', label='Agility')
    ax3.errorbar(meanAreaTrue, MUtrue, xerr=errorBarsTrue, fmt='o', color='darkblue', ecolor='mediumslateblue', label='Truebeam')
    plt.legend()
    plt.xlabel('Mean Segment Area (cm2)')
    plt.ylabel('# of Monitor Units')
    plt.title('MUs vs. Mean Segment Area 6X 24/2 2020-21')
    plt.show()
    
    fig, (ax6) = plt.subplots()
    ax6.errorbar(meanAreaList, modulationList, xerr=errorBars, fmt='o', color='darkred', ecolor='salmon', label='6X')
    ax6.errorbar(meanAreaListFFF, modulationListFFF, xerr=errorBarsFFF, fmt='o', color='darkblue', ecolor='mediumslateblue', label='6FFF')
    plt.legend()
    plt.xlabel('Mean Segment Area (cm2)')
    plt.ylabel('Modulation')
    plt.title('Modulation vs. Mean Segment Area 24/2 2020-21')
    plt.show()
    
    fig, (ax7) = plt.subplots()
    ax7.errorbar(meanAreaListFFF, modulationListFFF, xerr=errorBarsFFF, fmt='o', color='darkblue', ecolor='mediumslateblue', label='6FFF')
    plt.xlabel('Mean Segment Area (cm2)')
    plt.ylabel('Modulation')
    plt.title('Modulation vs. Mean Segment Area 6FFF 24/2 2020-21')
    plt.show()
    
    fig, (ax8) = plt.subplots()
    ax8.errorbar(meanAreaAgility, modulationAgility, xerr=errorBarsAgility, fmt='o', color='darkred', ecolor='salmon', label='Agility')
    ax8.errorbar(meanAreaTrue, modulationTrue, xerr=errorBarsTrue, fmt='o', color='darkblue', ecolor='mediumslateblue', label='Truebeam')
    plt.legend()
    plt.xlabel('Mean Segment Area (cm2)')
    plt.ylabel('Modulation')
    plt.title('Modulation vs. Mean Segment Area 6X 24/2 2020-21')
    plt.show()
    
    fig, (ax1) = plt.subplots()
    ax1.plot(stdevList, MUlist, 'o', color='darkred', label='6X')
    ax1.plot(stdevListFFF, MUlistFFF, 'o', color='darkblue', label='6FFF')
    ax1.legend()
    plt.xlabel('Standard Deviation (cm2)')
    plt.ylabel('# of Moniter Units')
    plt.title('MUs vs. St Dev 24/2 2020-21')
    plt.show()
    
    fig, (ax4) = plt.subplots()
    ax4.plot(stdevListFFF, MUlistFFF, 'o', color='darkblue', label='6FFF')
    ax4.legend()
    plt.xlabel('Standard Deviation (cm2)')
    plt.ylabel('# of Moniter Units')
    plt.title('MUs vs. St Dev 6FFF 24/2 2020-21')
    plt.show()
    
    fig, (ax5) = plt.subplots()
    ax5.plot(stdevAgility, MUagility, 'o', color='darkred', label='Agility')
    ax5.plot(stdevTrue, MUtrue, 'o', color='darkblue', label='True')
    ax5.legend()
    plt.xlabel('Standard Deviation (cm2)')
    plt.ylabel('# of Moniter Units')
    plt.title('MUs vs. St Dev 6X 24/2 2020-21')
    plt.show()
    
    toc = time.perf_counter()
    timeDiff = toc-tic
    print('Time:\t', timeDiff, 's\n# of MRNs:\t', len(MRNlist))
    
def passVsUnits(graphTitle, MRNlist):
    tic = time.perf_counter()
    # lists of values to graph
    MUlist = []
    MUlistFFF = []
    MUtrue = []
    MUagility = []
    absList = []
    absListFFF = []
    relList = []
    relListFFF = []
    
    for MRN in MRNlist:
        QAfields = get_qa_records(MRN)
        fieldIndexes = []
        QAfieldsNew = []
        for QAfield in QAfields:
            time1 = QAfield['treatmentTime'][:4]
            if int(time1) > 2019:  
                if QAfield['fieldLabel'] not in fieldIndexes:
                    QAfieldsNew.append(QAfield)
                    fieldIndexes.append(QAfield['fieldLabel'])
                        
        for QAfield in QAfieldsNew:
            fieldInfo = get_field_info(MRN, QAfield['fieldId'])
            siteInfo = get_site_info(QAfield['siteSetId'])
            if siteInfo['totalDose'] != 2400.0 or siteInfo['fractions'] != 2:
                continue
            
            try:
                if fieldInfo['isFff']:
                    MUlistFFF.append(fieldInfo['beamMeterset'])
                else:
                    MUlist.append(fieldInfo['beamMeterset'])
                    if fieldInfo['machineType'] == 'Agility' or 'Agility' in fieldInfo['machineType']:
                        MUagility.append(fieldInfo['beamMeterset'])
                    else:
                        MUtrue.append(fieldInfo['beamMeterset'])
            except:
                continue
            
            passrates = getPassRates(MRN, QAfield['fieldLabel'])
            if fieldInfo['isFff']:
                try:
                    absListFFF.append(passrates['AD'])
                    relListFFF.append(passrates['RD'])
                except:
                    MUlistFFF.remove(fieldInfo['beamMeterset'])
                    continue
            else:
                try:
                    absList.append(passrates['AD'])
                    relList.append(passrates['RD'])
                except:
                    MUlist.remove(fieldInfo['beamMeterset'])
                    continue
            
            #print(MRN, '\t', passrates['AD'], '\t', passrates['RD'])
    '''        
    plt.plot(MUlist, absList, 'o', color='darkred', label='Non-FFF')
    plt.plot(MUlistFFF, absListFFF, 'o', color='darkblue', label='FFF')
    plt.title(graphTitle)
    plt.legend()
    plt.xlabel('# of Monitor Units')
    plt.ylabel('Absolute Passrate')
    plt.show()
    
    plt.plot(MUlist, relList, 'o', color='darkred', label='Non-FFF')
    plt.plot(MUlistFFF, relListFFF, 'o', color='darkblue', label='FFF')
    plt.title(graphTitle)
    plt.legend()
    plt.xlabel('# of Monitor Units')
    plt.ylabel('Relative Passrate')
    plt.show()
    '''
    fig, (ax0) = plt.subplots()
    try:
        for i, x1 in enumerate(MUlist):
            y1 = absList[i]
            y2 = relList[i]
            ax0.plot((x1, x1), (y1, y2), color='lightgray')
    except:
        print(i)
    ax0.plot(MUlist, absList, 'o', color='darkred', label='Abs 6X')
    ax0.plot(MUlist, relList, 'o', color='salmon', label='Rel 6X')
    plt.title('Passrate vs. MUs 24/2 2020-21')
    plt.xlabel('# of Monitor Units')
    plt.legend()
    plt.ylabel('Passrate')
    plt.show()
    
    fig, (ax1) = plt.subplots()
    for i, x1 in enumerate(MUlistFFF):
        y1 = absListFFF[i]
        y2 = relListFFF[i]
        ax1.plot((x1, x1), (y1, y2), color='lightsteelblue') 
    ax1.plot(MUlistFFF, absListFFF, 'o', color='darkblue', label='Abs 6FFF')
    ax1.plot(MUlistFFF, relListFFF, 'o', color='mediumslateblue', label='Rel 6FFF')
    plt.title('MUs vs. Passrate 6FFF 24/2 2020-21')
    plt.legend()
    plt.xlabel('# of Monitor Units')
    plt.ylabel('Passrate')
    plt.show()
    
    print('Number of points graphed:\t', (len(MUlist) + len(MUlistFFF)))
    
    toc = time.perf_counter()
    timeDiff = toc-tic
    print('Time:\t', timeDiff, 's\n# of MRNs:\t', len(MRNlist))
    
def passVsStdev(MRNlist):
    tic = time.perf_counter()
    # lists of values to graph
    stdevList = []
    stdevListFFF = []
    stdevAgility = []
    stdevTrue = []
    relStdevList = []
    relStdevListFFF = []
    relStdevAgility = []
    relStdevTrue = []
    absList = []
    absListFFF = []
    absAgility = []
    absTrue = []
    relList = []
    relListFFF = []
    relAgility = []
    relTrue = []
    
    for MRN in MRNlist:
        QAfields = get_qa_records(MRN)
        fieldIndexes = []
        QAfieldsNew = []
        for QAfield in QAfields:
            time1 = QAfield['treatmentTime'][:4]
            if int(time1) > 2019:  
                if QAfield['fieldLabel'] not in fieldIndexes:
                    QAfieldsNew.append(QAfield)
                    fieldIndexes.append(QAfield['fieldLabel'])
        for QAfield in QAfieldsNew:
            fieldInfo = get_field_info(MRN, QAfield['fieldId'])
            siteInfo = get_site_info(QAfield['siteSetId'])
            if siteInfo['totalDose'] != 2400.0 or siteInfo['fractions'] != 2:
                continue
            
            passrates = getPassRates(MRN, QAfield['fieldLabel'])
            if fieldInfo['isFff']:
                try:
                    absListFFF.append(passrates['AD'])
                    relListFFF.append(passrates['RD'])
                except:
                    continue
            else:
                try:
                    absList.append(passrates['AD'])
                    relList.append(passrates['RD'])
                    if fieldInfo['machineType'] == 'Agility' or 'Agility' in fieldInfo['machineType']:
                        absAgility.append(passrates['AD'])
                        relAgility.append(passrates['RD'])
                    else:
                        absTrue.append(passrates['AD'])
                        relTrue.append(passrates['RD'])
                except:
                    continue
                
            total = 0
            areaList = []
            
            for i, dictionary in enumerate(fieldInfo['mqControlPoints']):
                leafSetA = dictionary['leafSetA']
                leafSetB = dictionary['leafSetB']
                negLeafSetB = [-x for x in leafSetB]
                
                # jaw placement assumes leaves are 5 mm
                bottom = int(len(leafSetA)/2) - int(2 * dictionary['collimatorX1'])
                jawDistance = int(2 * dictionary['fieldX'])
                
                jawOpen = [False for i in range(bottom)]
                jawOpen.extend([True for j in range(jawDistance)])
                jawOpen.extend([False for k in range((len(leafSetA) - bottom - jawDistance))])
                
                area = 0
                for j, value in enumerate(leafSetA):  
                    if jawOpen[j]:
                        diff = abs(value - negLeafSetB[j])
                        area = area + 0.5*diff
                
                areaList.append(area)
                total = total + area
                point = dictionary['point']
            #calculating stdev    
            mean = round((total/(point + 1)), 3)
            diffTotal = 0
            for area in areaList:
                sqDiff = abs(area - mean) * abs(area - mean)
                diffTotal = diffTotal + sqDiff
            
            stdev = math.sqrt(diffTotal/(len(areaList) - 1))
            relStdev = stdev/mean
            
            if fieldInfo['isFff']:
                stdevListFFF.append(stdev)
                relStdevListFFF.append(relStdev)
            else:
                stdevList.append(stdev)
                relStdevList.append(relStdev)
                if fieldInfo['machineType'] == 'Agility' or 'Agility' in fieldInfo['machineType']:
                    stdevAgility.append(stdev)
                    relStdevAgility.append(relStdev)
                else:
                    stdevTrue.append(stdev)
                    relStdevTrue.append(relStdev)
                
    fig, (ax0) = plt.subplots()
    for i, x1 in enumerate(stdevList):
        y1 = absList[i]
        y2 = relList[i]
        ax0.plot((x1, x1), (y1, y2), color='lightgray')
    ax0.plot(stdevList, absList, 'o', color='darkred', label='Abs 6X')
    ax0.plot(stdevList, relList, 'o', color='salmon', label='Rel 6X')
    plt.title('Pass Rates vs. St Dev 6X 24/2 2020-21')
    plt.xlabel('Standard Deviation of Area (cm2)')
    plt.legend()
    plt.ylabel('Passrate (%)')
    plt.show()
    
    fig, (ax1) = plt.subplots()
    for i, x1 in enumerate(stdevListFFF):
        y1 = absListFFF[i]
        y2 = relListFFF[i]
        ax1.plot((x1, x1), (y1, y2), color='lightsteelblue') 
    ax1.plot(stdevListFFF, absListFFF, 'o', color='darkblue', label='Abs 6FFF')
    ax1.plot(stdevListFFF, relListFFF, 'o', color='mediumslateblue', label='Rel 6FFF')
    plt.title('Pass Rates vs. St Dev 6FFF 24/2 2020-21')
    plt.legend()
    plt.xlabel('Standard Deviation of Area (cm2)')
    plt.ylabel('Passrate (%)')
    plt.show()
    
    fig, (ax2) = plt.subplots()
    for i, x1 in enumerate(stdevAgility):
        y1 = absAgility[i]
        y2 = relAgility[i]
        ax2.plot((x1, x1), (y1, y2), color='lightgray')
    for i, x1 in enumerate(stdevTrue):
        y1 = absTrue[i]
        y2 = relTrue[i]
        ax2.plot((x1, x1), (y1, y2), color='lightsteelblue') 
    ax2.plot(stdevAgility, absAgility, 'o', color='darkred', label='Abs Agility')
    ax2.plot(stdevAgility, relAgility, 'o', color='salmon', label='Rel Agility')
    ax2.plot(stdevTrue, absTrue, 'o', color='darkblue', label='Abs Truebeam')
    ax2.plot(stdevTrue, relTrue, 'o', color='mediumslateblue', label='Rel Truebeam')
    plt.title('Pass Rates vs. St Dev 6X 24/2 2020-21')
    plt.xlabel('Standard Deviation of Area (cm2)')
    plt.legend()
    plt.ylabel('Passrate (%)')
    plt.show()
    
    fig, (ax3) = plt.subplots()
    for i, x1 in enumerate(relStdevList):
        y1 = absList[i]
        y2 = relList[i]
        ax3.plot((x1, x1), (y1, y2), color='lightgray')
    ax3.plot(relStdevList, absList, 'o', color='darkred', label='Abs 6X')
    ax3.plot(relStdevList, relList, 'o', color='salmon', label='Rel 6X')
    plt.title('Pass Rates vs. Relative St Dev 6X 24/2 2020-21')
    plt.xlabel('Relative Standard Deviation of Area')
    plt.legend()
    plt.ylabel('Passrate (%)')
    plt.show()
    
    fig, (ax4) = plt.subplots()
    for i, x1 in enumerate(relStdevListFFF):
        y1 = absListFFF[i]
        y2 = relListFFF[i]
        ax4.plot((x1, x1), (y1, y2), color='lightsteelblue') 
    ax4.plot(relStdevListFFF, absListFFF, 'o', color='darkblue', label='Abs 6FFF')
    ax4.plot(relStdevListFFF, relListFFF, 'o', color='mediumslateblue', label='Rel 6FFF')
    plt.title('Pass Rates vs. Relative St Dev 6FFF 24/2 2020-21')
    plt.legend()
    plt.xlabel('Relative Standard Deviation of Area')
    plt.ylabel('Passrate (%)')
    plt.show()
    
    fig, (ax5) = plt.subplots()
    for i, x1 in enumerate(relStdevAgility):
        y1 = absAgility[i]
        y2 = relAgility[i]
        ax5.plot((x1, x1), (y1, y2), color='lightgray')
    for i, x1 in enumerate(relStdevTrue):
        y1 = absTrue[i]
        y2 = relTrue[i]
        ax5.plot((x1, x1), (y1, y2), color='lightsteelblue') 
    ax5.plot(relStdevAgility, absAgility, 'o', color='darkred', label='Abs Agility')
    ax5.plot(relStdevAgility, relAgility, 'o', color='salmon', label='Rel Agility')
    ax5.plot(relStdevTrue, absTrue, 'o', color='darkblue', label='Abs Truebeam')
    ax5.plot(relStdevTrue, relTrue, 'o', color='mediumslateblue', label='Rel Truebeam')
    plt.title('Pass Rates vs. Relative St Dev 6X 24/2 2020-21')
    plt.xlabel('Relative Standard Deviation of Area')
    plt.legend()
    plt.ylabel('Passrate (%)')
    plt.show()
    
    
    toc = time.perf_counter()
    timeDiff = toc-tic
    print('# of MRNs:\t', len(MRNlist), '\n# of cases:\t', (len(stdevList)+len(stdevListFFF)))
    print('Time:\t', timeDiff)


def passVsDist(MRNlist):
    tic = time.perf_counter()
    # lists of values to graph
    absList = []
    absListFFF = []
    absAgility = []
    absTrue = []
    
    relList = []
    relListFFF = []
    relAgility = []
    relTrue = []
    
    totalDisListFFF = []
    totalDisListAgility = []
    totalDisListTrue = []
    meanDisListFFF = []
    meanDisListAgility = []
    meanDisListTrue = []
    maxDisList = []
    minDisList = []
    
    stdevListFFF = []
    stdevAgility = []
    stdevTrue = []
    
    for MRN in MRNlist:
        QAfields = get_qa_records(MRN)
        fieldIndexes = []
        QAfieldsNew = []
        # sorts out QA fields from before 2020 and repeats
        for QAfield in QAfields:
            time1 = QAfield['treatmentTime'][:4]
            if int(time1) > 2019:  
                if QAfield['fieldLabel'] not in fieldIndexes:
                    QAfieldsNew.append(QAfield)
                    fieldIndexes.append(QAfield['fieldLabel'])
        
        for QAfield in QAfieldsNew:
            fieldInfo = get_field_info(MRN, QAfield['fieldId'])
            siteInfo = get_site_info(QAfield['siteSetId'])
            # sorts out QA fields that aren't 24 Gy/2 fx
            if siteInfo['totalDose'] != 2400.0 or siteInfo['fractions'] != 2:
                continue
            # obtains passrates for the QA field
            passrates = getPassRates(MRN, QAfield['fieldLabel'])
            if fieldInfo['isFff']:
                try:
                    absListFFF.append(passrates['AD'])
                    relListFFF.append(passrates['RD'])
                except:
                    continue
            else:
                try:
                    absList.append(passrates['AD'])
                    relList.append(passrates['RD'])
                    if fieldInfo['machineType'] == 'Agility' or 'Agility' in fieldInfo['machineType']:
                        absAgility.append(passrates['AD'])
                        relAgility.append(passrates['RD'])
                    else:
                        absTrue.append(passrates['AD'])
                        relTrue.append(passrates['RD'])
                except:
                    continue
            
            positionListList = []
            positionListListB = []
            
            for i, dictionary in enumerate(fieldInfo['mqControlPoints']):
                leafSetA = dictionary['leafSetA']
                leafSetB = dictionary['leafSetB']
                negLeafSetB = [-x for x in leafSetB]
                
                if i == 0:
                    # jaw placement assumes leaves are 5 mm
                    bottom = int(len(leafSetA)/2) - int(2 * dictionary['collimatorX1'])
                    jawDistance = int(2 * dictionary['fieldX'])
                    
                    jawOpen = [False for j in range(bottom)]
                    jawOpen.extend([True for j in range(jawDistance)])
                    jawOpen.extend([False for k in range((len(leafSetA) - bottom - jawDistance))])
                
                for j, value in enumerate(leafSetA):
                    if i == 0:
                        positionListList.append([value])
                        positionListListB.append([negLeafSetB[j]])
                    else:
                        positionListList[j].append(value)
                        positionListListB[j].append(negLeafSetB[j])
            
            totalDistance = 0
            distanceList = []
            totalDistanceB = 0
            distanceListB = []
            for i, posList in enumerate(positionListList):
                posListB = positionListListB[i]
                prevPos = 0.0
                prevPosB = 0.0
                totalDifference = 0
                totalDifferenceB = 0
                
                if jawOpen[i]:
                    for j, pos in enumerate(posList):
                        posB = posListB[j]
                        if prevPos != 0.0:
                            difference = abs(pos - prevPos)
                            totalDifference = totalDifference + difference
                            
                            differenceB = abs(posB - prevPosB)
                            totalDifferenceB = totalDifferenceB + differenceB
                        prevPos = pos 
                        prevPosB = posB
                
                totalDistance = totalDistance + totalDifference
                distanceList.append(totalDifference)
                
                totalDistanceB = totalDistanceB + totalDifferenceB
                distanceListB.append(totalDifferenceB)
                       
            averageDisA = totalDistance/len(distanceList)
            averageDisB = totalDistanceB/len(distanceListB)
            averageDis = (totalDistance + totalDistanceB)/(len(distanceList) + len(distanceListB))
            
            diffTotal = 0
            for dis in distanceList:
                sqDiff = abs(dis - averageDis) * abs(dis - averageDis)
                diffTotal = diffTotal + sqDiff
            for dis in distanceListB:
                sqDiff = abs(dis - averageDis) * abs(dis - averageDis)
                diffTotal = diffTotal + sqDiff
            stdev = math.sqrt(diffTotal/((len(distanceList) + len(distanceListB)) - 1))
            
            if min(distanceList) < min(distanceListB):
                minDis = min(distanceList)
            else:
                minDis = min(distanceListB)
            if max(distanceList) > max(distanceListB):
                maxDis = max(distanceList)
            else:
                maxDis = max(distanceListB)
            if fieldInfo['isFff']:
                totalDisListFFF.append(totalDistance + totalDistanceB)
                meanDisListFFF.append(averageDis) 
                stdevListFFF.append(stdev)
            else:
                if fieldInfo['machineType'] == 'Agility' or 'Agility' in fieldInfo['machineType']:
                    totalDisListAgility.append(totalDistance + totalDistanceB)
                    meanDisListAgility.append(averageDis) 
                    stdevAgility.append(stdev)
                else:
                    totalDisListTrue.append(totalDistance + totalDistanceB)
                    meanDisListTrue.append(averageDis)
                    stdevTrue.append(stdev)
            minDisList.append(minDis)
            maxDisList.append(maxDis)
            
      
    fig, (ax1) = plt.subplots()
    for i, x1 in enumerate(totalDisListFFF):
        y1 = absListFFF[i]
        y2 = relListFFF[i]
        ax1.plot((x1, x1), (y1, y2), color='lightsteelblue') 
    ax1.plot(totalDisListFFF, absListFFF, 'o', color='darkblue', label='Abs 6FFF')
    ax1.plot(totalDisListFFF, relListFFF, 'o', color='mediumslateblue', label='Rel 6FFF')
    plt.title('Pass Rates vs. Total Leaf Distance 6FFF 24/2 2020-21')
    plt.legend()
    plt.xlabel('Total Leaf Distance Travelled (cm)')
    plt.ylabel('Passrate (%)')
    plt.show()
    
    fig, (ax2) = plt.subplots()
    for i, x1 in enumerate(totalDisListAgility):
        y1 = absAgility[i]
        y2 = relAgility[i]
        ax2.plot((x1, x1), (y1, y2), color='lightgray')
    for i, x1 in enumerate(totalDisListTrue):
        y1 = absTrue[i]
        y2 = relTrue[i]
        ax2.plot((x1, x1), (y1, y2), color='lightsteelblue') 
    ax2.plot(totalDisListAgility, absAgility, 'o', color='darkred', label='Abs Agility')
    ax2.plot(totalDisListAgility, relAgility, 'o', color='salmon', label='Rel Agility')
    ax2.plot(totalDisListTrue, absTrue, 'o', color='darkblue', label='Abs Truebeam')
    ax2.plot(totalDisListTrue, relTrue, 'o', color='mediumslateblue', label='Rel Truebeam')
    plt.title('Pass Rates vs. Total Leaf Distance 6X 24/2 2020-21')
    plt.xlabel('Total Leaf Distance Travelled (cm)')
    plt.legend()
    plt.ylabel('Passrate (%)')
    plt.show()  
    
    fig, (ax3) = plt.subplots()
    for i, x1 in enumerate(meanDisListFFF):
        y1 = absListFFF[i]
        y2 = relListFFF[i]
        ax3.plot((x1, x1), (y1, y2), color='lightsteelblue') 
    ax3.plot(meanDisListFFF, absListFFF, 'o', color='darkblue', label='Abs 6FFF')
    ax3.plot(meanDisListFFF, relListFFF, 'o', color='mediumslateblue', label='Rel 6FFF')
    plt.title('Pass Rates vs. Mean Leaf Distance 6FFF 24/2 2020-21')
    plt.legend()
    plt.xlabel('Mean Leaf Distance Travelled (cm)')
    plt.ylabel('Passrate (%)')
    plt.show()
    
    fig, (ax4) = plt.subplots()
    for i, x1 in enumerate(meanDisListAgility):
        y1 = absAgility[i]
        y2 = relAgility[i]
        ax4.plot((x1, x1), (y1, y2), color='lightgray')
    for i, x1 in enumerate(meanDisListTrue):
        y1 = absTrue[i]
        y2 = relTrue[i]
        ax4.plot((x1, x1), (y1, y2), color='lightsteelblue') 
    ax4.plot(meanDisListAgility, absAgility, 'o', color='darkred', label='Abs Agility')
    ax4.plot(meanDisListAgility, relAgility, 'o', color='salmon', label='Rel Agility')
    ax4.plot(meanDisListTrue, absTrue, 'o', color='darkblue', label='Abs Truebeam')
    ax4.plot(meanDisListTrue, relTrue, 'o', color='mediumslateblue', label='Rel Truebeam')
    plt.title('Pass Rates vs. Mean Leaf Distance 6X 24/2 2020-21')
    plt.xlabel('Mean Leaf Distance Travelled (cm)')
    plt.legend()
    plt.ylabel('Passrate (%)')
    plt.show() 
    
    fig, (ax5) = plt.subplots()
    for i, x1 in enumerate(stdevListFFF):
        y1 = absListFFF[i]
        y2 = relListFFF[i]
        ax5.plot((x1, x1), (y1, y2), color='lightsteelblue') 
    ax5.plot(stdevListFFF, absListFFF, 'o', color='darkblue', label='Abs 6FFF')
    ax5.plot(stdevListFFF, relListFFF, 'o', color='mediumslateblue', label='Rel 6FFF')
    plt.title('Pass Rates vs. St Dev 6FFF 24/2 2020-21')
    plt.legend()
    plt.xlabel('Standard Deviation of Leaf Distance (cm)')
    plt.ylabel('Passrate (%)')
    plt.show()
    
    fig, (ax6) = plt.subplots()
    for i, x1 in enumerate(stdevAgility):
        y1 = absAgility[i]
        y2 = relAgility[i]
        ax6.plot((x1, x1), (y1, y2), color='lightgray')
    for i, x1 in enumerate(stdevTrue):
        y1 = absTrue[i]
        y2 = relTrue[i]
        ax6.plot((x1, x1), (y1, y2), color='lightsteelblue') 
    ax6.plot(stdevAgility, absAgility, 'o', color='darkred', label='Abs Agility')
    ax6.plot(stdevAgility, relAgility, 'o', color='salmon', label='Rel Agility')
    ax6.plot(stdevTrue, absTrue, 'o', color='darkblue', label='Abs Truebeam')
    ax6.plot(stdevTrue, relTrue, 'o', color='mediumslateblue', label='Rel Truebeam')
    plt.title('Pass Rates vs. St Dev 6X 24/2 2020-21')
    plt.xlabel('Standard Deviation of Leaf Distance (cm)')
    plt.legend()
    plt.ylabel('Passrate (%)')
    plt.show()
    
    
    toc = time.perf_counter()
    timeDiff = toc-tic
    print('# of MRNs:\t', len(MRNlist), '\n# of cases:\t', (len(meanDisListAgility)+len(meanDisListTrue)+len(meanDisListFFF)))
    print('Time:\t\t', timeDiff)         

# total distance leaves are travelling vs. passrates
        
# Liposarcoma, Retroperitoneum
if __name__ == '__main__':      
    mqControlPoints('1234567', ['C1', 'C2']) # not a real MRN