# import os, time, re, sys
import traceback, sys # for pretty-printing any issues that happened during runtime; if we hit FileNotFound I don't appreciate when a log traceback is shown, the error should be simple and clear
from datetime import datetime
# from dateutil import tz
import argparse
from pathlib import Path
import re
import json



if __name__ == '__main__':
    # run as a program
    # import format_sheet_xlsxwriter as excel_xlsxwriter_format_sheet
    pass
elif '.' in __name__:
    # package
    # from . import format_sheet_xlsxwriter as excel_xlsxwriter_format_sheet
    pass
else:
    # included with no parent package
    # import format_sheet_xlsxwriter as excel_xlsxwriter_format_sheet
    pass




MDD_TRANSLATORSCOMMENT_PROPERTY_NAME = 'SEToolOverlayHelper_TranslatorsComment'






def upd(data,config={}):
    columns_global = ((data or {})['report_scheme'] if 'report_scheme' in (data or {}) else {})['columns'] if 'columns' in (((data or {})['report_scheme'] if 'report_scheme' in (data or {}) else {})) else ['name']

    errorhandling_counter = { 'num': 0 }

    def upd_record(record_data):

        name = record_data['name'] if 'name' in record_data else '{s}'.format(s=record_data)

        try:

            comment_preserve = record_data['comment'] if 'comment' in record_data else None

            comment = None

            if 'properties' in record_data:
                properties = record_data['properties']
                try:
                    for prop in properties:
                        prop_name = prop['name'] if 'name' in prop else ''
                        prop_name = '{s}'.format(s=prop_name)
                        if prop_name.strip().lower() == MDD_TRANSLATORSCOMMENT_PROPERTY_NAME.strip().lower():
                            comment = '{s}'.format(s=prop['value'])
                except Exception as e:
                    comment = 'Error: failed to read properties: {e}'.format(e=e)
                    if errorhandling_counter['num']<=1:
                        print('Error: failed to read properties: {e}'.format(e=e),file=sys.stderr)
                    errorhandling_counter['num'] = errorhandling_counter['num'] + 1

            if not comment:
                comment = ''
            if comment_preserve:
                comment = '{comment}; {comment_preserve}'.format(comment=comment,comment_preserve=comment_preserve)
            
            return {
                **record_data,
                'update': None, # reset, just in case
                'comment': comment,
            }
            
        except Exception as e:
            print('Error: failed when processing row "{name}"'.format(name=name))
            raise e

    def upd_section(section_data):

        if ('name' not in section_data) or not section_data['name']:
            return section_data
        
        name = section_data['name']

        try:

            columns = [c for c in section_data['columns']] if 'columns' in section_data else [c for c in columns_global]
            columns = [c for c in columns if c not in ['properties','attributes']]
            if 'name' not in columns:
                columns = ['name',*columns]
            if 'update' not in columns:
                columns.insert(columns.index('name')+1,'update')
            # if 'comment' in columns:
            #     raise Exception('the file already includes the "comment" column - we are not eager to overwrite')
            if 'comment' not in columns:
                columns.append('comment')
            
            content = [ upd_record(s) for s in (section_data['content'] if 'content' in section_data else []) if ('name' in s) and (not not s['name']) and not(s['name']=='') ]

            return {
                **section_data,
                'columns': columns,
                'content': content,
            }
        
        except Exception as e:
            print('Error: failed when processing section "{name}"'.format(name=name))
            raise e
    
    return {
        **data,
        'sections': [ upd_section(s) for s in (data['sections'] if 'sections' in data else []) ],
    }





