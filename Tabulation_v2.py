
import pandas as pd
import re
import os

#import library
import speech_recognition as sr
#Initiаlize  reсоgnizer  сlаss  (fоr  reсоgnizing  the  sрeeсh)
r = sr.Recognizer()

digits_dict = {
    
    'zero' : '0',
    'one' : '1',
    'two' : '2',
    'three' : '3',
    'four' : '4',
    'five' : '5',
    'six' : '6',
    'seven' : '7',
    'eight' : '8',
    'nine' : '9',
    'to' : '2'
    
}

def RectifyDigits(text):
    
    for key, value in digits_dict.items():
        search_pattern = " " + key + " "
        replace_pattern = value + " "
        text = re.sub(search_pattern, replace_pattern, text)
    
    return text


def Tabularize(text):

    global database
    text = text.lower()
    record = [[]]
    try:
        fields = text.split(' and ')
        
        if len(fields)>=3:
            name = fields.pop(0)
            addr = fields.pop(0)
            mob = fields.pop(0)
            
            remainder = []
            if len(fields)>0:
                remainder = fields
                remainder = [x.strip().capitalize() for x in remainder]
            
            numbercorr_addr = RectifyDigits(addr)
            name = name.strip().title()
            numbercorr_addr = numbercorr_addr.strip().title()
            mob = mob.replace(" ","")
            
            record = [name, numbercorr_addr, mob]
            if len(remainder)!=0:
                for fld in remainder:
                    record.append(fld)

            print(record)
            database.append(record)
            
        else:
            print("ERROR Min. 3 Fields (Name, Address, Mobile Number) Required")
            print("Text Found from Recording:", text)
            
    except:
        print("ERROR in Row:", text)


database = []

directory_path = 'Recordings/'
file_list = [directory_path+"/"+file for file in os.listdir(directory_path)]
sorted_files = sorted(file_list, key=os.path.getmtime)

for audio_file in sorted_files:
    with sr.AudioFile(audio_file) as source:
        audio_text = r.listen(source)
        try:
            print("\n",audio_file.split("/")[-1])
            # using google speech recognition
            text = r.recognize_google(audio_text)
            Tabularize(text)
        
        except:
             print('ERROR in Audio File:', audio_file)


df = pd.DataFrame(database)

xls_filename = 'Survey_data.xlsx'

if os.path.exists(xls_filename):
    old_df = pd.read_excel(xls_filename)
    df = pd.concat([old_df, df], axis = 0, ignore_index = True)
    print("Content Appended to Excel File")
    
df.to_excel(xls_filename, index=False)
print("Excel File Creation SUCCESS")

