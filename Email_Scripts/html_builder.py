import pandas as pd

class NativeDict(dict):
    """
        Helper class to ensure that only native types are in the dicts produced by
        :func:`to_dict() <pandas.DataFrame.to_dict>`
    """
    def __init__(self, *args, **kwargs):
        super().__init__(((k, self.convert_if_needed(v)) for row in args for k, v in row), **kwargs)

    @staticmethod
    def convert_if_needed(value):
        """
            Converts `value` to native python type.
        """
        if pd.isnull(value):
            return None
        if isinstance(value, pd.Timestamp):
            return value.isoformat()
        if hasattr(value, 'dtype'):
            mapper = {'i': int, 'u': int, 'f': float}
            _type = mapper.get(value.dtype.kind, lambda x: x)
            return _type(value)
        if value == 'NaT':
            return None
        return value

def make_table(df, **kwargs):
    # Unpack arguements
    columns = kwargs.get('columns', [])
    row_class = kwargs.get('row_class', lambda x: 'not present')
    cell_classes = kwargs.get('cell_classes', {})
    col_classes = kwargs.get('col_classes', {})
    tooltips = kwargs.get('tooltips', {})
    links = kwargs.get('links', {})
    default_styles = kwargs.get('default_styles', True)
    styles =  kwargs.get('styles', '')

    # Check for pandas data frame input
    if not isinstance(df, pd.DataFrame):
        raise TypeError('Input data frame MUST BE a Pandas DataFrame, pandas.DataFrame')
    # Check for improper column list data type
    if not isinstance(columns, list):
        raise TypeError('columns input must be List object type, list')
    # Check for improper row_class function
    if not callable(row_class):
        raise TypeError('row_class must be passed a function')
    # Check for improper cell_classes dict data type
    if not isinstance(cell_classes, dict):
        raise TypeError('cell_classes lookup should be a Dictionary object type, dict')
    # Check for improper col_classes dict data type
    if not isinstance(col_classes, dict):
        raise TypeError('col_classes lookup should be a Dictionary object type, dict')
    # Check for improper tooltips dict data type
    if not isinstance(tooltips, dict):
        raise TypeError('tooltips lookup should be a Dictionary object type, dict')
    for key in tooltips:
        if not key in df.columns.values or not tooltips[key] in df.columns.values:
            raise KeyError('Both key and value in Tooltips dict must be in DataFrame column names')
    # Check for improper links dict data type
    if not isinstance(links, dict):
        raise TypeError('links lookup should be a Dictionary object type, dict')
    for key in links:
        if not key in df.columns.values or not links[key] in df.columns.values:
            raise KeyError('Both key and value in Links dict must be in DataFrame column names')
    # Assign DataFrame column headers if no input present, or len zero
    if len(columns) == 0:
        columns = df.columns.values
    else:
        # Check Specified columns are all in DataFrame
        for col in columns:
            if not col in df.columns.values:
                raise KeyError('Specified column does not exsist in DataFrame:', col)

    # Convert data frame to list of dicts
    data = df.to_dict(orient='records', into=NativeDict)

    check_row_classes = False if row_class(data[0]) == 'not present' else True

    # Verify provided function returns a string
    if check_row_classes:
        if not isinstance(row_class(data[0]), str):
            raise TypeError('Return value from row_class function must be type str')

    check_cell_classes = True if len(cell_classes.keys()) > 0 else False

    # check to make sure props on row classes are functions and return strings
    if check_cell_classes:
        for key in cell_classes:
            if not callable(cell_classes[key]):
                raise TypeError('All values in cell_classes dict must be functions, error on:', key)
            else:
                test = cell_classes[key](data[0][key], data[0])
                if not isinstance(test, str):
                    raise TypeError('Return values from cell_classes functions must be type str, error on:', key)

    # Build table header
    table_head = ""
    for col in columns:
        table_head += f"<th>{col}</th>"

    # Build table body
    table_body = ""
    for row in data:

        row_html = ""

        for col in columns:
            input = row[col] if row[col] != None else ""

            cell_class_list = ""

            if col in cell_classes:
                cell_class_list += " " + cell_classes[col](row[col], row)

            if col in col_classes:
                cell_class_list += " " + col_classes[col]

            if col in tooltips:
                cell_class_list += " default"
                title = f'title=\"{row[tooltips[col]]}\"'
            else:
                title = ''

            if col in links:
                input = f'<a href=\"{row[links[col]]}\">{input}</a>'

            row_html += f'<td class=\"{cell_class_list}\" {title} >{input}</td>'

        if check_row_classes:
            row_class_returned = row_class(row)
            table_row = f'<tr class=\"{row_class_returned}\">{row_html}</tr>\n'
        else:
            table_row = f'<tr>{row_html}</tr>\n'

        table_body += table_row.format(row_html=row_html)


    if default_styles:
        css_string = open("C:/Socrata/hdot-scripts/Python/modules/html_builder_styles.css", "r").read()
    else:
        css_string = ''

    table = """
    <table>
        <tr>{th}</tr>
        {tb}
    </table>
    <style>{st}</style>
    """

    # Format Final Table to be Returned
    formatted_table = table.format(th=table_head, tb=table_body, st=css_string)

    if len(styles) > 0:
        formatted_table += f'\n<style>\n{styles}</style>'

    return formatted_table
