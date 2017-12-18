

import argparse
import calendar
import json
import logging
import os
import re
import subprocess
import sys
import time

def parse_command_line_args():
    p = argparse.ArgumentParser()
    p.add_argument('-i', '--input', type=str, required=True, help='Input from previous step output')
    p.add_argument('-o', '--outdir', type=str, required=False, default='output', help='Local output directory [Default: ./output]')
    return p.parse_args()

def main():
    args = parse_command_line_args()

    with open(args.input) as f:
        products = json.load(f)

    products_by_date = {}
    products_by_grid = {}

    for p in products:
        name = p
        attrs = products[p]['attrs']
        files = products[p]['files']
        print(name)
        print(attrs)
        print(files)
        print('\n')
        add_by_date(products_by_date, name, attrs, files)

        with open(os.path.join('.', args.outdir, 'products_by_date.json'), 'w') as f:
            json.dump(products_by_date, f, indent=4)    


def add_by_date(output, name, attrs, files):
    # make a data structure like
    # output[year][month][day][grid][product]
    year = attrs['year']
    month = attrs['month']
    day = attrs['day']
    grid = attrs['grid']
    if not year in output:
        output[year] = {}
    if not month in output[year]:
        output[year][month] = {}
    if not day in output[year][month]:
        output[year][month][day] = {}
    if not grid in output[year][month][day]:
        output[year][month][day][grid] = {
            'name': name,
            'attrs': attrs,
            'files': files,
        }

# def add_by_grid(output, p):
#     if not p.grid in output:
#         output[p.grid] = {}

#     datestring = '%s%s%s' % (p.year, p.month, p.day)
#     if not datestring in output[p.grid]:
#         output[p.grid][datestring] = {
#             'name': 'S2%s_%s%s%s_lat%slon%s_T%s_ORB%s_%s%s' % (p.satellite, p.year, p.month, p.day, p.lat, p.lon, p.grid, p.orbit, p.original_projection, ('_%s' % (p.new_projection) if p.new_projection is not None else '')),
#             'satellite': 'sentinel-2%s' % (p.satellite.lower()),
#             'lat': p.lat,
#             'lon': p.lon,
#             'orbit': p.orbit,
#             'original_projection': p.original_projection,
#             'new_projection': p.original_projection       # Not a typo, this happens with Rockall
#         }

#     if p.new_projection is not None:
#         output[p.grid][datestring]['new_projection']: p.new_projection

#     if p.file_type == 'vmsk_sharp_rad_srefdem_stdsref':
#         output[p.grid][datestring]['product'] = {
#             'data': p.s3_key,
#             'size': sizeof_fmt(p.s3_size)
#         }
#     else:
#         output[p.grid][datestring][p.file_type] = {
#             'data': p.s3_key,
#             'size': sizeof_fmt(p.s3_size)
#         }

main()
