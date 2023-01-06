#!/usr/bin/python3

import csv
import os

class AbstractExporter(object):
    def start(self):
        raise NotImplementedError()

    def write_row(self, tablename, row):
        raise NotImplementedError()

    def write_rows(self, tablename, rows):
        raise NotImplementedError()

    def finalise(self):
        raise NotImplementedError()

class SQLDumpExporter(AbstractExporter):
    out_file_path = None
    _out_f = None

    def __init__(self, out_file_path):
        super().__init__()
        self.out_file_path = out_file_path

    def start(self):
        self._out_f = open(self.out_file_path, "w", encoding="utf-8")

    def write_row(self, tablename, row):
        for k in list(row.keys()):
            v = row.get(k)
            if v is None:
                del row[k]
                continue
            
            if type(v) == str and '"' in v:
                v = v.replace('"', '\\"')
                row[k] = v

        fieldnames = list(row.keys())
        cols_comma_sep = ", ".join(fieldnames)
        values = list(map(lambda f: '"' + str(row.get(f, "")) + '"', fieldnames))
        values_comma_sep = ", ".join(values)

        update_comma_sep = []
        for k in fieldnames:
            update_comma_sep.append("{} = \"{}\"".format(k, row[k]))

        update_comma_sep = ", ".join(update_comma_sep)

        sql = "INSERT INTO {} ({}) VALUES ({}) ON DUPLICATE KEY UPDATE {};\n".format(
            tablename, cols_comma_sep, values_comma_sep, update_comma_sep
        )
        self._out_f.write(sql)

    def write_rows(self, tablename, rows):
        if type(rows) == dict:
            self.write_row(tablename, rows)
            return

        # TODO: write multiple rows in a single SQL query.
        for row in rows:
            self.write_row(tablename, row)

    def finalise(self):
        self._out_f.close()
