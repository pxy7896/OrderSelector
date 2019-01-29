# -*- coding:utf-8 -*-
''' Class SingleTest implementation.
By Xiaoyi Pang <pangxiaoyi@genscript.com>,
Copyright @ 2018, All Rights Reserved.
'''

import sys
import re
from collections import Counter

class SingleTest:
    def __init__(self, order='', group='', name='', date='', plate='', source=[]):
        self.order = order
        self.group = group
        self.name = name
        self.date = date
        self.plate = plate
        self.source = source
            

    #@classmethod
    # plate = plate
    def assignPlate(self, other):
        self.order = other.order
        self.group = other.group
        self.name = other.name
        self.date = other.date
        self.plate = other.plate
        self.source = other.source
        

    # initiate by list
    def createByList(self, li=None):
        # pass list must make it a list
        li = list(li)
        #print li
        self.order, self.group, self.name, self.date, self.plate = li[0:5]
        self.source = li[5:]
        return

    # plate - plate
    def substractPlate(self, other):
        result = self.source
        for i in range(len(result)):
            result[i] = result[i] - other.source[i]
        return result

    # plate + plate
    def addPlate(self, other):
        result = self.source
        for i in range(len(result)):
            result[i] = result[i] + other.source[i]
        return result

    # operation on single plate
    def filterSinglePlate(self, operator, value):
        filterVal = float(value)
        result = []
        for i in range(len(self.source)):
            temp = self.source[i]
            if operator == "gt":
                if temp > filterVal:
                    result.append(i)
                    #print temp
            elif operator == "lt":
                if temp < filterVal:
                    result.append(i)
            elif operator == "eq":
                if temp == filterVal:
                    result.append(i)
            elif operator == "ge":
                if temp >= filterVal:
                    result.append(i)
            elif operator == "le":
                if temp <= filterVal:
                    result.append(i)
            else:
                #print "Illegal operator :)"
                continue
        # convert index to position
        temp = []
        for i in result:
            #print("*"+str(i))
            row = chr(ord('A') + int(int(i)/12))
            col = str(1 + int(int(i)%12))
            temp.append(str(self.plate) + row + col)
        return temp

    # modify source
    def modifySingplePlateSource(self, data):
        self.source = list(data)

    # human-readable print
    def printPlate(self, sep=",", file=sys.stdout):
        #print >> file, "\t".join([str(self.order), str(self.group), str(self.name), str(self.date), str(self.plate)])
        print(sep.join([str(self.order), str(self.group), str(self.name), str(self.date), str(self.plate)]),file=file)
        result = ""
        sep = sep
        for i in range(len(self.source)):
            if 'E' in str(self.source[i]):
                result += "'" + str(self.source[i]) + "'" + sep
            else:
                result += str(self.source[i]) + sep
            if i != 0 and i % 12 == 11:
                result += "\n"
        #print >> file, result
        print(result, file=file)
        return 



               
def printSourceList(li, sep=",", file=sys.stdout):
    li = list(li)
    result = ""
    sep = sep
    for i in range(len(li)):
        if 'E' in str(li[i]):
            result += "'" + str(li[i]) + "'" + sep
        else:
            result += str(li[i]) + sep
        if i != 0 and i % 12 == 11:
            result += "\n"
    #print >> file, result
    print(result, file=file)
    return

# search available plates
def searchAvailablePlates(li, field, val):
    raw = []
    result = ""
    li = list(li)
    # search by order number
    if field == "o":
        group = []
        people = []
        date = []
        plate = []
        for item in li:
            if item.order == val:
                info = "\t".join([str(item.order), str(item.group), str(item.name), str(item.date), str(item.plate)])
                raw.append(info)
                if item.group not in group:
                    group.append(item.group)
                if item.name not in people:
                    people.append(item.name)
                if item.date not in date:
                    date.append(item.date)
                plate.append(item.plate)
        if len(raw) == 0:
            result = "Please check legal_data.txt for available records!\n"
        else:
            result = "\n".join(["Order: "+val, "Group: "+str(len(group))+" "+str(group), "Operator: "+str(len(people))+" "+str(people), "Date: "+str(len(date))+" "+str(date), "Plate: "+str(len(plate))])
    # search by name abbreviation
    elif field == "n":
        order = []
        for item in li:
            if item.name == val:
                info = "\t".join([item.order, item.group, item.name, item.date, item.plate])
                raw.append(info)
                if item.order not in order:
                    order.append(item.order)
        if len(raw) == 0:
            result = "Please check legal_data.txt for available records!\n"
        else:
            result = "Name: " + val + "\n" + "Order: " + str(len(order)) + " " + str(order) + "\n" + "Plate: " + str(len(raw)) + "\n"
    # search by date 
    elif field == "d":
        order = []
        group = []
        people = []
        plate = []
        for item in li:
            if item.date == val:
                info = "\t".join([item.order, item.group, item.name, item.date, item.plate])
                raw.append(info)
                if item.order not in order:
                    order.append(item.order)
                if item.group not in group:
                    group.append(item.group)
                if item.name not in people:
                    people.append(item.name)
                plate.append(item.plate)
        if len(raw) == 0:
            result = "Please check legal_data.txt for available records!\n"
        else:
            result = "\n".join(["Date: "+val, "Order: "+str(len(order))+" "+str(order), "Group: "+str(len(group))+" "+str(group), "Operator: "+str(len(people))+" "+str(people), "Plate: "+str(len(plate))])
    else:
        pass
    return result, raw

# help find a group of plates
def findPlateGroup(li, order, group):
    li = list(li)
    result = []
    for item in li:
        if item.order == order and item.group == group:
            result.append(item)
    return result

def filterGroupPlates(li, op, val):
    li = list(li)
    # keep single plate filter results
    tmp = []
    result = []
    for item in li:
        tmp += item.filterSinglePlate(op, val)
    # remove plate number. only locations needed.
    tmp_dict = []
    for item in tmp:
        tmp_dict.append(item[re.search(r'^\d*',item).end():])
    tmp_dict = dict(Counter(tmp_dict))
    #print "# " + str(tmp_dict)
    for key, value in tmp_dict.items():
        if value == len(li):
            result.append(key)
    #print "* " + str(result)
    return result

def calTwoGroups(group1, group2, grp_op, op, val):
    group1 = list(group1)
    group2 = list(group2)
    result = []
    if grp_op == "sub":
        if op in ["gt", "ge"]:
            min_group1 = [100] * 96
            max_group2 = [0] * 96
            for i in range(len(group1)):
                for j in range(96):
                    if group1[i].source[j] < min_group1[j]:
                        min_group1[j] = group1[i].source[j]
            for i in range(len(group2)):
                for j in range(96):
                    if group2[i].source[j] > max_group2[j]:
                        max_group2[j] = group2[i].source[j]
            for i in range(96):
                if min_group1[i] - max_group2[i] >= float(val):
                    row = chr(ord('A') + i/12)
                    col = str(1 + i%12)
                    result.append(row + col)
    return result




