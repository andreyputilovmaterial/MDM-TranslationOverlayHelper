
from pathlib import Path
import pandas as pd

import re



class Map:
    def __init__(self,excel_filename,config={}):
        
        self.config = config

        with pd.ExcelFile(excel_filename,engine='openpyxl') as xls:
            df_overview = xls.parse(sheet_name='overview', header=0, index_col=0, keep_default_na=False).fillna('')
            
            # mdd_properties = dict(zip(df_overview['name'], df_overview['value']))
            mdd_properties = df_overview.iloc[:, 0].to_dict()

            self.mdd_path = mdd_properties['MDD']
            self.mdd_fname = Path(self.mdd_path).name
            self.mdd_patched_fname = '{basepart}_updated.mdd'.format(basepart=re.sub(r'\.mdd\s*?$','','{s}'.format(s=self.mdd_fname),flags=re.I))

            self.data_sections = {}
            columns_unique = []
            columns_seen = set()
            for sheet_name in xls.sheet_names:
                df = xls.parse(sheet_name=sheet_name, header=0, index_col=0, keep_default_na=False).fillna('')
                for col in df.columns:
                    if col not in columns_seen:
                        columns_unique.append(col)
                        columns_seen.add(col)
                if sheet_name=='fields':
                    self.data_sections['fields'] = df
                elif sheet_name=='shared_lists':
                    self.data_sections['shared_lists'] = df
                elif sheet_name=='pages':
                    self.data_sections['pages'] = df

            self.langs = []
            for col_name in columns_unique:
                possible_lang_matches = re.match(r'^\s*?langcode-(.*?)\s*?$',col_name)
                if possible_lang_matches:
                    lang_name = possible_lang_matches[1]
                    self.langs.append(lang_name)
            



