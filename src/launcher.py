
import argparse
# from pathlib import Path
import traceback, sys






if __name__ == '__main__':
    # run as a program
    from lib.mdmreadpy import read_mdd
    from lib.mdmreadpy.lib.mdmreportpy import report_create as report_html_create
    from lib.mdmexcelreportpy import report_create as report_excel_create
    import program_generate_overlays_script
    import program_prep_mddread_scheme
elif '.' in __name__:
    # package
    from .lib.mdmreadpy import read_mdd
    from .lib.mdmreadpy.lib.mdmreportpy import report_create as report_html_create
    from .lib.mdmexcelreportpy import report_create as report_excel_create
    from . import program_generate_overlays_script
    from . import program_prep_mddread_scheme
else:
    # included with no parent package
    from lib.mdmreadpy import read_mdd
    from lib.mdmreadpy.lib.mdmreportpy import report_create as report_html_create
    from lib.mdmexcelreportpy import report_create as report_excel_create
    import program_generate_overlays_script
    import program_prep_mddread_scheme






# STDOUT_COLOR_RED = "\033[91m"
STDOUT_COLOR_RED = "\033[31m"
STDOUT_COLOR_RESET = "\033[0m"
STDOUT_COLOR_GREEN = "\033[32m"


def call_read_mdd_program(*argcs,**kwargs):
    return read_mdd.entry_point(*argcs,**kwargs)

def call_report_program(*argcs,**kwargs):
    raise Exception('deprecated: --program report is deprecated here; please use --program report_html or --program report_excel instead')

def call_report_html_program(*argcs,**kwargs):
    return report_html_create.entry_point(*argcs,**kwargs)

def call_report_excel_program(*argcs,**kwargs):
    return report_excel_create.entry_point(*argcs,**kwargs)

def call_generate_overlays_script(*argcs,**kwargs):
    return program_generate_overlays_script.entry_point(*argcs,**kwargs)

def call_prepmddscheme_program(*argcs,**kwargs):
    return program_prep_mddread_scheme.entry_point(*argcs,**kwargs)



run_programs = {
    'read_mdd': call_read_mdd_program,
    'report': call_report_program,
    'report_html': call_report_html_program,
    'report_excel': call_report_excel_program,
    'generate_overlays_script': call_generate_overlays_script,
    'prep_mddread_scheme': call_prepmddscheme_program,
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
                run_programs[program](args_rest)
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
        print(f'{STDOUT_COLOR_RED}Error:{STDOUT_COLOR_RESET}',file=sys.stderr)
        print('',file=sys.stderr)
        print(f'{STDOUT_COLOR_RED}{e}{STDOUT_COLOR_RESET}',file=sys.stderr)
        print('',file=sys.stderr)
        exit(1)


if __name__ == '__main__':
    main()


