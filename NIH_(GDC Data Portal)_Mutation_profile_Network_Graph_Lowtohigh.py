#NIH (GDC Data Portal) Mutation Profile Network Graph Generator Low to High Mutation Count.
#This module buildes the network graph from the case with the fewest mustations to the one with the most.
#It is matching cases with the other case(s) that share the most mutations with.
#Python 3.10
#Linux
#Anthony Stillman
#Imports
#selenium 4.10.0
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import time
import os
import json
import re
#pandas 2.0.3
import pandas as pd
#pyvis 0.3.2
from pyvis.network import Network
import random

#Create Desktop Folder to save raw data and processed data.
def folder_creation():
    print("Please enter the directory (ex: /home/user/Desktop) for the a folder the raw data and processed data will be stored.")
    cdir = input("Enter Directory:")
    os.chdir(cdir)
    dir = os.path.join(cdir, "test_file")
    if not os.path.exists(dir):
        os.mkdir(dir)
    dir2 = os.path.join(cdir, "test_file", "Analyzed_Data")
    if not os.path.exists(dir2):
        os.mkdir(dir2)
    dir3 = os.path.join(cdir, "test_file", "Raw_Data")
    if not os.path.exists(dir3):
        os.mkdir(dir3)
    dir_list = []
    dir_list.append(dir)
    dir_list.append(dir2)
    dir_list.append(dir3)
    return dir_list

#Open page and accepting terms.
def openpage():
    print("""Go to GDC Data Portal Exploration: "
          "https://portal.gdc.cancer.gov/exploration?filters=%7B%22content%22%3A%5B%7B%22content%22%3A%7B%22field%22%3A%22genes.is_cancer_gene_census%22%2C%22value%22%3A%5B%22true%22%5D%7D%2C%22op%22%3A%22in%22%7D%5D%2C%22op%22%3A%22and%22%7D"
          "Select Primary Site of cancer."
          "Change Show entries at the bottom of the page"
          "In the URL, there should be 'cases_size='. Change the number to number of cases to put them all on the same page"
          "copy the current URL and paste it into the input:""")
    website = input("Paster here:")
    driver = webdriver.Firefox()
    driver.get(website)
    print("Wait 30 seconds. Loading...")
    time.sleep(30)
    driver.find_element(by=By.XPATH, value="//button[@data-test='modal-cancel-button']").click()
    return driver

#Finding all the links to cases mutations lists.
def get_case_link(driver):
    elems = driver.find_elements(by=By.XPATH, value="//a[@class = 'test-mutations-count active']")
    links = [elem.get_attribute('href') for elem in elems]
    print("Links to mutations found.")
    driver.close()
    return links

#Open links and download JSON mutations files for each case into Raw_Data subfolder.
def download_json(links):
    for link in links:
        options = Options()
        options.set_preference("browser.download.folderList", 2)
        options.set_preference("browser.download.manager.showWhenStarting", False)
        options.set_preference("browser.download.dir", dir_list[2])
        options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/x-gzip")
        driver = webdriver.Firefox(options=options)
        driver.get(link)
        print("Wait 30 seconds. Loading...")
        time.sleep(30)
        driver.find_element(by=By.XPATH, value="//button[@data-test='modal-cancel-button']").click()
        time.sleep(10)
        driver.find_element(by=By.XPATH, value="//button[@class='test-download-button button css-1alfshc']").click()
        time.sleep(30)
        driver.close()
#Giving each file a unique ID.
def name_files():
    folder = dir_list[2]
    for count, filename in enumerate(os.listdir(folder)):
        dst = f"{str(count).rjust(6, '0')}.json"
        src = f"{folder}/{filename}"
        dst = f"{folder}/{dst}"
        os.rename(src, dst)

#Making a JSON file that is blank
def health_cell():
    folder = dir_list[2]
    os.chdir(folder)
    dictionary = {
        " ": " "
    }
    json_object = json.dumps(dictionary, indent=4)
    with open("healthy_cell.json", "w") as outfile:
        outfile.write(json_object)

