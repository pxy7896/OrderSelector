# -*- coding:utf-8 -*-
''' A parser for raw xlsx data.
By Xiaoyi Pang <pangxiaoyi@genscript.com>,
Copyright @ 2018, All Rights Reserved.
'''

import pandas as pd
import os
import sys
import SingleTest
import string
import random
import datetime
from shutil import copyfile
from shutil import rmtree


def test_get_plate_id(dataDir):
    outFile = open("plateID.txt", "w")
    #print os.listdir(dataDir)
    for file in os.listdir(dataDir):
        if os.path.splitext(file)[1] == '.csv':
            with open(dataDir + "/" + file, 'r', encoding='utf-8') as inFile:
                for line in inFile:
                    if line.find("Plate") != -1:
                        outFile.write(line.replace(',', ''))
    outFile.close()

          
def getLegalRecords(inFile):
    result = [] 
    curDir = os.getcwd()
    #workDir = "temp_" + id_generator() 
    i = datetime.datetime.now()
    workDir = "temp_" + str(i.hour) + str(i.minute)
    if workDir in os.listdir(os.getcwd()):
        rmtree(workDir)
    else:
        os.mkdir(workDir)
        os.chdir(workDir)
#    print(inFile)
    inFile = inFile.lstrip().rstrip()
    # get all sheets
    data_xls = pd.read_excel(inFile, sheet_name=None)
    name = os.path.splitext(inFile)[0].split("\\")[-1]
    # separate files for each sheet
    #print(name)
    for i in data_xls.keys():
        # for windows
        data_xls[i].to_csv(name + "." + str(i) + ".csv", encoding='utf-8', index=False)
    test_get_plate_id(os.getcwd())
    outFile = open("legal_data.txt", "a+")
    illegalFile = open("illegal_data.txt", "w")
    for file in os.listdir(os.getcwd()):
        if os.path.splitext(file)[1] == '.csv':
            # for previous plate info
            header = "X"
            #illegal = False
            with open(file, 'r', encoding='utf-8') as file1:
                # temporarily keep data of a plate
                tempList = []
                for line in file1:
                    if line.find("Results") != -1 or (line.find("Plate") == -1 and line.find("Unnamed") != -1):
                        continue
                    if line.find("Plate") != -1:
                        #info = line.split("Wavelength")[0].split("Plate:")[1].split()
                        #print(line.strip(r","))
                        #tmp_info = line.rstrip().strip(r",").split("Plate:")[1].split()
                        tmp_info = line.split("Unnamed")[0].rstrip().strip(",").rstrip().split("Plate:")[1].split()
                        #print(tmp_info)
                        if len(tmp_info) != 5:
                            tempHead = "#".join(tmp_info)
                            #print(tempHead)
                            #illegal = True
                        else:
                            #print(tmp_info)
                            order, group, name, plate, day = tmp_info
                            tempHead = "#".join([order, group, name, day, plate])
                            #illegal = False
                                
                        if len(tempList) == 96:
                            if len(header.split("#")) == 5:
                                s = SingleTest.SingleTest()
                                #print("in-"+header+"*")
                                s.createByList(header.split("#") + [float(i) for i in tempList])
                                s.printPlate(file=outFile)
                                result.append(s)
                            else:
                                #print("len(head)<5=="+header)
                                illegalFile.write(",".join(header.split("#")) + "\n")
                                SingleTest.printSourceList(li=tempList, file=illegalFile)
                        elif len(tempList) > 0:
                            #print("len(tempList)<96=="+header+"=="+str(len(tempList)))
                            illegalFile.write(",".join(header.split("#")) + "\n")
                            SingleTest.printSourceList(li=tempList, file=illegalFile)
                        else:
                            pass
                        header = tempHead
                        tempList = []
                      
                    else:
                        temp = line.replace(","," ").split()
                        if len(temp) < 12:
                            tempList += temp
                            continue
                        else:
                            tempList += temp[:12]
                # process last plate
                if len(tempList) == 96:
                    if len(header.split("#")) == 5:
                        s = SingleTest.SingleTest()
                        #print("last-"+header+"*")
                        s.createByList(header.split("#") + [float(i) for i in tempList])
                        s.printPlate(file=outFile)
                        result.append(s)
                    else:
                        illegalFile.write(",".join(header.split("#")) + "\n")
                        SingleTest.printSourceList(li=tempList, file=illegalFile)
                else:
                    illegalFile.write(",".join(header.split("#")) + "\n")
                    SingleTest.printSourceList(li=tempList, file=illegalFile)

    illegalFile.close()
    outFile.close()
    #os.system("cp legal_data.txt " + curDir + "/legal_data.txt" )
    copyfile("legal_data.txt", curDir + "/legal_data.txt")
    copyfile("illegal_data.txt", curDir + "/illegal_data.txt")
    os.chdir(curDir)
    rmtree(workDir)
    #print len(result)
    return result

# find single plate by order#, group# and plate#
def getSinglePlate(result, order, group, plate):
    for i in result:
        if i.order == order and i.group == group and i.plate == plate:
            return i
    return False

# get a plates within same order and same group
def getGroupPlate(result, order, group):
    temp = []
    for i in result:
        if i.order == order and i.group == group:
            temp.append(i)
    return temp
                        


    
