import datajoint as dj
import re
import inspect
import pdb
import datetime


def get_options(table, field, context=None):
    '''
    For a given table and field, return the options of this field.
    Either from a enum or from the foreign keys.
    Inputs: table: table object
            field: str, field name
            context: context to search the class for the table
    Output: a list of possible values of this field, return empty list if there is no options
    '''
    if not context:
        context = inspect.currentframe().f_back.f_locals

    inspect.currentframe().f_locals.update(**context)

    dtype = table.heading.attributes[field].type
    # check whether the current field is an enum field.
    if 'enum' in dtype:
        temp = re.search(r'\(.*?\)', dtype).group()
        options = re.findall(r"'(.*?)'", dtype)
        return options
    else:
        graph = table.connection.dependencies
        graph.load()
        foreign_keys = graph.parents(table.full_table_name)

        for key, value in foreign_keys.items():
            if field == list(value['attr_map'].items())[0][0]:
                try:
                    int(key)
                    parent_table_name = list(graph.parents(key).keys())[0]
                    parent_field = list(list(graph.parents(key).values())[0]['attr_map'].items())[0][1]
                except ValueError:
                    parent_table_name = key
                    parent_field = value['attr_map'][1]
                break

        parent_table = dj.table.lookup_class_name(
            parent_table_name, context
        )

        options = (eval(parent_table)).fetch(parent_field)

        if not len(options):
            options = []
        return list(options)


def get_default(query, field):
    '''
    For a given table and field, return the options of this field.
    Inputs: table: query object
            field: str, field name
    Output: number or string, the default value of this field
    '''
    default = query.heading.attributes[field].default

    if default:
        matches = re.findall(r'\"(.+?)\"', query.heading.attributes[field].default)
        if matches:
            if matches[0] == 'current_timestamp()':
                return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            else:
                return matches[0]
        else:
            return ''
    else:
        return ''



if __name__ == "__main__":

    from dj_tables import lab, subject
    default = get_default(subject.Subject, 'subject_ts')
    print(default)