#Matching cases, building Excel and Network graph.
def match_maker():
    #Extracting mutation profiles from downloaded files.
    folder = dir_list[2]
    os.chdir(folder)
    dict_list = {}
    dict_string = {}
    for file in os.listdir():
        f = open(file, 'r')
        data = str(json.load(f))
        string_pattern =  r"'symbol': '[^']*"
        regex_pattern = re.compile(string_pattern)
        result = regex_pattern.findall(data)
        m_list = []
        for value in result:
            value1 = value.split("'")
            m_list.append(value1[3])
        m_list = list(set(m_list))
        dict_list[str(file[:-5])] = m_list
        m_string = ", ".join(m_list)
        dict_string[str(file[:-5])] = m_string
        f.close()
    #Finding best matches for cases based on similiarity of mutation profile.
    dict_match = {}
    for k1 in dict_list.keys():
        fract1 = 0
        match_list = []
        for k2 in dict_list.keys():
            if len(dict_list[k1]) >= len(dict_list[k2]):
                pass
            elif len(dict_list[k1]) < len(dict_list[k2]):
                fract2 = len(set(dict_list[k1]) & set(dict_list[k2])) / len(dict_list[k2])
                if fract2 == fract1:
                    match_list.append(k2)
                elif fract2 > fract1:
                    match_list.clear()
                    match_list.append(k2)
                else:
                    pass
            else:
                pass

        dict_match[k1] = match_list
    #Creating index that will be used to track cases in Network graph.
    index = 0
    ref_index = {}
    for k3 in dict_match.keys():
        ref_index[k3] = index
        index += 1
    #Turning matches from cases into their assocatied index.
    match_index = {}
    for k4 in dict_match.keys():
        temp_v = []
        for x in dict_match[k4]:
            temp_v.append(ref_index[x])
        match_index[k4] = temp_v
    #Turning data into string, so the can better fit in dataframe.
    match_index_string = {}
    for k5 in match_index.keys():
        match_index_string[k5] = " ,".join(str(i) for i in match_index[k5])
    dict_match_string = {}
    for k6 in dict_match.keys():
        dict_match_string[k6] = " ,".join(str(i) for i in dict_match[k6])
    dataframe_dict = {}
    for k7 in dict_string.keys():
        temp_data = []
        temp_data.append(dict_string[k7])
        temp_data.append(match_index_string[k7])
        temp_data.append(dict_match_string[k7])
        temp_data.append(ref_index[k7])
        dataframe_dict[k7] = temp_data
    #Creating Data frame and excel.
    df1 = pd.DataFrame.from_dict(dataframe_dict, orient='index', columns=['Mutated Genes', 'Match Index', 'Matches', 'Index'])
    os.makedirs(dir_list[1], exist_ok=True)
    df1.to_excel(dir_list[1] + "/dataframe.xlsx")
    #Creating network graph.
    os.chdir(dir_list[1])
    label_number = []
    net_numbers = []
    for k8, v1 in ref_index.items():
        label_number.append(k8)
        net_numbers.append(v1)

    number_of_colors = len(net_numbers)

    color = ["#" + ''.join([random.choice('0123456789ABCDEF') for j in range(6)])
             for i in range(number_of_colors)]

    net = Network(notebook=True, cdn_resources="remote", select_menu=True, filter_menu=True)
    net.add_nodes(net_numbers, label=label_number, color=color)
    net.show_buttons(filter_="physics")
    for k9 in ref_index.keys():
        for i in match_index[k9]:
            net.add_edge(ref_index[k9], i)

    net.show("Node_test.html")
    #Showing forms of data.
    print(dict_list)
    print(dict_string)
    print(dict_match)
    print(ref_index)
    print(match_index)
    print(match_index_string)
    print(dict_match_string)
    print(dataframe_dict)
    print(df1)
    print(label_number)
    print(net_numbers)
    print(color)




#Running modules in sequence.
dir_list = folder_creation()
download_json(get_case_link(openpage()))
name_files()
#health_cell()
match_maker()

