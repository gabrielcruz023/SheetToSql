import contextlib
import os

import click
import pyexcel


def format_value(value):
    if value == 'NULL':
        return 'NULL'

    with contextlib.suppress(AttributeError, TypeError):
        return value.strftime('%Y-%m-%d %H-%M-%S')

    with contextlib.suppress(ValueError, TypeError):
        return str(int(value))

    with contextlib.suppress(ValueError, TypeError):
        return str(float(value))

    return '\'%s\'' % str(value)


def renderer(row):
    for cell in row:
        yield format_value(cell)


@click.command()
@click.argument('sheet', type=click.File('rb'))
@click.argument('output', type=click.File('w'), nargs=-1)
@click.option('--batch', type=click.INT, default=100,
              help='Size of SQL query batch.')
def sheet2sql(sheet, output, batch):
    '''
    Converts Excel sheets into SQL insert's, where SHEET is the file's
    path and OUTPUT is all output files which names exists in the file.
    '''
    sheet_ext = os.path.splitext(sheet.name)[1][1:]
    insert_layout = 'INSERT INTO {} ({}) VALUES ({})\n'

    for sql_output in output:
        sheet_name = os.path.splitext(os.path.basename(sql_output.name))[0]

        try:
            rows = pyexcel.iget_array(file_type=sheet_ext, file_content=sheet,
                                      row_renderer=renderer,
                                      sheet_name=sheet_name)
        except Exception:
            raise Exception('Couldn\'t open %r' % sheet.name)

        columns = ','.join(header.replace('\'', '') for header in next(rows))
        for index, row in enumerate(rows, start=1):
            if index > 1 and index % batch == 0:
                sql_output.write('GO\n')

            sql_output.write(insert_layout.format(sheet_name, columns,
                                                  ','.join(row)))


if __name__ == '__main__':
    sheet2sql()
