
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





def produce_sharedlists_item_address_fn(item_name):
    item_name_parse_matches = re.match(r'^\s*?(\w+(?:\s*?\[\s*?\.\.\s*?\])?(?:\.\w+(?:\s*?\[\s*?\.\.\s*?\])?)*?)\s*?((?:\.(?:categories|elements)\s*?\[\s*?\{?\s*?(\w+)\s*?\}?\s*?\])?)\s*?$',item_name,flags=re.I)
    if not item_name_parse_matches:
        raise Exception('Error: Can\'t parse item name: {n}'.format(n=item_name))
    return 'objMDM{iterative_fields}{add_subelement}'.format(
        iterative_fields = ''.join([ '.{node}["{name}"]'.format(node='Types' if i==0 else 'Elements',name=re.sub(r'^\s*?(\w+)\s*?(?:\[\s*?\.\.\s*?\])?\s*?$',lambda m: m[1],n,flags=re.I)) for i,n in enumerate('{match}'.format(match=item_name_parse_matches[1]).split('.')) ]),
        add_subelement = re.sub(r'^\s*?(\.(?:Categories|Elements)\s*?\[\s*?\{?\s*?)\s*?(\w+)\s*?(\}?\s*?\])\s*?$',lambda m: '{begin}"{body}"{end}'.format(begin=m[1],body=m[2],end=m[3]),item_name_parse_matches[2],flags=re.I),
    )

def produce_fields_item_address_fn(item_name):
    item_name_parse_matches = re.match(r'^\s*?(\w+(?:\s*?\[\s*?\.\.\s*?\])?(?:\.\w+(?:\s*?\[\s*?\.\.\s*?\])?)*?)\s*?((?:\.(?:categories|elements)\s*?\[\s*?\{?\s*?(\w+)\s*?\}?\s*?\])?)\s*?$',item_name,flags=re.I)
    if not item_name_parse_matches:
        raise Exception('Error: Can\'t parse item name: {n}'.format(n=item_name))
    return 'objMDM{iterative_fields}{add_subelement}'.format(
        iterative_fields = ''.join([ '.{node}["{name}"]'.format(node='Fields' if i==0 else 'Fields',name=re.sub(r'^\s*?(\w+)\s*?(?:\[\s*?\.\.\s*?\])?\s*?$',lambda m: m[1],n,flags=re.I)) for i,n in enumerate('{match}'.format(match=item_name_parse_matches[1]).split('.')) ]),
        add_subelement = re.sub(r'^\s*?(\.(?:Categories|Elements)\s*?\[\s*?\{?\s*?)\s*?(\w+)\s*?(\}?\s*?\])\s*?$',lambda m: '{begin}"{body}"{end}'.format(begin=m[1],body=m[2],end=m[3]),item_name_parse_matches[2],flags=re.I),
    )

def produce_pages_item_address_fn(item_name):
    item_name_parse_matches = re.match(r'^\s*?(\w+(?:\s*?\[\s*?\.\.\s*?\])?(?:\.\w+(?:\s*?\[\s*?\.\.\s*?\])?)*?)\s*?((?:\.(?:categories|elements)\s*?\[\s*?\{?\s*?(\w+)\s*?\}?\s*?\])?)\s*?$',item_name,flags=re.I)
    if not item_name_parse_matches:
        raise Exception('Error: Can\'t parse item name: {n}'.format(n=item_name))
    return 'objMDM{iterative_fields}{add_subelement}'.format(
        iterative_fields = ''.join([ '.{node}["{name}"]'.format(node='Pages' if i==0 else 'Item',name=re.sub(r'^\s*?(\w+)\s*?(?:\[\s*?\.\.\s*?\])?\s*?$',lambda m: m[1],n,flags=re.I)) for i,n in enumerate('{match}'.format(match=item_name_parse_matches[1]).split('.')) ]),
        add_subelement = re.sub(r'^\s*?(\.(?:Categories|Elements)\s*?\[\s*?\{?\s*?)\s*?(\w+)\s*?(\}?\s*?\])\s*?$',lambda m: '{begin}"{body}"{end}'.format(begin=m[1],body=m[2],end=m[3]),item_name_parse_matches[2],flags=re.I),
    )




