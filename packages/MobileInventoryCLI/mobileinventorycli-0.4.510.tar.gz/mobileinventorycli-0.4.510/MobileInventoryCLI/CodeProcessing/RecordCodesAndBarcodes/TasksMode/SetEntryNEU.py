from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.DB.PrintLogging import prinL as print
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.DB.db import *
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.DB.RandomStringUtil import *
import MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.Unified.Unified as unified
import MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.possibleCode as pc
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.DB.Prompt import *
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.DB.Prompt import prefix_text
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.TasksMode.ReFormula import *
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.FB.FormBuilder import *
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.FB.FBMTXT import *
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.RNE.RNE import *
from MobileInventoryCLI.CodeProcessing.RecordCodesAndBarcodes.Lookup2.Lookup2 import Lookup as Lookup2
from collections import namedtuple,OrderedDict
import nanoid
from password_generator import PasswordGenerator
import random
from pint import UnitRegistry
import pandas as pd
import numpy as np
from datetime import *
from colored import Style,Fore
import json,sys,math,re,calendar
def today():
    dt=datetime.now()
    return date(dt.year,dt.month,dt.day)


class NEUSetter:
    def __init__(self):
        pass

    def setFieldByName(self,fname):
        if fname == None:
            try:
                fields=[
                    'Code',
                    'Price',
                    'Description',
                    'Facings',
                    'Size',
                    'CaseCount',
                    'Tax',
                    'TaxNote',
                    'CRV',
                    'Name',
                    'Location',
                    'ALT_Barcode',
                    'DUP_Barcode',
                    'CaseID_BR',
                    'CaseID_LD',
                    'CaseID_6W',
                    'LoadCount',
                    'PalletCount',
                    'ShelfCount',]
                fct=len(fields)
                for num,f in enumerate(fields):
                    msg=f'{num}/{num+1} of {fct} -> {f}'
                    print(msg)
                which=Prompt.__init2__(None,func=FormBuilderMkText,ptext="which index?: ",helpText="which index",data="integer")
                if which in [None,]:
                    return
                elif which in ['d',]:
                    which=0
                fname=fields[which]
            except Exception as e:
                print(e)
                return
        while True:
            try:
                barcode=Prompt.__init2__(None,func=FormBuilderMkText,ptext=f"[{fname}] Barcode|Code|Name:",helpText="what are you looking for?",data="string")
                if barcode in ['d',None]:
                    return
                with Session(ENGINE) as session:
                    query=session.query(Entry).filter(or_(
                        Entry.Barcode==barcode,
                        Entry.Code==barcode,
                        Entry.Barcode.icontains(barcode),
                        Entry.Code.icontains(barcode),
                        Entry.Name.icontains(barcode)
                        ))
                    results=query.all()
                    ct=len(results)
                    if ct == 0:
                        print("Nothing Found")
                        continue
                    for num,entry in enumerate(results):
                        msg=f"{num}/{num+1} of {ct} - {entry.seeShort()}"
                        print(msg)
                    which=Prompt.__init2__(None,func=FormBuilderMkText,ptext=f"[{fname}]which index?: ",helpText="which index",data="integer")
                    if which in [None,]:
                        continue
                    elif which in ['d',]:
                        which=0
                    selected=results[which]
                    column=getattr(Entry,fname)
                    newValue=Prompt.__init2__(None,func=FormBuilderMkText,ptext=f"[old] {fname} = {getattr(selected,fname)} to:",helpText="new value",data=str(column.type))
                    if newValue in [None,'d']:
                        continue
                    setattr(selected,fname,newValue)
                    session.commit()
                    session.flush()
                    session.refresh(selected)
                    print(selected)
            except Exception as e:
                print(e)
                break