
import argparse
# from pathlib import Path
import traceback, sys






if __name__ == '__main__':
    # run as a program
    from lib.mdmreadpy import read_mdd
    from lib.mdmreadpy.lib.mdmreportpy import report_create as report_html_create
    from lib.mdmexcelreportpy import report_create as report_excel_create
    import generate_scripts
elif '.' in __name__:
    # package
    from .lib.mdmreadpy import read_mdd
    from .lib.mdmreadpy.lib.mdmreportpy import report_create as report_html_create
    from .lib.mdmexcelreportpy import report_create as report_excel_create
    from . import generate_scripts
else:
    # included with no parent package
    from lib.mdmreadpy import read_mdd
    from lib.mdmreadpy.lib.mdmreportpy import report_create as report_html_create
    from lib.mdmexcelreportpy import report_create as report_excel_create
    import generate_scripts






def call_read_mdd_program():
    return read_mdd.entry_point({'arglist_strict':False})

def call_report_program():
    raise Exception('deprecated: --program report is deprecated here; please use --program report_html or --program report_excel instead')

def call_report_html_program():
    return report_html_create.entry_point({'arglist_strict':False})

def call_report_excel_program():
    return report_excel_create.entry_point({'arglist_strict':False})

def call_generate_overlays_script():
    return generate_scripts.entry_point({'arglist_strict':False})




run_programs = {
    'read_mdd': call_read_mdd_program,
    'report': call_report_program,
    'report_html': call_report_html_program,
    'report_excel': call_report_excel_program,
    'generate_overlays_script': call_generate_overlays_script,
}



def main():
    try:
        parser = argparse.ArgumentParser(
            description="Universal caller of mdmtranslationsoverlayhelper-py utilities"
        )
        parser.add_argument(
            #'-1',
            '--program',
            choices=dict.keys(run_programs),
            type=str,
            required=True
        )
        args, args_rest = parser.parse_known_args()
        if args.program:
            program = '{arg}'.format(arg=args.program)
            if program in run_programs:
                run_programs[program]()
            else:
                raise AttributeError('program to run not recognized: {program}'.format(program=args.program))
        else:
            print('program to run not specified')
            raise AttributeError('program to run not specified')
    except Exception as e:
        # the program is designed to be user-friendly
        # that's why we reformat error messages a little bit
        # stack trace is still printed (I even made it longer to 20 steps!)
        # but the error message itself is separated and printed as the last message again

        # for example, I don't write "print('File Not Found!');exit(1);", I just write "raise FileNotFoundErro()"
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
    main()


