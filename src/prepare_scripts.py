
import sys

import re



if __name__ == '__main__':
    # run as a program
    import prepare_scripts_TEMPLATE as TEMPLATE
elif '.' in __name__:
    # package
    from . import prepare_scripts_TEMPLATE as TEMPLATE
else:
    # included with no parent package
    import prepare_scripts_TEMPLATE as TEMPLATE



def escape(s):
    s = '{s}'.format(s=s) # anyway we are writing it as text
    s = s.replace("\r", "\n")
    # Remove other invalid control chars
    s = re.sub(r"[\x00-\x08\x0B\x0C\x0E-\x1F]", "", s)
    s = s.replace('"','""')
    s = s.replace("\n",'" + newline + "')
    return s




# changes SL_GlobaslBrands.Categories[Amazon] (address string found in Excel) into mdm.Types["SL_GlobalBrands"].Elements["Amazon"] (address string that should be used in syntax)
def produce_sharedlists_item_syntax(item_name):
    item_name_parse_matches = re.match(r'^\s*?(\w+(?:\s*?\[\s*?\.\.\s*?\])?(?:\.\w+(?:\s*?\[\s*?\.\.\s*?\])?)*?)\s*?((?:\.(?:categories|elements)\s*?\[\s*?\{?\s*?(\w+)\s*?\}?\s*?\])?)\s*?$',item_name,flags=re.I)
    if not item_name_parse_matches:
        raise Exception('Error: Can\'t parse item name: {n}'.format(n=item_name))
    return 'objMDM{iterative_fields}{add_subelement}'.format(
        iterative_fields = ''.join([ '.{node}["{name}"]'.format(node='Types' if i==0 else 'Elements',name=re.sub(r'^\s*?(\w+)\s*?(?:\[\s*?\.\.\s*?\])?\s*?$',lambda m: m[1],n,flags=re.I)) for i,n in enumerate('{match}'.format(match=item_name_parse_matches[1]).split('.')) ]),
        add_subelement = re.sub(r'^\s*?(\.)((?:Categories|Elements))(\s*?\[\s*?\{?\s*?)\s*?(\w+)\s*?(\}?\s*?\])\s*?$',lambda m: '{begin_prefix}{begin_field}{begin_suffix}"{body}"{end}'.format(begin_prefix=m[1],begin_field='Elements',begin_suffix=m[3],body=m[4],end=m[5]),item_name_parse_matches[2],flags=re.I),
    )

# changes Gender.Categories[Male] (address string found in Excel) into mdm.Fields["Gender"].Elements["Male"] (address string that should be used in syntax)
def produce_fields_item_syntax(item_name):
    item_name_parse_matches = re.match(r'^\s*?(\w+(?:\s*?\[\s*?\.\.\s*?\])?(?:\.\w+(?:\s*?\[\s*?\.\.\s*?\])?)*?)\s*?((?:\.(?:categories|elements)\s*?\[\s*?\{?\s*?(\w+)\s*?\}?\s*?\])?)\s*?$',item_name,flags=re.I)
    if not item_name_parse_matches:
        raise Exception('Error: Can\'t parse item name: {n}'.format(n=item_name))
    return 'objMDM{iterative_fields}{add_subelement}'.format(
        iterative_fields = ''.join([ '.{node}["{name}"]'.format(node='Fields' if i==0 else 'Fields',name=re.sub(r'^\s*?(\w+)\s*?(?:\[\s*?\.\.\s*?\])?\s*?$',lambda m: m[1],n,flags=re.I)) for i,n in enumerate('{match}'.format(match=item_name_parse_matches[1]).split('.')) ]),
        add_subelement = re.sub(r'^\s*?(\.(?:Categories|Elements)\s*?\[\s*?\{?\s*?)\s*?(\w+)\s*?(\}?\s*?\])\s*?$',lambda m: '{begin}"{body}"{end}'.format(begin=m[1],body=m[2],end=m[3]),item_name_parse_matches[2],flags=re.I),
    )

# changes PAGE_AgeRange.DV_AgeGender (address string found in Excel) into mdm.Pages["PAGE_AgeGender"].Item["DV_AgeGender"] (address string that should be used in syntax)
def produce_pages_item_syntax(item_name):
    item_name_parse_matches = re.match(r'^\s*?(\w+(?:\s*?\[\s*?\.\.\s*?\])?(?:\.\w+(?:\s*?\[\s*?\.\.\s*?\])?)*?)\s*?((?:\.(?:categories|elements)\s*?\[\s*?\{?\s*?(\w+)\s*?\}?\s*?\])?)\s*?$',item_name,flags=re.I)
    if not item_name_parse_matches:
        raise Exception('Error: Can\'t parse item name: {n}'.format(n=item_name))
    return 'objMDM{iterative_fields}{add_subelement}'.format(
        iterative_fields = ''.join([ '.{node}["{name}"]'.format(node='Pages' if i==0 else 'Item',name=re.sub(r'^\s*?(\w+)\s*?(?:\[\s*?\.\.\s*?\])?\s*?$',lambda m: m[1],n,flags=re.I)) for i,n in enumerate('{match}'.format(match=item_name_parse_matches[1]).split('.')) ]),
        add_subelement = re.sub(r'^\s*?(\.(?:Categories|Elements)\s*?\[\s*?\{?\s*?)\s*?(\w+)\s*?(\}?\s*?\])\s*?$',lambda m: '{begin}"{body}"{end}'.format(begin=m[1],body=m[2],end=m[3]),item_name_parse_matches[2],flags=re.I),
    )




