"""
SQL-like interface to tabular structured data
"""

# ------------------------------------------------------------------------------------------------ #
# Copyright (c) 2024, Mikhail Zakharov <zmey20000@yahoo.com>
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
# ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

# ------------------------------------------------------------------------------------------------ #
import csv
import json
import sys
import signal
import time

# -- Constants ----------------------------------------------------------------------------------- #
# JOIN
JOIN_INNER = 0
JOIN_LEFT = 1
JOIN_RIGHT = 2
JOIN_FULL = 3

# ORDER BY
ORDER_BY_INC = 0  # Increasing
ORDER_BY_DEC = 1  # Decreasing

# Syntax
LINETERMINATOR = '\n'                   # '\n' is autoconverted to '\r\n' on Windows
TNAME_COLUMN_DELIMITER = '.'            # Delimiter between table name and a column: table.column
TNAME_TNAME_DELIMITER = '_'             # Delimiter between table names e.g, on join(): table_table

# ------------------------------------------------------------------------------------------------ #
try:
    # If tsqlike has been imported
    from tsqlike.__about__ import __version__
except ModuleNotFoundError:
    try:
        # If it is called directly as a Python file
        from __about__ import __version__
    except ModuleNotFoundError:
        __version__ = '?.?.?'


# -- Standalone functions ------------------------------------------------------------------------ #
def open_file(file_name=None, file_mode='r+', encoding=None, newline=None):
    """ Open a file """

    # Detect default file: STDIN or STDOUT
    default_file = sys.stdin if 'r' in file_mode else sys.stdout

    try:
        f = file_name and open(file_name, file_mode, encoding=encoding,
                               newline=newline) or default_file
    except (FileNotFoundError, PermissionError, OSError) as _err:
        print(f'FATAL@open_file(): {_err}')
        sys.exit(1)

    # Ignore BrokenPipeError on *NIX if piping output
    if f == sys.stdout and sys.platform != 'win32':
        signal.signal(signal.SIGPIPE, signal.SIG_DFL)

    return f


# ------------------------------------------------------------------------------------------------ #
def close_file(file):
    """
    Close the file

    :param file:    File to close
    """

    if file and file is not sys.stdout and file is not sys.stdin:
        file.close()


# ------------------------------------------------------------------------------------------------ #
def str_to_type(s, use_none=False):
    """ Convert string s to a proper type: int, float or boolean """

    # Convert '' - empty strings to None?
    if s == '' and use_none:
        return None

    if s in ('True', 'true'):
        return True

    if s in ('False', 'false'):
        return False

    try:
        return float(s) if '.' in s or ',' in s else int(s)     # to float and int
    except (ValueError, TypeError):
        return s                                                # no conversion possible -> string


# ------------------------------------------------------------------------------------------------ #
def read_csv(in_file=None, encoding=None, newline='', name='', detect_str_types=False,
             dialect='excel', **fmtparams):
    """
    Read CSV from a file and import into a Table object

    :param in_file:             Filename to read CSV from
    :param encoding:            Character encoding
    :param newline:             UNIX/Windows/Mac style line ending
    :param name:                Table name to assign
    :param detect_str_types:    Detect and correct types of data, default - False
    :param dialect:             CSV dialect, e.g: excel, unix
    :**fmtparams:               Various optional CSV parameters:
        :param delimiter:       CSV field delimiter
        :param quotechar:       CSV quote character
        :param quoting:         CSV quote style
    :return: Table
    """

    f = open_file(in_file, file_mode='r', encoding=encoding, newline=newline)
    _data = csv.reader(f, dialect=dialect, **fmtparams)
    t = Table(data=list(_data), name=name, detect_str_types=detect_str_types)
    close_file(f)
    return t


# -------------------------------------------------------------------------------------------- #
def read_json(in_file=None, name='', detect_str_types=False):
    """ Read JSON data from file

    :param in_file:         Filename to read JSON from
    :param name:            Table name to assign
    :param detect_str_types:    Detect and correct types of data, default - False
    :return                 Table
    """

    _data = {}
    f = open_file(file_name=in_file, file_mode='r')
    try:
        _data = json.load(f)
    except (IOError, OSError) as _err:
        print(f'FATAL@Table.read_json(): Unable to load JSON structure: {_err}')
    t = Table(data=_data, name=name, detect_str_types=detect_str_types)
    close_file(f)
    return t


