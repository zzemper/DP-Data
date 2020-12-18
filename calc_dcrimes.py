import sqlite3
import matplotlib
import matplotlib.pyplot as plt
import numpy as np #used for calculating trendlines
import os

def access_database(db_name):
    '''
    This function takes in a db_file and creates the database named crime.db,  
    which will be used to store all the data. This function also allows
    us to access the data.
    '''
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path + '/' + db_name)
    cur = conn.cursor()
    return cur, conn

def crime_by_precinct(cur,conn):
    '''
    returns the total crimes per precinct, police obstruction by precinct, and complaints per precinct.
    '''
    precinct_name_list = []
    unit_crime_counts_tuplist = []
    unit_police_crime_counts_tuplist = []
    unit_complaints_tuplist = []
    for i in range(2,13):
        #get total crimes for each precinct
        cur.execute("SELECT charge FROM All_Detroit_Crimes WHERE unit_id = ?", (i,))
        precinct_crime_tuplist = cur.fetchall()
        #get total charges of police obstruction by precinct
        count = 0
        for charge in precinct_crime_tuplist:
            if charge[0] == "OBSTRUCTING POLICE":
                count += 1

        #get total citizen complaints by precinct 
        cur.execute('SELECT id FROM Citizen_Complaints WHERE unit = ?', (i,))
        complaint_counts = cur.fetchall()

        precinct_name_list.append(i)
        unit_crime_counts_tuplist.append(len(precinct_crime_tuplist))
        unit_police_crime_counts_tuplist.append(count)
        unit_complaints_tuplist.append(len(complaint_counts))

    return(precinct_name_list, unit_crime_counts_tuplist, unit_police_crime_counts_tuplist, unit_complaints_tuplist)
        
def precinct_bar_viz(precincts, totals, obstruction, complaints):
    
    
    # data to plot
    n_groups = len(precincts)    
    # create plot
    fig, ax = plt.subplots()
    index = np.arange(n_groups)
    bar_width = 0.35
    opacity = 0.8
    
    rects1 = plt.bar(index, totals, bar_width,
    alpha=opacity,
    color='g',
    label='Total 2019 Crimes')
    
    rects2 = plt.bar(index + bar_width, obstruction, bar_width,
    alpha=opacity,
    color='purple',
    label='Arrests for "Obstructing the Police"')

    rects3 = plt.bar(index + bar_width + bar_width, complaints, bar_width,
    alpha=opacity,
    color='b',
    label='Citizen Complaints Against the Police')
    
    plt.xlabel('Police Precincts')
    plt.ylabel("Counts")
    plt.title("Counts of Total 2019 Crimes, Charges for Obstructing the Police, and Citizen Complaints \n Against the Police, by Detroit Police Precinct")
    plt.xticks(index + bar_width, precincts, rotation=90, fontsize=6,)
    plt.legend()
    
    #plt.tight_layout()
    plt.show()


def precinct_bar_viz_no_totals(precincts, obstruction, complaints):
    # data to plot
    n_groups = len(precincts)    
    # create plot
    fig, ax = plt.subplots()
    index = np.arange(n_groups)
    bar_width = 0.35
    opacity = 0.8
    
    rects1 = plt.bar(index, obstruction, bar_width,
    alpha=opacity,
    color='r',
    label='Arrests for "Obstructing the Police"')

    rects2 = plt.bar(index + bar_width, complaints, bar_width,
    alpha=opacity,
    color='b',
    label='Citizen Complaints Against the Police')
    
    plt.xlabel('Police Precincts')
    plt.ylabel("Counts")
    plt.title("Counts of 2019 Charges for Obstructing the Police, and Citizen Complaints \n Against the Police, by Detroit Police Precinct")
    plt.xticks(index + bar_width, precincts, rotation=90, fontsize=6,)
    plt.legend()
    
    #plt.tight_layout()
    plt.show()

def setup_total_pie_viz(cur,conn):
    #grab counts of each type of finding from complaints table
    findings_list = ["Admin. Closure", "Exonerated", "Inconclusive", "No Charge", "Sustained", "Unfounded", "Void"]
    findings_counts = []
    for finding in findings_list:
        cur.execute("SELECT id FROM Citizen_Complaints WHERE finding = ?", (finding,))
        findings_counts.append(len(cur.fetchall()))
    return (findings_list, findings_counts)


