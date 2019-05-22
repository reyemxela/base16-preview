#!/usr/bin/python3

import re
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('inputfile', help='Input .yaml file', type=argparse.FileType('r'))
parser.add_argument('-o', '--output', dest='outputfile', help='Output file (default: ./output.svg)', default='./output.svg', type=argparse.FileType('w'))
parser.add_argument('-r', '--rows', dest='rows', help='Number of rows in the output image', default='2', type=int, metavar='N')
parser.add_argument('-b', '--bordersize', dest='bordersize', help='Size of border padding', default='30', type=int, metavar='N')
parser.add_argument('-t', '--tilesize', dest='tilesize', help='Size of the individual color tiles', default='45', type=int, metavar='N')
parser.add_argument('-g', '--gapsize', dest='gapsize', help='Size of the padding between tiles', default='15', type=int, metavar='N')

args = parser.parse_args()

rows = args.rows
bordersize = args.bordersize
tilesize = args.tilesize
gapsize = args.gapsize

f = args.inputfile
o = args.outputfile

colors = []
for line in f.readlines():
    if re.match('base', line):
        colors.append("#" + re.split('base0.*"(.*)".*', line)[1])

numcolors = len(colors) #16
tilesinrow = int(numcolors / rows)

width = (tilesinrow*tilesize) + ((tilesinrow+1)*gapsize) + (bordersize * 2)
height = (rows*tilesize) + ((rows+1)*gapsize) + (bordersize * 2)

output = ''
output += '<?xml version="1.0" encoding="UTF-8" ?>\n'
output += '<svg width="{}" height="{}" xmlns="http://www.w3.org/2000/svg">\n'.format(width, height)
output += '<rect x="0" y="0" width="{}" height="{}" style="fill:{}" />\n'.format(width, height, colors[0])

tiley = -1
tilex = 0
for i in range(numcolors):
    if i % tilesinrow == 0:
        tiley += 1
        tilex = 0
    x = bordersize + gapsize + ( gapsize*tilex ) + ( tilesize*tilex )
    y = bordersize + gapsize + ( gapsize*tiley ) + ( tilesize*tiley )
    output += '<rect x="{}" y="{}" width="{}" height="{}" style="fill:{}" />\n'.format(x, y, tilesize, tilesize, colors[i])
    tilex += 1

output += '</svg>\n'
o.write(output)
