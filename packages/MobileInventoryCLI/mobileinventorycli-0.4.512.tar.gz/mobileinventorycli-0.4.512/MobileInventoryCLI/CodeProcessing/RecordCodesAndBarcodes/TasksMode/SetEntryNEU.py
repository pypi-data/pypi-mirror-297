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

    def newCodesFromExpireds(self):
        pass
        #scan through expireds table and check each barcode for an entry in Entry and update info from first result, or if not exists, prompt to create it/skip it/delete it, perform said action

    def newCodesFromPCs(self):
        pass
        #scan through PairCollections table and check each barcode for an entry in Entry and if not exists, prompt to create it/skip it/delete it, perform said action, and remove PairCollections with corresponding Barcode

    def setFieldByName(self,fname):
        fnames=[]
        if isinstance(fname,str):
            fnames=[fname,]
        elif isinstance(fname,list):
            fnames=fname
        elif fname == None:
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
                    msg=f'{Fore.light_green}{num}/{Fore.light_yellow}{num+1} of {Fore.light_red}{fct} -> {Fore.turquoise_4}{f}{Style.reset}'
                    print(msg)
                fnames=[]
                which=Prompt.__init2__(None,func=FormBuilderMkText,ptext=f"which {Fore.light_green}index{Fore.light_red}({Fore.light_green}es{Fore.light_red}){Fore.light_yellow}?: ",helpText=f"which {Fore.light_green}index{Fore.light_red}({Fore.light_green}es{Fore.light_red}){Fore.light_yellow}, use comma to separate multiple fields{Style.reset}",data="list")
                if which in [None,]:
                    return
                elif which in ['d',]:
                    which=[0,]
                for i in which:
                    try:
                        fnames.append(fields[int(i)])
                    except Exception as e:
                        print(e)
                        try:
                            fnames.append(fields[fields.index(str(i))])
                        except Exception as e:
                            print(e)

            except Exception as e:
                print(e)
                return
        while True:
            try:
                barcode=Prompt.__init2__(None,func=FormBuilderMkText,ptext=f"[{fnames}] {Fore.light_green}Barcode|{Fore.turquoise_4}Code|{Fore.light_magenta}Name{Fore.light_yellow}:",helpText="what are you looking for?",data="string")
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
                        msg=f'{Fore.light_green}{num}/{Fore.light_yellow}{num+1} of {Fore.light_red}{ct} -> {entry.seeShort()}'
                        print(msg)
                    which=Prompt.__init2__(None,func=FormBuilderMkText,ptext=f"[{fnames}]which {Fore.light_green}index{Fore.light_yellow}?: ",helpText=f"{Fore.light_steel_blue}which index {Fore.light_yellow}number in light yellow{Style.reset}",data="integer")
                    if which in [None,]:
                        continue
                    elif which in ['d',]:
                        which=0
                    selected=results[which]
                    for fname in fnames:
                        column=getattr(Entry,fname)
                        newValue=Prompt.__init2__(None,func=FormBuilderMkText,ptext=f"[{Fore.medium_violet_red}old{Fore.light_yellow}] {Fore.light_magenta}{fname} = {Fore.light_red}{getattr(selected,fname)}{Fore.orange_red_1} to: {Style.reset}",helpText="new value",data=str(column.type))
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