#!/usr/bin/python3

# HACK

in_f = open("dump.sql", "r")

lines = in_f.read().split('\n')

for line in lines:
    line = line.strip()

    while '"["' in line and not '"[\\"' in line:
        part_to_replace = '"[' + line.split('"[')[-1].split(']"')[0] + ']"'
        replace_with = '"[' + part_to_replace.replace('"', '\\"') + ']"'
        line = line.replace(part_to_replace, replace_with)

    line = line.replace('["11", "22"]', '[\\"11\\", \\"22\\"]')
    line = line.replace('["11", "22", "81"]', '[\\"11\\", \\"22\\", \\"81\\"]')
    line = line.replace('[\\"[\\"', '"[\\"')
    line = line.replace('\\"]\\"]', '\\"]')
    line = line.replace('""', '"')

    print(line)

in_f.close()