def entry_point(config={}):
    try:
        time_start = datetime.now()
        script_name = 'mdmtoolsap prep mddread scheme script'

        parser = argparse.ArgumentParser(
            description="Updates the .json file and prepares it for the needs of translation utility",
            prog='mdmtoolsap --prep_mddread_scheme report_excel'
        )
        parser.add_argument(
            '--inpfile',
            help='JSON with MDD Data',
            type=str,
            required=True
        )
        parser.add_argument(
            '--outfile',
            help='JSON to be written',
            type=str,
            required=True
        )
        # parser.add_argument(
        #     '--flags',
        #     help='(Optional) set of flags (comma-delimited) to control program behavior)',
        #     type=str,
        #     required=False
        # )
        args = None
        args_rest = None
        if( ('arglist_strict' in config) and (not config['arglist_strict']) ):
            args, args_rest = parser.parse_known_args()
        else:
            args = parser.parse_args()
        
        print('{script_name}: script started at {dt}'.format(dt=time_start,script_name=script_name))

        input_mdd_filename = None
        if args.inpfile:
            input_mdd_filename = Path(args.inpfile)
            # input_mdd_filename = '{input_mdd_filename}'.format(input_mdd_filename=input_mdd_filename.resolve())
        # input_mdd_filename_specs = open(input_mdd_filename_specs_name, encoding="utf8")
        input_mdd_filename = Path.resolve(input_mdd_filename)
        #print('{script_name}: reading {fname}'.format(fname=input_mdd_filename,script_name=script_name))
        if not(Path(input_mdd_filename).is_file()):
            raise FileNotFoundError('file not found: {fname}'.format(fname=input_mdd_filename))

        inpfile_map_in_json = None
        with open(input_mdd_filename, encoding="utf8") as input_mdd_file: # TODO: is setting encoding needed?
            try:
                inpfile_map_in_json = json.load(input_mdd_file)
            except json.JSONDecodeError as e:
                # just a more descriptive message to the end user
                # can happen if the tool is started two times in parallel and it is writing to the same json simultaneously
                raise TypeError('Diff: Can\'t read input file as JSON: {msg}'.format(msg=e))

        output_mdd_filename = None
        if args.outfile:
            output_mdd_filename = Path(args.outfile)
            # output_mdd_filename = '{output_mdd_filename}'.format(output_mdd_filename=output_mdd_filename.resolve())
        else:
            # output_mdd_filename = ( Path(input_mdd_filename).parents[0] / '{basename}{ext}'.format(basename=re.sub(r'\.json\s*?$','','{n}'.format(n=Path(input_mdd_filename).name),flags=re.I),ext='.xlsx') if Path(input_mdd_filename).is_file() else re.sub(r'^\s*?(.*?)(?:\.json)?\s*?$',lambda m: '{base}{added}'.format(base=m[1],added='.xlsx'),'{path}'.format(path=input_mdd_filename)) )
            output_mdd_filename = input_mdd_filename
        # output_mdd_filename_specs = open(output_mdd_filename_specs_name, encoding="utf8")
        output_mdd_filename = Path.resolve(output_mdd_filename)

        config = {}

        # if args.flags:
        #     config['flags'] = '{s}'.format(s=args.flags).split(',')

        result = upd(inpfile_map_in_json,config)
        
        print('{script_name}: saving as "{fname}"'.format(fname=output_mdd_filename,script_name=script_name))
        
        with open(output_mdd_filename, "w", encoding='utf-8') as outfile: #TODO:  is setting encoding needed?
            json.dump(result,outfile,indent=2)

        time_finish = datetime.now()
        print('{script_name}: finished at {dt} (elapsed {duration})'.format(dt=time_finish,duration=time_finish-time_start,script_name=script_name))

    except Exception as e:
        # for pretty-printing any issues that happened during runtime; if we hit FileNotFound I don't appreciate when a log traceback is shown, the error should be simple and clear
        # the program is designed to be user-friendly
        # that's why we reformat error messages a little bit
        # stack trace is still printed (I even made it longer to 20 steps!)
        # but the error message itself is separated and printed as the last message again

        # for example, I don't write 'print('File Not Found!');exit(1);', I just write 'raise FileNotFoundErro()'
        print('',file=sys.stderr)
        print('Stack trace:',file=sys.stderr)
        print('',file=sys.stderr)
        traceback.print_exception(e,limit=20)
        print('',file=sys.stderr)
        print('',file=sys.stderr)
        print('',file=sys.stderr)
        print('Error:',file=sys.stderr)
        print('',file=sys.stderr)
        print('{e}'.format(e=e),file=sys.stderr)
        print('',file=sys.stderr)
        exit(1)


if __name__ == '__main__':
    entry_point({'arglist_strict':True})
