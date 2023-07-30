#Python 3.10
#Selenium 4.10.0
#2048 Player

#Importing modules
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import random

#Starting driver and opening web page.
driver = webdriver.Firefox()
action = ActionChains(driver)
driver.get("https://play2048.co/")

#Making driver wait to allow page to load.
driver.implicitly_wait(30)

#Values to later be used to break out of the loop if the game is over or get stuck.
matrix_t = []
qc = 0

#Game play loop.
while True:
    #Allowing time before moves.
    driver.implicitly_wait(10)
    #Getting data from the current board.
    element = driver.find_element(By.CLASS_NAME, "tile-container")

    element0 = element.get_attribute("outerHTML")
    #Removing un-needed data.
    element1 =element0[33:]
    #Splitting cell data into individual strings.
    element2 = element1.split("<div ")
    #Data is duplicated. Removing duplicates.
    element3 = element2[::2]

    #Merge tiles have both the actual tile data and the data for the two tiles that merged to make it.
    #This is the beginning of the process of removing those data of the two merged tiles. First locate which tiles are merged tiles.
    merge_index = []
    for i in range(len(element3)):
        if 'merged' in element3[i]:
            merge_index.append(i)
        else:
            pass
    #The two extra tiles are always two above the merged tile, so this is findding their locations.
    remove_index = []

    for v in merge_index:
        remove_index.append(v-1)
        remove_index.append(v-2)
    #This is removing the excess merge strings from the data.
    index3 = []

    for i in range(len(element3)):
        index3.append(i)

    for i in remove_index:
        index3.remove(i)

    element4 = []

    for i in index3:
        element4.append(element3[i])

    #Creating matrix of the current board.
    matrix0 = [['a', 'b', 'c', 'd'], ['e', 'f', 'g', 'h'], ['i', 'j', 'k', 'l'], ['n', 'o', 'p', 'q']]

    matrix1 = matrix0

    for v in element4:
        temp1 = v
        temp1 = temp1.split(' ')
        value1 = temp1[1][5:]
        index1 = int(temp1[2][14]) - 1
        index2 = int(temp1[2][16]) - 1
        matrix1[index2][index1] = value1
    #Creating the horizontal matrix of the current board.
    matrix_h = [[], [], [], []]

    for v in element4:
        temp1 = v
        temp1 = temp1.split(' ')
        value1 = temp1[1][5:]
        index2 = int(temp1[2][16]) - 1
        matrix_h[index2].append(value1)
    # Creating the lateral matrix of the current board.
    matrix_l = [[], [], [], []]

    for v in element4:
        temp1 = v
        temp1 = temp1.split(' ')
        value1 = temp1[1][5:]
        index2 = int(temp1[2][14]) - 1
        matrix_l[index2].append(value1)
    #Counitng how many matches the horizontal axis has.
    h_score = 0

    for v in matrix_h:
        if len(v) < 2:
            pass
        elif len(v) == 2:
            if v[0] == v[1]:
                h_score += 1
            else:
                pass
        elif len(v) == 3:
            if v[0] == v[1]:
                h_score += 1
            elif v[1] == v[2]:
                h_score += 1
            else:
                pass
        elif len(v) == 4:
            if v[0] == v[1]:
                h_score += 1
                if v[2] == v[3]:
                    h_score += 1
                else:
                    pass
            elif v[1] == v[2]:
                h_score += 1
            elif v[2] == v[3]:
                h_score += 1
            else:
                pass
    # Counitng how many matches the lateral axis has.
    l_score = 0

    for v in matrix_l:
        if len(v) < 2:
            pass
        elif len(v) == 2:
            if v[0] == v[1]:
                l_score += 1
            else:
                pass
        elif len(v) == 3:
            if v[0] == v[1]:
                l_score += 1
            elif v[1] == v[2]:
                l_score += 1
            else:
                pass
        elif len(v) == 4:
            if v[0] == v[1]:
                l_score += 1
                if v[2] == v[3]:
                    l_score += 1
                else:
                    pass
            elif v[1] == v[2]:
                l_score += 1
            elif v[2] == v[3]:
                l_score += 1
            else:
                pass
    #Determining if which axis move will cause the most merges. If equal, random move.
    if h_score > l_score:
        action.send_keys(Keys.ARROW_LEFT).perform()


    elif h_score < l_score:
        action.send_keys(Keys.ARROW_UP).perform()


    else:
        x = random.randint(0, 2)
        if x == 0:
            action.send_keys(Keys.ARROW_LEFT).perform()
        elif x == 1:
            action.send_keys(Keys.ARROW_RIGHT).perform()
        elif x == 2:
            action.send_keys(Keys.ARROW_DOWN).perform()
        else:
            action.send_keys(Keys.ARROW_UP).perform()


#Counter to see if the game is stuck or over. Will break out of loop if either occur.
    if matrix_l == matrix_t:
        qc += 1

    elif matrix_l != matrix_t:
        qc = 0

    else:
        pass

    if qc > 20:
        break

    else:
        pass



    matrix_t = matrix_l

print("Game over")