def produce_variable_syntax(item_name, row, langs, produce_item_address_fn):
    syntax_add = ''

    if re.match(r'^\s*?$',item_name,flags=re.I):
        return ''
    
    item_path = produce_item_address_fn(item_name)

    # if 'update' not in df.columns:
    #     raise Exception('Error: "update" column not found')

    update_column_contents = row['update']
    variable_needs_updating = False if not update_column_contents or len(update_column_contents)==0 else ( True if re.match(r'^\s*?(?:y|yes|x|1|affirmative|true)\s*?$',update_column_contents,flags=re.I) else ( False if re.match(r'^\s*?(?:n|no|0|false|none)\s*?$',update_column_contents,flags=re.I) else ( not not update_column_contents ) ) )
    suppressmarker_variable = not variable_needs_updating

    data = {}
    suppressmarker_perlang = {}
    
    for lang in langs:
        col = 'langcode-{code}'.format(code=lang)
        data[lang] = row[col]
        if not not data[lang] or len(data[lang])>0:
            suppressmarker_perlang[lang] = False
        else:
            suppressmarker_perlang[lang] = True
    
    substitutes_base = {
        'suppress_marker_if_needs_updating': '\'' if suppressmarker_variable else '',
        'item_name': item_name,
        'item_path': item_path,
    }

    syntax_add = syntax_add + '{suppress_marker_if_needs_updating}\' variable: {item_name}\n'.format(**substitutes_base)
    for lang in langs:
        substitutes = {
            **substitutes_base,
            'langcode': lang,
            'text': escape(data[lang]),
            'suppress_marker_if_updated_text_empty':  '\'' if suppressmarker_perlang[lang] else '',
        }
        syntax_add = syntax_add + '{suppress_marker_if_needs_updating}\' {langcode} label: {text}\n'.format(**substitutes)
    for lang in langs:
        substitutes = {
            **substitutes_base,
            'langcode': lang,
            'text': escape(data[lang]),
            'suppress_marker_if_updated_text_empty':  '\'' if suppressmarker_perlang[lang] else '',
        }
        syntax_add = syntax_add + '{suppress_marker_if_needs_updating}{suppress_marker_if_updated_text_empty}{item_path}.Labels["Label"].Text["Question"]["{langcode}"] = "{text}"\n'.format(**substitutes)
    syntax_add = syntax_add + '\n\n'

    return syntax_add






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
                syntax_add = produce_variable_syntax(item_name, row, langs, produce_sharedlists_item_address_fn)

                resulting_syntax = resulting_syntax + syntax_add
                
            except Exception as e:
                print('Error: failed when processing shared list {n}'.format(n=item_name),file=sys.stderr)
                raise e

    # process section fields
    if 'fields' in map.data_sections:
        
        df = map.data_sections['fields']

        for item_name, row in df.iterrows():

            try:
                
                syntax_add = produce_variable_syntax(item_name, row, langs, produce_fields_item_address_fn)

                resulting_syntax = resulting_syntax + syntax_add
                
            except Exception as e:
                print('Error: failed when processing field {n}'.format(n=item_name),file=sys.stderr)
                raise e

    # process section pages
    if 'pages' in map.data_sections:
        
        df = map.data_sections['pages']

        for item_name, row in df.iterrows():

            try:
                
                syntax_add = produce_variable_syntax(item_name, row, langs, produce_pages_item_address_fn)

                resulting_syntax = resulting_syntax + syntax_add
                
            except Exception as e:
                print('Error: failed when processing page {n}'.format(n=item_name),file=sys.stderr)
                raise e


    result = '{part_begin}{part_body}{part_end}'.format(
        part_begin = TEMPLATE.template_begin.replace('<<MDDINPNAME>>',map.mdd_fname).replace('<<MDDOUTNAME>>',map.mdd_patched_fname).replace('<<LOCALVARS>>',''.join([', sLangText{langcode}'.format(langcode=lang) for lang in langs])),
        part_body = resulting_syntax,
        part_end = TEMPLATE.template_end,
    )

    return result



