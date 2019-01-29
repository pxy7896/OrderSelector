# -*- coding:utf-8 -*-
''' Main body of the whole pipeline.
By Xiaoyi Pang <pangxiaoyi@genscript.com>,
Copyright @ 2019, All Rights Reserved.
'''

#import pandas as pd
import os
import sys
import RawParser
import SingleTest


if __name__ == '__main__':
    print("\nWelcome to OrderHelper!\n")
    inputPath = input("Please input raw data file path: ")
    legalRecords = RawParser.getLegalRecords(inputPath)
    #curDir = os.getcwd()
    #dataDir = curDir + "/../data"
    #legalRecords = RawParser.getLegalRecords(curDir + "/../data/data.xlsx", dataDir)

    while input("\nPress q to quit or press c to continue\n") != "q":
        choice = input("Press 1 for within group, 2 for between group, 3 for search.\n")
        if choice == "1":
            while input("\nPress q to quit in-group operations or press c to continue\n") != 'q':
                order = input("\nInput order number: ")
                group = input("\nInput group number: ")
                plate = input("\nInput plate number or press a for all: ")
                if plate == 'a':
                    temp = RawParser.getGroupPlate(legalRecords, order=order, group=group)
                    if len(temp) == 0:
                        print("\nIllegal order or group number. Please check legal_data.txt for available records!\n")
                        continue
                    else:
                        outFile = input("\nPlease input file name for writing results: ")
                        op = input("\nInput formula like : gt 1\n").split()
                        resultFile = open(outFile, "w+")
                        resultFile.write(" ".join([str(order), str(group)] + op)+"\n")
                        result = []
                        time = temp[0].date
                        for i in temp:
                            if i.date != time:
                                resultFile.write(str(time) + "\n")
                                SingleTest.printSourceList(li=result, file=resultFile)
                                result = i.filterSinglePlate(op[0], op[1])
                                time = i.date
                            else:
                                result += i.filterSinglePlate(op[0], op[1])
                        resultFile.write(str(time) + "\n")
                        SingleTest.printSourceList(li=result, file=resultFile)
                        resultFile.close()

                else:
                    temp = RawParser.getSinglePlate(legalRecords, order, group, plate)
                    if temp == False:
                        print("Illegal plate. Please check legal_data.txt for available records!\n")
                        continue
                    else:
                        outFile = input("\nPlease input file name for writing results: ")
                        op = input("\nInput formula like : gt 1\n").split()
                        temp.modifySingplePlateSource(temp.filterSinglePlate(op[0], op[1]))
                        resultFile = open(outFile, "w+")
                        resultFile.write(" ".join([str(order), str(group)] + op)+"\n")
                        temp.printPlate(file=resultFile)
                        resultFile.close()
        # Calculations between groups
        elif choice == "2":
            order = input("\nInput order number: ")
            op = input("\nInput formula like : 'A gt 1 and D lt 1' or 'A sub D gt 0.5' \n")
            outFile = input("\nPlease input file name for writing results or blank to print here: ")
            result = []
            if 'and' in op.split():
                tmp_expr = op.split('and')
                pre_tmp_result = []
                flag = False
                for item in tmp_expr:
                    group, operator, val = item.split()
                    tmp_result = SingleTest.filterGroupPlates(SingleTest.findPlateGroup(legalRecords, order, group), operator, val)
                    if flag == False:
                        pre_tmp_result = tmp_result
                        flag = True
                        continue
                    else:
                        pre_tmp_result = list(set(tmp_result).intersection(set(pre_tmp_result)))
                result = list(set(pre_tmp_result))
            else:
                info = op.split()
                group1 = SingleTest.findPlateGroup(legalRecords, order, info[0])
                group2 = SingleTest.findPlateGroup(legalRecords, order, info[2])
                result = SingleTest.calTwoGroups(group1, group2, info[1], info[3], info[4])

            if len(outFile) < 3:
                print("\nOrder: " + order + " " + op + "\n")
                print(" ".join(result) + "\n")
            else:
                resultFile = open(outFile, "w+")
                resultFile.write("Order: " + order + " " + op + "\n")
                resultFile.close()
                SingleTest.printSourceList(result, file=resultFile)
        # Search
        elif choice == "3":
            field = input("\nPlease input: o/n/d. o - search by Order number, n - search by Name, d - search by date\n")
            outFile = input("\nPlease input file name for writing results or blank to print here: ")
            val = input("\nSearch: ")
            result, raw = SingleTest.searchAvailablePlates(legalRecords, field, val)
            if len(outFile) < 3:
                print("\n")
                print(result)
                print("\n")
                print("\n".join(raw))
            else:
                resultFile = open(outFile, "w+")
                resultFile.write(result)
                resultFile.write("\n".join(raw))
                resultFile.close()
        else:
            continue

    print("Bye!\n")
