
import numpy as np
import csv
import datetime
import argparse    # 1. argparseをインポート

import matplotlib
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser(description='Create gait chart figure')    # 2. パーサを作る
parser.add_argument('filename')    # 必須の引数を追加
parser.add_argument('-o','--outfilename', default='output.pdf')
parser.add_argument('-t', '--time', action='store_true')
parser.add_argument('-f', '--frame', action='store_true')
args = parser.parse_args()

data =[]

with open(args.filename, 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        tmp=[int(row[0])]
        tmp.append( datetime.datetime.strptime(row[1], "%H:%M:%S.%f") )
        tmp.append(int(row[2]))
        for i in range(3,len(row)):
            tmp.append(int(row[i]))
        data.append(tmp)



startMframe = data[0][2]
lastMframe = data[-1][2]
legNum = len(data[0])-3

#print(startMframe)
#print(lastMframe)
#print(legNum)

fig= plt.figure(figsize=(10, 5))
ax = fig.add_subplot(111)
ax.set_xlim(startMframe, lastMframe)
ax.set_ylim(0,legNum)
plt.tick_params(labelleft=False)

for f in range(len(data)-1):
    for l in range(legNum):
        if data[f][l+3] == 1:
            rect = plt.Rectangle((data[f][2],5-l),data[f+1][2]-data[f][2],1,fc="#000000")
            ax.add_patch(rect)

plt.savefig(args.outfilename)
plt.show(block=False)
input("Enter to close")
plt.close()
