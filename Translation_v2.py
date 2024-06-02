
import pandas as pd
import math

from deep_translator import GoogleTranslator

src_lang = 'en'
dest_lang = 'mr'
translator = GoogleTranslator(source=src_lang, target=dest_lang)

df = pd.read_excel("Survey_data.xlsx")

for index, row in df.iterrows():
    rec = []
    
    for field in row:
        if str(field)!='nan':
            if type(field)==str:
                trans_field = translator.translate(field)
                rec.append(trans_field)
            else:
                rec.append(field)
            
    records.append(rec)

df1 = pd.DataFrame(records)
df_mr = pd.concat([df_mr, df1], axis = 0, ignore_index = True)

xls_filename = 'Survey_data_Marathi.xlsx'

df_mr.to_excel(xls_filename, index=False)
print("Excel File Translation SUCCESS")