# generates a block of lines with syntax for each variable, that start with a comment with variable name
def produce_syntax_piece(item_name, row, langs, produce_item_syntax, config={}):
    syntax_piece_add = ''

    if re.match(r'^\s*?$',item_name,flags=re.I):
        return ''
    
    item_path = produce_item_syntax(item_name)

    update_column_contents = row['update']
    variable_needs_updating = False if not update_column_contents or len(update_column_contents)==0 else ( True if re.match(r'^\s*?(?:y|yes|x|1|affirmative|true)\s*?$',update_column_contents,flags=re.I) else ( False if re.match(r'^\s*?(?:n|no|0|false|none)\s*?$',update_column_contents,flags=re.I) else ( not not update_column_contents ) ) )
    
    if not variable_needs_updating:
        if 'flags' in config and 'print_not_updated_lines_commented_out' in config['flags'] and not not config['flags']['print_not_updated_lines_commented_out']:
            pass
        else:
            return ''

    data = {}
    is_overlay_empty = {}
    
    for lang in langs:
        col = 'langcode-{code}'.format(code=lang)
        data[lang] = row[col]
        if not not data[lang] or len(data[lang])>0:
            is_overlay_empty[lang] = False
        else:
            is_overlay_empty[lang] = True
    
    substitutes_base = {
        'linecommentmarker_if_var_needs_updating': '\'' if not variable_needs_updating else '',
        'item_name': item_name,
        'item_path': item_path,
    }

    syntax_piece_add = syntax_piece_add + '{linecommentmarker_if_var_needs_updating}\' variable: {item_name}\n'.format(**substitutes_base)
    for lang in langs:
        substitutes = {
            **substitutes_base,
            'langcode': lang,
            'text': escape(data[lang]),
            'linecommentmarker_if_updated_text_empty':  '\'' if is_overlay_empty[lang] else '',
        }
        syntax_piece_add = syntax_piece_add + '{linecommentmarker_if_var_needs_updating}\' {langcode} label: {text}\n'.format(**substitutes)
    for lang in langs:
        substitutes = {
            **substitutes_base,
            'langcode': lang,
            'text': escape(data[lang]),
            'linecommentmarker_if_updated_text_empty':  '\'' if is_overlay_empty[lang] else '',
        }
        syntax_piece_add = syntax_piece_add + '{linecommentmarker_if_var_needs_updating}{linecommentmarker_if_updated_text_empty}{item_path}.Labels["Label"].Text["Question"]["{langcode}"] = "{text}"\n'.format(**substitutes)
    syntax_piece_add = syntax_piece_add + '\n\n'

    return syntax_piece_add






def produce_scripts(map,config={}):

    langs = map.langs

    resulting_syntax = ''

    # process section shared lists
    if 'shared_lists' in map.data_sections:
        
        df = map.data_sections['shared_lists']

        for item_name, row in df.iterrows():

            try:
                
                if 'update' not in df.columns:
                    raise Exception('Error: "update" column not found')
                syntax_piece_add = produce_syntax_piece(item_name, row, langs, produce_sharedlists_item_syntax, config)

                resulting_syntax = resulting_syntax + syntax_piece_add
                
            except Exception as e:
                print('Error: failed when processing shared list {n}'.format(n=item_name),file=sys.stderr)
                raise e

    # process section fields
    if 'fields' in map.data_sections:
        
        df = map.data_sections['fields']

        for item_name, row in df.iterrows():

            try:
                
                if 'update' not in df.columns:
                    raise Exception('Error: "update" column not found')
                syntax_piece_add = produce_syntax_piece(item_name, row, langs, produce_fields_item_syntax, config)

                resulting_syntax = resulting_syntax + syntax_piece_add
                
            except Exception as e:
                print('Error: failed when processing field {n}'.format(n=item_name),file=sys.stderr)
                raise e

    # process section pages
    if 'pages' in map.data_sections:
        
        df = map.data_sections['pages']

        for item_name, row in df.iterrows():

            try:
                
                if 'update' not in df.columns:
                    raise Exception('Error: "update" column not found')
                syntax_piece_add = produce_syntax_piece(item_name, row, langs, produce_pages_item_syntax, config)

                resulting_syntax = resulting_syntax + syntax_piece_add
                
            except Exception as e:
                print('Error: failed when processing page {n}'.format(n=item_name),file=sys.stderr)
                raise e


    result = '{part_begin}{part_body}{part_end}'.format(
        part_begin = TEMPLATE.template_begin.replace('<<MDDINPNAME>>',map.mdd_fname).replace('<<MDDOUTNAME>>',map.mdd_patched_fname).replace('<<LOCALVARS>>',''.join([', sLangText{langcode}'.format(langcode=lang) for lang in langs])),
        part_body = resulting_syntax,
        part_end = TEMPLATE.template_end,
    )

    return result



