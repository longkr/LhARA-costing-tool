#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for "Equipment" class
============================

  Assumes python path includes LhARA code.

  Script starts by testing built in methods.

"""

import numpy as np

import Equipment as Eqp

##! Start:
print("========  Equipment: tests start  ========")

##! Check built-in methods:
EquipmentTest = 1
print()
print("EquipmentTest:", EquipmentTest, " check built-in methods.")
#.. __init__
print("    __init__:")
try:
    Eqp1 = Eqp.Equipment("LhARA")
except:
    print('      ----> Failed to create instance.')
    raise Exception
print('      ----> instance Eqp1 created.')
print("    <---- __init__ done.")
#.. __repr__
print("    __repr__:")
print("      ---->", repr(Eqp1))
print("    <---- __repr__ done.")
#.. __str__
print("    __str__:")
print(Eqp1)
print("    <---- __str__ done.")

##! Check getInstance method:
EquipmentTest = 2
print()
print("EquipmentTest:", EquipmentTest, " check getInstance method.")
Eqp2 = Eqp.Equipment("Test-1")
Eqp3 = Eqp.Equipment("Test-2")
Eqp4 = Eqp.Equipment("Test-2")
inst = Eqp.Equipment.getInstance("Dummy")
if inst == None:
    print('      ----> Correctly reported no instance:', inst)
else:
    raise Exception("Failed to catch absense of instance in getInstance")
try:
    inst = Eqp.Equipment.getInstance("Test-2")
except Eqp.DuplicateEquipmentClassInstance:
    print('      ----> Correctly caught multiple instance exception.')
inst = Eqp.Equipment.getInstance("Test-1")
if inst == Eqp2:
    print('      ----> Correctly found:', inst)
else:
    raise Exception("Failed to get instance Test-1")
inst = Eqp.Equipment.getInstance("LhARA")
if inst == Eqp1:
    print('      ----> Correctly found:', inst)
else:
    raise Exception("Failed to get instance LhARA")
print("    <---- getInstance done.")

##! Check get/set methods:
EquipmentTest = 3
print()
print("EquipmentTest:", EquipmentTest, " test get/set methods.")
print("    ----> Set equipment cost and total")
EqpCost = np.array([1., 2., 3., 4., 5.])
Eqp1.setEquipmentCost(EqpCost)
Eqp2.setEquipmentCost(EqpCost)
Eqp3.setEquipmentCost(EqpCost)
Eqp4.setEquipmentCost(EqpCost)
Eqp1.setTotalEquipmentCost()
Eqp2.setTotalEquipmentCost()
Eqp3.setTotalEquipmentCost()
Eqp4.setTotalEquipmentCost()
print(Eqp1)
print(Eqp2)
print(Eqp3)
print(Eqp4)
print("    <---- Done.")

##! Check creation of pandas dataframe:
EquipmentTest = 4
print()
print("EquipmentTest:", EquipmentTest, " test creation of pandas dataframe.")
EqpDtFrm = Eqp.Equipment.createPandasDataframe()
print("    <---- Done.")

##! Check creation of pandas dataframe:
EquipmentTest = 5
print()
print("EquipmentTest:", EquipmentTest, " test creation of csv file.")
try:
    Eqp.Equipment.createCSV(EqpDtFrm, '99-Scratch/Equipment.csv')
    print("    ----> CSV file successfully created.")    
except:
    print("    ----> FAILED to create CSV file.")
    raise exception
print("    <---- Done.")


##! Complete:
print()
print("========  Equipment: tests complete  ========")