# ------------------------------------------------------------------------------------------------ #
class EvalCtrl:

    """
    Control eval() function with white/black lists
    """

    blacklist = ['call(', 'popen(', 'Popen(', 'run(', 'system(']

    # -------------------------------------------------------------------------------------------- #
    def blacklisted(self, stanza):
        """
        Checks if there is any of the blacklised words in stanza

        :param stanza:      String to sanitize
        :return:            Boolean and the first blacklisted word
        """

        for word in self.blacklist:
            if word in stanza.replace(' ', '').replace('\t', ''):
                return True, word
        return False, None

    # -------------------------------------------------------------------------------------------- #
    def blacklist_add(self, word):
        """
        Add a new word into the black list

        :param word:    The word to add
        """

        if word not in self.blacklist:
            self.blacklist.append(word)

        return self

    # -------------------------------------------------------------------------------------------- #
    def blacklist_remove(self, word):
        """
        Remove the word from the blacklist

        :param word:    The word to remove from the blacklist
        """

        if word in self.blacklist:
            self.blacklist.remove(word)

        return self


# ------------------------------------------------------------------------------------------------ #
class Table:
    """
    Represents an tSQLike Table object with the below structure:
        * name:         string()
        * table:        list(list_1() ... list_n())
            * header:   list()
            * row:      list()
        * timestamp:    integer()
        * rows:         integer()
        * cols:         integer()
    """

    # -------------------------------------------------------------------------------------------- #
    def __init__(self, data=None, name=None, detect_str_types=False, use_none=False):
        self.timestamp = int(time.time())
        self.name = name or str(self.timestamp)

        if not data:
            self.table = []
            self.header = []
            self.rows = 0
            self.cols = 0
        elif isinstance(data, list) and len(data):
            if isinstance(data[0], dict):                   # list(dicts())
                self.import_list_dicts(data, detect_str_types=detect_str_types, use_none=use_none)
            if isinstance(data[0], list):                   # list(lists())
                self.import_list_lists(data, detect_str_types=detect_str_types, use_none=use_none)
        elif isinstance(data, dict) and len(data):
            print(type(next(iter(data))))
            if isinstance(data[next(iter(data))], list):    # dict(lists()):
                self.import_dict_lists(data, detect_str_types=detect_str_types, use_none=use_none)
        else:
            raise ValueError('FATAL@Table.__init__: Unexpected data format')

        # TODO: Invent nice aliases for the methods
        # Method aliases - Import
        self.import_table = self.import_list_lists
        self.import_thashes = self.import_list_dicts
        self.import_htables = self.import_dict_lists
        # Export data
        self.export_table = self.export_list_lists
        self.export_thashes = self.export_list_dicts
        self.export_htables = self.export_dict_lists

    # -------------------------------------------------------------------------------------------- #
    def __repr__(self):
        return str(self.table)

    # -------------------------------------------------------------------------------------------- #
    def _redimension(self):
        """ Recalculate dimensions of the Table.table """

        self.rows = len(self.table)
        self.cols = self.rows and len(self.table[0]) or 0

    # -- Import methods -------------------------------------------------------------------------- #
    def import_list_dicts(self, data, name=None, detect_str_types=False, use_none=False):
        """
        Import a list of dictionaries

        :alias:                     import_thashes()
        :param data:                Data to import formatted as list of dictionaries
        :param name:                If not None, set it as the Table name
        :param detect_str_types:    Detect and correct types of data, default - False
        :param use_none:            Use None type for empty, i.e. '', strings
        :return:                    self
        """

        # Set a new Table name if requested
        if name:
            self.name = str(name)

        if isinstance(data, list) and len(data) and isinstance(data[0], dict):
            self.header = [self.name + TNAME_COLUMN_DELIMITER + str(f)
                           if TNAME_COLUMN_DELIMITER not in str(f) else f for f in (data[0].keys())]

            self.table = [list(r.values()) for r in data] if not detect_str_types else [
                [str_to_type(v, use_none) for v in r.values()] for r in data]

        else:
            raise ValueError('FATAL@Table.import_list_dicts: Unexpected data format')

        self._redimension()
        self.timestamp = int(time.time())

        return self

    # -------------------------------------------------------------------------------------------- #
    def import_dict_lists(self, data, name=None, detect_str_types=False, use_none=False):
        """
        Import a dictionary of lists
        """

        if name:
            self.name = name

        if isinstance(data, dict) and len(data) and isinstance(data[next(iter(data))], list):
            self.header = [self.name + TNAME_COLUMN_DELIMITER + str(h)
                           if TNAME_COLUMN_DELIMITER not in str(h) else str(h) for h in
                           list(data.keys())]

            self.table = [[None for _ in range(len(data.keys()))]
                          for _ in range(len(data[next(iter(data))]))]

            for c, f in enumerate(data.keys()):
                for r, v in enumerate(data[f]):
                    self.table[r][c] = v if not detect_str_types else str_to_type(v, use_none)
            self._redimension()
        else:
            raise ValueError('FATAL@Table.import_dict_lists: Unexpected data format')

        self.timestamp = int(time.time())
        return self

    # -------------------------------------------------------------------------------------------- #
    def import_list_lists(self, data, header=True, name=None,
                          detect_str_types=False, use_none=False):
        """
        Import list(list_1(), list_n()) with optional first row as the header

        :param data:            Data to import formatted as list of lists
        :param header:          If true, data to import HAS a header
        :param name:            If not None, set it as the Table name
        :param detect_str_types:    Detect and correct types of data, default - False
        :return:                self
        """

        # Set a new Table name if requested
        if name:
            self.name = str(name)

        if isinstance(data, list) and len(data) and isinstance(data[0], list):
            # TODO: Check all rows to be equal length
            if not detect_str_types:
                self.table = data[1:] if header else data
            else:
                self.table = [[str_to_type(v, use_none) for v in r] for r in data[1:]]

            self._redimension()

            # If table header is not properly initiated, make each column: "name.column"
            if header and data[0]:
                self.header = [self.name + TNAME_COLUMN_DELIMITER + str(f)
                               if TNAME_COLUMN_DELIMITER not in str(f) else f for f in data[0]]
            else:
                # Let's create a header, if there is no one
                self.header = [str(h) for h in range(self.cols)]
        else:
            raise ValueError('FATAL@Table.import_list_lists: Unexpected data format')

        self.timestamp = int(time.time())
        return self

    # -- Export data ----------------------------------------------------------------------------- #
    def export_list_dicts(self):
        """ Export as list of dictionaries """

        return [{self.header[c]: r[c] for c in range(self.cols)} for r in self.table]

    # -------------------------------------------------------------------------------------------- #
    def export_list_lists(self, header=True):
        """ Export Table """

        return [self.header] + self.table if header else self.table

    # -------------------------------------------------------------------------------------------- #
    def export_dict_lists(self):
        """ Export a dictionary of lists """

        return {self.header[c]: [self.table[r][c]
                                 for r in range(self.rows)] for c in range(self.cols)}

    # -------------------------------------------------------------------------------------------- #
    def write_csv(self, out_file=None, encoding=None,
                  dialect='excel', lineterminator=LINETERMINATOR, **fmtparams):

        """
        Make CSV from the Table object and write it to a file or stdout

        :param out_file:            Filename to write CSV data or None for stdout
        :param encoding:            Character encoding
        :param lineterminator:      Line ends
        :**fmtparams:               Various optional CSV parameters:
            :param delimiter:           CSV field delimiter
            :param quotechar:           CSV quote character
            :param quoting:             CSV quote style
        :return:                    Nothing
        """

        f = open_file(out_file, 'w', encoding=encoding)
        wr = csv.writer(f, dialect=dialect, lineterminator=lineterminator, **fmtparams)

        try:
            wr.writerow(self.header)                                # Write the header ...
            for r in self.table:                                    # and the body of the table
                wr.writerow(r)
        except BrokenPipeError as _err:
            print(f'FATAL@Table.write_csv: {_err}', file=sys.stderr)

        close_file(f)

    # -------------------------------------------------------------------------------------------- #
    def write_json(self, out_file=None, export_f='export_list_dicts()',
                   indent=None, separators=None, sort_keys=False, evalctrl=EvalCtrl()):
        """
        Make JSON from the Table object and write it to a file or stdout

        :param out_file:    Filename to write CSV data or None for stdout
        :param export_f:    Function with arguments, an internal "export_*" or an external one
        :param indent:      JSON indentation
        :param separators:  JSON separators tuple
        :param sort_keys:   Whether to sort keys or not
        :param evalctrl:    eval() controlling class
        :return: Nothing
        """

        # Usage example: t.write_json(out_file='1.json', export_f='export_dict_lists()')

        if export_f:
            bl = evalctrl.blacklisted(export_f)
            if bl[0]:
                raise ValueError(f'FATAL@Table.write_json: Found blacklisted expression: [{bl[1]}]')

            methods = [method for method in dir(self) if
                       method.startswith('export_') and callable(getattr(self, method))]

            if export_f.split('(')[0].strip() in methods:
                # Our internal export_* method
                export_f = 'self.' + export_f

            efunc = eval(compile(export_f, '<string>', 'eval'))
            f = open_file(out_file, 'w')
            try:
                f.write(json.dumps(efunc, indent=indent,
                                   separators=separators, sort_keys=sort_keys))
            except (IOError, OSError) as _err:
                print(f'FATAL@Table.write_json(): {_err}')
                sys.exit(1)

            close_file(f)

    # -------------------------------------------------------------------------------------------- #
    def write_json_lt(self, out_file=None, indent=None, separators=None, sort_keys=False):
        """
        Lite, no eval() version of write_json() method

        :param out_file:    Filename to write CSV data or None for stdout
        :param indent:      JSON indentation
        :param separators:  JSON separators tuple
        :param sort_keys:   Whether to sort keys or not
        :return: Nothing
        """

        f = open_file(out_file, 'w')
        try:
            f.write(json.dumps(self.export_list_dicts(), indent=indent,
                               separators=separators, sort_keys=sort_keys))
        except (IOError, OSError) as _err:
            print(f'FATAL@Table.write_json_lt(): {_err}')
            sys.exit(1)

        close_file(f)
        return self

    # -------------------------------------------------------------------------------------------- #
    def write_xml(self):
        """ Not implemented """
        # TODO: Implement me

    # -- Data processing ------------------------------------------------------------------------- #
    def join(self, table, on='', mode=JOIN_INNER, new_tname='', replace=False, evalctrl=EvalCtrl()):
        """Join two Tables (self and table) on an expression

        :param table:       Table to join self with
        :param on:          Valid Python expression
        :param mode:        Join mode
        :param new_tname:   Give a name of the returned Table
        :param replace:     Replace source with the new data or not
        :param evalctrl:    eval() controlling class
        :return:            self
        """

        # Replace 'on' to work with eval() on per row entry
        if on:
            bl = evalctrl.blacklisted(on)
            if bl[0]:
                raise ValueError(f'FATAL@Table.join: Found blacklisted expression: [{bl[1]}]')

            for column in self.header:
                if column in on:
                    on = on.replace(column, 'tl[' + str(self.header.index(column)) + ']')
            for column in table.header:
                if column in on:
                    on = on.replace(column, 'tr[' + str(table.header.index(column)) + ']')
        else:
            on = 'True'                             # Will perform FULL JOIN

        # Best performance of eval():
        # https://mezzantrop.wordpress.com/2024/05/08/beating-eval-slowness-in-python
        efunc = eval(compile('lambda tl, tr:' + on, '<string>', 'eval'))

        r_table = []
        tl_match = []
        tr_match = []

        # Concatenate table headers as row[0] of the results table
        r_table.append(self.header + table.header)

        # Inner JOIN
        for c_tl, tl in enumerate(self.table):
            for c_tr, tr in enumerate(table.table):
                if efunc(tl, tr):
                    r_table.append(tl + tr)
                    tl_match.append(c_tl)
                    tr_match.append(c_tr)
        if mode in (JOIN_LEFT, JOIN_FULL):
            for it in range(0, self.rows):
                if it not in tl_match:
                    r_table.append([self.table[it] + [None] * table.cols])
        if mode in (JOIN_RIGHT, JOIN_FULL):
            for it in range(0, table.rows):
                if it not in tr_match:
                    r_table.append([[None] * self.cols + table.table[it]])

        if replace:
            # Replace source - self - with the joined Table
            return Table.import_list_lists(self, name=new_tname if new_tname else
                                           self.name + TNAME_TNAME_DELIMITER + table.name,
                                           data=r_table)
        # Return a new Table
        return Table(name=new_tname if new_tname
                     else self.name + TNAME_TNAME_DELIMITER + table.name, data=r_table)

    # -------------------------------------------------------------------------------------------- #
    def join_lt(self, table, scol, tcol, mode=JOIN_INNER, new_tname='', replace=False):

        """
        Light, limited and safe Join, that doesn't use eval()
        :param table:       Table to join self with
        :param scol:        Self column to join on
        :param tcol:        Table column to join on
        :param mode:        Join mode
        :param new_tname:   Give a name of the returned Table
        :param replace:     Replace source with the new data or not
        :return:            self
        """

        lci = self.header.index(scol) if scol in self.header else None
        rci = table.header.index(tcol) if tcol in table.header else None

        if None in (lci, rci):
            return Table()

        r_table = []
        l_dict = {}
        r_dict = {}

        # Concatenate table headers as row[0] of the results table
        r_table.append(self.header + table.header)

        for tl in range(self.rows):
            if not l_dict.get(self.table[tl][lci]):
                l_dict[self.table[tl][lci]] = [self.table[tl]]
            else:
                l_dict[self.table[tl][lci]].append(self.table[tl])

        for tr in range(table.rows):
            if not r_dict.get(table.table[tr][rci]):
                r_dict[table.table[tr][rci]] = [table.table[tr]]
            else:
                r_dict[table.table[tr][rci]].append(table.table[tr])

        ldk = l_dict.keys()
        rdk = r_dict.keys()
        for lk in ldk:
            for rk in rdk:
                if lk == rk:
                    # Inner JOIN
                    for lv in l_dict[lk]:
                        for rv in r_dict[rk]:
                            r_table.append(lv + rv)
                    continue
                if mode in (JOIN_RIGHT, JOIN_FULL):
                    if rk not in ldk:
                        for rv in r_dict[rk]:
                            r_table.append([None] * self.cols + rv)
                    continue
            if mode in (JOIN_LEFT, JOIN_FULL):
                if lk not in rdk:
                    for lv in l_dict[lk]:
                        r_table.append(lv + [None] * table.cols)

        if replace:
            # Replace source - self - with the joined Table
            return Table.import_list_lists(self, name=new_tname if new_tname else
                                           self.name + TNAME_TNAME_DELIMITER + table.name,
                                           data=r_table)
        # Return a new Table
        return Table(name=new_tname if new_tname
                     else self.name + TNAME_TNAME_DELIMITER + table.name, data=r_table)

    # -------------------------------------------------------------------------------------------- #
    def select(self, columns='*', where='', new_tname='', evalctrl=EvalCtrl()):

        """Select one or more columns from the Table if condition "where" is met.
        Return a new Table object

        :param columns:     Columns of the Table or '*' to return
        :param where:       Valid Python expression
        :param new_tname:   Give a name of the returned Table
        :param evalctrl:    eval() controlling class
        :return:            A new Table object
        """

        r_table = [[]]
        r_columns = []
        columns = self.header if columns == '*' else columns.split(',')

        if where:
            bl = evalctrl.blacklisted(where)
            if bl[0]:
                raise ValueError(f'FATAL@select: Found blacklisted expression: [{bl[1]}]')

        for column in self.header:
            if column in columns:
                c_idx = self.header.index(column)
                if where:
                    where = where.replace(column, 'r[' + str(c_idx) + ']')
                r_table[0].append(column)
                r_columns.append(c_idx)

        if not where:
            where = 'True'

        efunc = eval(compile('lambda r:' + where, '<string>', 'eval'))

        return Table(name=new_tname if new_tname else
                     self.name + TNAME_TNAME_DELIMITER + str(self.timestamp),
                     data=r_table + [[r[c] for c in r_columns] for r in self.table if efunc(r)])

    # -------------------------------------------------------------------------------------------- #
    def select_lt(self, columns='*', where='', comp='==', val='', new_tname=''):
        """ eval()-free version of select()

        :param columns:     Columns of the Table or '*' to return
        :param where:       Column name
        :param comp:        Comparison or membership operator
        :param val:         Value to compare with
        :param new_tname:   Give a name of the returned Table
        :return:            A new Table object
        """

        r_table = [[]]
        r_columns = []
        columns = self.header if columns in ('*', '') else columns.split(',')

        for column in self.header:
            if column in columns:
                r_table[0].append(column)
                r_columns.append(self.header.index(column))

        if not where or not comp or not val:
            return Table(name=new_tname if new_tname else
                         self.name + TNAME_TNAME_DELIMITER + str(self.timestamp),
                         data=r_table + [[r[c] for c in r_columns] for r in self.table])

        scol_idx = self.header.index(where)
        _type = type(val)
        return Table(name=new_tname if new_tname else
                     self.name + TNAME_TNAME_DELIMITER + str(self.timestamp),
                     data=r_table + [[r[c] for c in r_columns]
                                     for r in self.table
                                     if comp == '==' and _type(r[scol_idx]) == val or
                                     comp == '!=' and _type(r[scol_idx]) != val or
                                     comp == '>' and _type(r[scol_idx]) > val or
                                     comp == '<' and _type(r[scol_idx]) < val or
                                     comp == '>=' and _type(r[scol_idx]) >= val or
                                     comp == '<=' and _type(r[scol_idx]) <= val or
                                     comp == 'in' and _type(r[scol_idx]) in val or
                                     comp == 'not in' and _type(r[scol_idx]) not in val])

    # -------------------------------------------------------------------------------------------- #
    def order_by(self, column='', direction=ORDER_BY_INC, new_tname=''):
        """
        ORDER BY primitive of SQL SELECT

        :param column:      Order by this column
        :param direction:   Sort direction ORDER_BY_INC or ORDER_BY_DEC to specify sorting order
        :param new_tname:   Give a new name for the returned Table
        :return:            A new Table object
        """

        # Extract a column referenced by order_by and sort it
        sl = [(self.table[r][self.header.index(column)], r) for r in range(self.rows)]
        sl.sort()
        if direction != ORDER_BY_INC:               # Assuming the decreasing order is desired
            sl = sl[::-1]

        return Table(name=new_tname if new_tname else
                     self.name + TNAME_TNAME_DELIMITER + str(self.timestamp),
                     data=[self.header] + [[self.table[r[1]][c]
                                            for c in range(self.cols)] for r in sl])

    # -------------------------------------------------------------------------------------------- #
    def group_by(self, column='', function=None, ftarget=None, new_tname=''):
        """
        GROUP BY primitive of SQL SELECT

        :param column:      Group by this column
        :param function:    Aggregate function to apply
        :param ftarget:     Column to apply aggregate function
        :param new_tname:   Give a new name for the returned Table
        :return:            A new Table object
        """

        gd = {r[self.header.index(column)]: function(r[self.header.index(ftarget)])
              for r in self.table}

        return Table(name=new_tname if new_tname else
                     self.name + TNAME_TNAME_DELIMITER + str(self.timestamp),
                     data=[[column, ftarget]] + [[k, v] for k, v in gd.items()])


# -- MAIN starts here ---------------------------------------------------------------------------- #
if __name__ == "__main__":
    print(f'tSQLike (https://github.com/mezantrop/tSQLike) version: {__version__}\n\n')
    print('This is a Python3 library module.')
    print('To use tSQLike in the code, import it:\n\nfrom tsqlike import tsqlike')
