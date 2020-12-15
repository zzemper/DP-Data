import requests
import json
import sqlite3
import os
import csv 

def create_database(db_file):
    '''
    This function takes in a db_file and creates the database named crime.db,  
    which will be used to store all the data. 
    '''
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_file)
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS Unit_Lookup (id INTEGER, name TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS Citizen_Complaints (id INTEGER, unit INTEGER, ctzn_age TEXT, ctzn_race TEXT, ctzn_sex TEXT, allegation TEXT, finding TEXT, ofcr_race TEXT, ofcr_sex TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS All_Detroit_Crimes (crime_id INTEGER, unit_id INTEGER, charge TEXT)")
    return cur, conn

def read_json(JSON_FNAME):
    """
    This function reads from the JSON cache file and returns a dictionary from the cache data.
    If the file doesn’t exist, it returns an empty dictionary.
    """
    dir_path = os.path.dirname(os.path.realpath(__file__))
    JSON_FNAME = dir_path + '/' + "DPD_Citizen_Complaints.json"
    try:
        cache_file = open(JSON_FNAME, 'r', encoding="utf-8") # Try to read the data from the file
        cache_contents = cache_file.read()  # If it's there, get it into a string
        CACHE_DICTION = json.loads(cache_contents) # And then load it into a dictionary
        cache_file.close() # Close the file, we're good, we got the data in a dictionary.
        return CACHE_DICTION
    except:
        CACHE_DICTION = {}
        return CACHE_DICTION

def unit_calculator(unit_raw):
    if unit_raw == "UNKNOWN COMMAND":
        unit = 0
    elif unit_raw[:4] == "VICE":
        unit = 1
    elif unit_raw[:3] == "ABA":
        unit = 13
    elif unit_raw[:3] == "ARS":
        unit = 14
    elif unit_raw[:5] == "ASSET":
        unit = 15
    elif unit_raw[:3] == "AUT":
        unit = 16
    elif unit_raw[:3] == "CEA":
        unit = 17
    elif unit_raw[:3] == "CEN":
        unit = 18
    elif unit_raw[:4] == "CITY":
        unit = 19
    elif unit_raw[:3] == "COM":
        unit = 20
    elif unit_raw[:4] == "CRIM":
        unit = 21
    elif unit_raw[:9] == "DETROIT D":
        unit = 22
    elif unit_raw[:9] == "DETROIT F":
        unit = 23
    elif unit_raw[:9] == "DETROIT P":
        unit = 24
    elif unit_raw[:3] == "DOM":
        unit = 25
    elif unit_raw[:3] == "DOW":
        unit = 26
    elif unit_raw[:4] == "EXEC":
        unit = 27
    elif unit_raw[:5] == "FATAL":
        unit = 28
    elif unit_raw[:5] == "FIREA":
        unit = 29
    elif unit_raw[:5] == "FLEET":
        unit = 30
    elif unit_raw[:4] == "FORF":
        unit = 31
    elif unit_raw[:3] == "FUG":
        unit = 32
    elif unit_raw[:3] == "GAM":
        unit = 33
    elif unit_raw[:3] == "GAN":
        unit = 34
    elif unit_raw[:3] == "GEN":
        unit = 35
    elif unit_raw[:4] == "HARB":
        unit = 36
    elif unit_raw[:4] == "HEAD":
        unit = 37
    elif unit_raw[:3] == "HOM":
        unit = 38
    elif unit_raw[:3] == "INT":
        unit = 39
    elif unit_raw[:3] == "INV":
        unit = 40
    elif unit_raw[:3] == "JUN":
        unit = 41
    elif unit_raw[:7] == "MAJOR C":
        unit = 42
    elif unit_raw[:7] == "MAJOR V":
        unit = 43
    elif unit_raw[:7] == "MOUNTED":
        unit = 44
    elif unit_raw[:3] == "NAR":
        unit = 45
    elif unit_raw[:11] == "OFFICE OF P":
        unit = 46
    elif unit_raw[:11] == "OFFICE OF T":
        unit = 47
    elif unit_raw[:3] == "ORG":
        unit = 48
    elif unit_raw[:4] == "PROP":
        unit = 49
    elif unit_raw[:3] == "REC":
        unit = 50
    elif unit_raw[:3] == "SEC":
        unit = 51
    elif unit_raw[:3] == "SEX":
        unit = 52
    elif unit_raw[:9] == "SPECIAL R":
        unit = 53
    elif unit_raw[:9] == "SPECIAL V":
        unit = 54
    elif unit_raw[:3] == "TAC":
        unit = 55
    elif unit_raw[:4] == "TASK":
        unit = 56
    elif unit_raw[:3] == "TEL":
        unit = 57
    elif unit_raw[:4] == "TRAF":
        unit = 58
    elif unit_raw[:5] == "TRAIN":
        unit = 59
    elif unit_raw[:2] == "10":
        unit = 10
    elif unit_raw[:2] == "11":
        unit = 11
    elif unit_raw[:2] == "12":
        unit = 12
    else:
        unit = int(unit_raw[0])

    return unit

def create_unit_lookup_table(cur,conn):
    
    unit_list = ['UNKNOWN COMMAND' ,'VICE ENFORCEMENT','2ND PRECINCT' ,'3RD PRECINCT' ,'4TH PRECINCT' ,'5TH PRECINCT' ,'6TH PRECINCT' ,'7TH PRECINCT' ,'8TH PRECINCT' ,'9TH PRECINCT' ,'10TH PRECINCT' ,'11TH PRECINCT' ,'12TH PRECINCT','ABANDONED VEHICLE TASK FORCE' ,'ARSON' ,'ASSETS AND LICENSING' ,'AUTO THEFT' ,'CEASE FIRE' ,'CENTRAL DISTRICT' ,'CITYWIDE PARK UNIT' ,'COMMUNICATIONS OPERATIONS' ,'CRIME SCENE SERVICES' ,'DETROIT DETENTION CENTER' ,'DETROIT FUGITIVE APREHENSION TEAM' ,'DETROIT POLICE DEPARTMENT' ,'DOMESTIC VIOLENCE' ,'DOWNTOWN SERVICES' ,'EXECUTIVE PROTECTION' ,'FATAL SQUAD' ,'FIREARMS INVESTIGATIVE UNIT' ,'FLEET MANAGEMENT' ,'FORFEITURE SECTION' ,'FUGITIVE APPREHENSION TEAM' ,'GAMING ADMINISTRATION' ,'GANG INTELLIGENCE' ,'GENERAL ASSIGNMENT UNIT' ,'HARBORMASTER UNIT' ,'HEADQUARTERS SURVEILLANCE' ,'HOMICIDE' ,'INTERNAL AFFAIRS' ,'INVESTIGATIVE OPERATIONS DIVISION' ,'JUNIOR POLICE CADETS' ,'MAJOR CRIMES DIVISION' ,'MAJOR VIOLATORS' ,'MOUNTED' ,'NARCOTICS ENFORCEMENT' ,'OFFICE OF PUBLIC INFORMATION' ,'OFFICE OF THE CHIEF INVESTIGATOR' ,'ORGANIZED CRIMES' ,'PROPERTY CONTROL' ,'RECORDS AND IDENTIFICATION' ,'SECONDARY EMPLOYMENT' ,'SEX CRIME UNIT' ,'SPECIAL RESPONSE TEAM' ,'SPECIAL VICTIMS UNIT' ,'TACTICAL SERVICES SECTION' ,'TASK FORCE ADMINISTRATION' ,'TELEPHONE CRIME REPORTING' ,'TRAFFIC ENFORCEMENT' ,'TRAINING']
    for i in range(60):
        cur.execute("INSERT INTO Unit_Lookup (id,name) VALUES(?,?)", (i,unit_list[i]))
        conn.commit()

def create_citizen_complaints_table(cur,conn):
    '''
    fills the table with all citizen complaint data
    '''
    #create statement for the table
    #cur.execute("DROP TABLE IF EXISTS Citizen_Complaints")
    
    #call read_json to get complaints json data into a dictionary
    dir_path = os.path.dirname(os.path.realpath(__file__))
    JSON_FNAME = dir_path + '/' + "DPD_Citizen_Complaints.json"
    complaints_dict = read_json(JSON_FNAME)
    
    #loop through complaints to  collect just the rows with 2019 data
    cdict_2019 = {}
    i = 0
    for complaint in complaints_dict["features"]:
        year = complaint["properties"]["Report_Date"][:4]
        if year == "2019":
            cdict_2019[i] = complaint["properties"]
            i += 1
    
    #add this 2019 complaint data to the database
    for key in cdict_2019:
        id = key
        unit_raw = cdict_2019[key]["Unit"]
        unit = unit_calculator(unit_raw)
        ctzn_age = cdict_2019[key]["Age"]
        ctzn_race = cdict_2019[key]["ctznRace"]
        ctzn_sex = cdict_2019[key]["ctznSex"]
        allegation = cdict_2019[key]["Allegation"]
        finding = cdict_2019[key]["Finding"]
        ofcr_race = cdict_2019[key]["ofcrRace"]
        ofcr_sex = cdict_2019[key]["ofcrSex"]

        cur.execute("INSERT INTO Citizen_Complaints (id,unit,ctzn_age,ctzn_race,ctzn_sex,allegation,finding,ofcr_race,ofcr_sex) VALUES (?,?,?,?,?,?,?,?,?)", (id,unit,ctzn_age,ctzn_race,ctzn_sex,allegation,finding,ofcr_race,ofcr_sex))

        conn.commit()
  


def create_all_detroit_crimes_table(cur,conn):
    #call read_json to get complaints json data into a dictionary
    dir_path = os.path.dirname(os.path.realpath(__file__))
    JSON_FNAME = dir_path + '/' + "DPD_Citizen_Complaints.json"
    crime_dict = read_json(JSON_FNAME)




def main():
    '''
    This function sets up the database and creates the entire State_Crimes table
    using create_database(db_file) and create_state_crime_counts_table(cur, conn, start, end, start_year),
    while limiting stored data to at most 25 rows at a time.
    '''
    # SETUP DATABASE AND TABLE
    cur, conn = create_database('detroit_crime.db')

    cur.execute('SELECT COUNT(*) FROM Unit_Lookup')
    row_count_u = cur.fetchone()[0]
    if row_count_u == 0:
        create_unit_lookup_table(cur, conn)

    cur.execute('SELECT COUNT(*) FROM Citizen_Complaints')
    row_count_c = cur.fetchone()[0]
    if row_count_c == 0:
        create_citizen_complaints_table(cur,conn)

    create_all_detroit_crimes_table(cur,conn)

if __name__ == "__main__":
    main()