def complaints_pie_viz(cur, conn, labels, sizes):
    '''
    Makes a pie chart of the outcomes of all 2019 citizen complaints.
    '''
    #cur.execute('SELECT COUNT(*) FROM Citizen_Complaints')
    #row_count_c = cur.fetchone()[0]

    colors = ['lightskyblue', 'lightcoral', 'yellowgreen', 'gold', 'pink', 'red', 'magenta']

    plt.figure()
    plt.subplot(121)
    plt.title("2019 Citizen Complaints Against Detroit Police Findings")
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors)
    plt.axis('equal')

    plt.tight_layout(w_pad=-5)
    plt.show()

def setup_race_pie_viz(cur,conn,race):
    #grab findings for each race
    cur.execute("SELECT finding FROM Citizen_Complaints WHERE ctzn_race = ?", (race,))
    race_tuplist = cur.fetchall()
    #change tuple list into a regular list
    race_list = []
    for finding in race_tuplist:
        race_list.append(finding[0])
    #get the frequencies of each finding type
    race_dict = {}
    for finding in race_list:
        race_dict[finding] = race_dict.get(finding, 0) + 1
    #if a finding type isn't in the data put a 0 in for it in frequencies
    findings_list = ["Admin. Closure", "Exonerated", "Inconclusive", "No Charge", "Sustained", "Unfounded", "Void"]
    for finding in findings_list:
        if finding not in race_dict:
            race_dict[finding] = 0
    sorted_findings = sorted(race_dict.items())
    labels = []
    sizes = []
    for tup in sorted_findings:
        labels.append(tup[0])
        sizes.append(tup[1])

    return ((len(race_list), labels, sizes))

def setup_sex_pie_viz(cur,conn,sex):
    #grab findings for each sex
    cur.execute("SELECT finding FROM Citizen_Complaints WHERE ctzn_sex = ?", (sex,))
    sex_tuplist = cur.fetchall()
    sex_list = []
    #change tuple list into a regular list
    for finding in sex_tuplist:
        sex_list.append(finding[0])
    #get the frequencies of each finding type
    sex_dict = {}
    for finding in sex_list:
        sex_dict[finding] = sex_dict.get(finding, 0) + 1

    sorted_findings = sorted(sex_dict.items())
    labels = []
    sizes = []
    for tup in sorted_findings:
        labels.append(tup[0])
        sizes.append(tup[1])

    return ((len(sex_list), labels, sizes))

def complaints_by_minority_pie_viz(cur, conn, minority1, counts1, labels1, sizes1, minority2, counts2, labels2, sizes2):
    '''
    Makes a pie chart of the outcomes of all 2019 citizen complaints.
    '''

    colors = ['lightskyblue', 'lightcoral', 'yellowgreen', 'gold', 'pink', 'red', 'magenta']

    plt.figure()
    plt.subplot(121)
    plt.title("2019 " + minority1 + " Citizen Complaints Against \n Detroit Police Findings \n From: " + str(counts1) + " Reports" )
    plt.pie(sizes1, labels=labels1, autopct='%1.1f%%', colors=colors)
    plt.axis('equal')

    plt.subplot(122)
    plt.title("2019 " + minority2 + " Citizen Complaints Against \n Detroit Police Findings \n From: " + str(counts2) + " Reports")
    plt.pie(sizes2, labels=labels2, autopct='%1.1f%%', colors=colors)
    plt.axis('equal')

    plt.tight_layout(w_pad=-5)
    plt.show()    

    
    
   

def main():
    '''
    This function sets up the database.
    '''
    # SETUP DATABASE AND TABLE
    cur, conn = access_database('detroit_crime.db')

    #bar graphs with precinct data 
    #tuplist = crime_by_precinct(cur,conn)
    #precinct_bar_viz(tuplist[0], tuplist[1], tuplist[2], tuplist[3])
    #precinct_bar_viz_no_totals(tuplist[0], tuplist[2], tuplist[3])

    #Totals pie chart
    #values = setup_total_pie_viz(cur,conn)
    #complaints_pie_viz(cur, conn, values[0], values[1])

    #findings by race pie chart
    pie1 = setup_race_pie_viz(cur,conn, "Asian")
    pie2 = setup_race_pie_viz(cur,conn, "White")
    complaints_by_minority_pie_viz(cur,conn, "Asian", pie1[0], pie1[1], pie1[2], "White", pie2[0], pie2[1], pie2[2])

    #findings by sex pie chart
    #pie3 = setup_sex_pie_viz(cur,conn, "Female")
    #pie4 = setup_sex_pie_viz(cur,conn, "Male")
    #complaints_by_minority_pie_viz(cur,conn, "Female", pie3[0], pie3[1], pie3[2], "Male", pie4[0], pie4[1], pie4[2])


if __name__ == "__main__":
    main()