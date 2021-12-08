"""
Created on Tue Jun  1 14:17:42 2021
@author: weersim
"""

from mira_rest.mosaiq_qa import get_qa_records#, get_field_info, get_site_info
from mostRecent import mostRecentQueries
# import sys
# sys.path.append("Q:\VMAT QA Project\Madrigals Code")
 
def query_mosaiq(mrn, inputDate=''):
    # Retrieve all the QA fields for the given patient
    QAfields = get_qa_records(mrn)
    # qa_fields is a list of dictionaries
    print('Retrieved ' + str(len(QAfields)) + ' QA fields')
    
    # Selects qa fields from most recent date   
    QAfieldsSelected = mostRecentQueries(QAfields, inputDate)
    print(str(len(QAfieldsSelected)) + ' QA fields selected\n')
    
    beamList = []
    for QAfield in QAfieldsSelected:
        if QAfield['fieldLabel'] in beamList:
            QAfield['warning'] = 'The same beams have been delivered multiple times in one day. Please confirm with the associates.'
        else:
            beamList.append(QAfield['fieldLabel'])
    '''
    # The next loop should only be done for the selected QA fields
    for qa_field in QAfieldsSelected:
        print('Field name of QA field: ', qa_field['fieldLabel'])
        print('QA field was delivered on unit: ', qa_field['machineName'])
        print('Time QA field was delivered: ', qa_field['treatmentTime'])
        
        # Retrieve more info for each field, such as linac type, field type, and MUs
        field_info = get_field_info(mrn, qa_field['fieldId'])
        print('machineType = ', field_info['machineType'])
        print('Field type = ', field_info['type'])
        print('MU = ', field_info['beamMeterset'])
        
        # Retrieve prescription info
        site_info = get_site_info(qa_field['siteSetId'])
        print('Dose prescription = ', site_info['totalDose'])
        print('Dose per fraction = ', site_info['treatmentDose'], '\n')
    '''
    return QAfieldsSelected

if __name__ == '__main__':
    
    #mrn = "0005723" # IMRT fields
    #mrn = "3287540"
    #mrn = '4859154' # VMAT fields
    #mrn = '4835965'
    #mrn = '4859154'
    #mrn = '1134293'
    mrn = '4362627'
    
    query_mosaiq(mrn)