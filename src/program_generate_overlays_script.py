import traceback, sys # for pretty-printing any issues that happened during runtime; if we hit FileNotFound I don't appreciate when a log traceback is shown, the error should be simple and clear
from datetime import datetime
# from dateutil import tz
import argparse
from pathlib import Path

import pandas as pd


if __name__ == '__main__':
    # run as a program
    # import plugins
    from read_excel import Map
    from prepare_scripts import produce_scripts
elif '.' in __name__:
    # package
    # from . import plugins
    from .read_excel import Map
    from .generate_scripts import produce_scripts
else:
    # included with no parent package
    # import plugins
    from read_excel import Map
    from prepare_scripts import produce_scripts









def entry_point(config={}):
    try:
        time_start = datetime.now()
        script_name = 'mdmtoolsap translation overlay codegen script'

        parser = argparse.ArgumentParser(
            description="Produce a ready mrs script to write updates to MDD",
            prog='mdmtoolsap --program generate_overlays_script',
        )
        parser.add_argument(
            '--inpfile',
            help='Input Excel file location',
            type=str,
            required=True
        )
        parser.add_argument(
            '--outfile',
            help='Desird name for the resulting script',
            type=str,
            required=True,
        )
        parser.add_argument(
            '--flags',
            help='Possible comma-separate flags that change program behavior: `print_not_updated_lines_commented_out` to include all rows inm export but keep those where "update" column is not punched commented out (as opposed to those lines being cmopletely skipped by default), `dont_write_translators_comments_to_mdd` to not include code that writes comment column to MDD',
            type=str,
            required=False,
        )
        args = None
        args_rest = None
        if( ('arglist_strict' in config) and (not config['arglist_strict']) ):
            args, args_rest = parser.parse_known_args()
        else:
            args = parser.parse_args()

        print('{script_name}: script started at {dt}'.format(dt=time_start,script_name=script_name))

        input_excel_filename = None
        if args.inpfile:
            input_excel_filename = Path(args.inpfile)

        #print('{script_name}: reading {fname}'.format(fname=input_excel_filename,script_name=script_name))
        if not(Path(input_excel_filename).is_file()):
            raise FileNotFoundError('File not found: {fname}'.format(fname=input_excel_filename))
        
        config = {
            'flags': {
                'write_translators_comments_to_mdd': True, # that would be the default, unless "dont_write_translators_comments_to_mdd" flag is set
            },
        }

        if args.flags:
            for flag in args.flags.split(','):
                if flag.lower().strip()=='print_not_updated_lines_commented_out'.lower().strip():
                    config['flags']['print_not_updated_lines_commented_out'] = True
                elif flag.lower().strip()=='dont_write_translators_comments_to_mdd'.lower().strip():
                    config['flags']['write_translators_comments_to_mdd'] = False
                else:
                    raise Exception('Error: {script_name}: Unrecognized flag: {flag}'.format(script_name=script_name,flag=flag))

        map = Map(input_excel_filename,config)
        result = produce_scripts(map,config)
        
        out_fname = None
        if args.outfile:
            out_fname = Path(args.outfile)
        out_fname = Path.resolve(out_fname)

        print('{script_name}: saving as "{fname}"'.format(fname=out_fname,script_name=script_name))
        if not not result:
            with open(out_fname, 'w', encoding='utf-8') as outfile:
                outfile.write(result)
        else:
            raise Exception('Error: inp file was not opened and loaded, something was wrong')

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
