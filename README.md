# OrderSelector v1.0
My friend Wei needs a tool to help her obtain positions of 'satisfying' values after filtering and calculating raw data obtained from her lab.
These data are collected from several different colleagues and are kept in an single excel file. 
We call each block of the raw data is a 'plate'. Each plate has a header line with format like this: "Plate: OrderID GroupID Operator PlateID Date"(But some fields in many headers may just lose or reverse). 1 order may have more than 1 group and 1 group may have more than one plate. Also an operator may be involved in several orders, groups, plates or dates.
Fortunately, the dimension of a single plate is 8×12(for positions, row names: [A, H]; col names: [1, 12]) and the values are in a narrow range of [0, 3], which is relatively easy to recognize and process.

Finally, I wrote this interactive tool with the following main functions:
1. In-group operations:
    Filter single plate: operators: >, >=, =, <, <=
    Filter all plates: all plates must meet the conditions.
2. Inter-group operations:
    Only subtraction available for groups with same OrderID.
3. Search operations:
    By order/operator/date.

Requirements:
Language: python 3.6
Operation system: Windows 10
Package required: pandas

