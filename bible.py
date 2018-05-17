import io
import matplotlib

matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import collections
from scipy.stats.stats import pearsonr
import numpy as np
import pandas as pd


def getBookName(s):
    idx = s.find('|')
    return s[:idx]


# reverses string to find last '|' and returns words
def getListofWords(s):
    backwards = s[::-1]
    idx = backwards.find('|')
    backwords = backwards[:idx]
    return cleanWords(backwords[::-1].split())


def cleanWords(words):
    badChars = [',', '.', ':', ';', '\n', '-']
    for i in range(len(words)):
        for ch in badChars:
            if ch in words[i]:
                idx = words[i].find(ch)
                words[i] = words[i][:idx] + words[i][idx + 1:]
    return words


def compareBooks(book1, book2):
    points = []
    for item in ntWordCounts[book1]:
        word = item
        if item in ntWordCounts[book2] and len(word) > 0:
            points.append((ntWordCounts[book1][item], ntWordCounts[book2][item]))

    # for point in points:
    #     plt.scatter(point[0], point[1])
    # plt.savefig('myfilename.png')

    x, y = zip(*points)
    corr = pearsonr(x, y)[0]
    # if corr >= 0:
    #     print(book1, book2, round(corr, 3), len(x))
    return round(corr, 4)


author = {}
author['Act'] = 'Luke'
author['Co1'] = 'Paul'
author['Co2'] = 'Paul'
author['Col'] = 'Paul'
author['Eph'] = 'Paul'
author['Gal'] = 'Paul'
author['Heb'] = 'Unknown'
author['Jam'] = 'James'
author['Jde'] = 'Jude'
author['Jo1'] = 'John'
author['Jo2'] = 'John'
author['Jo3'] = 'John'
author['Joh'] = 'John'
author['Luk'] = 'Luke'
author['Mar'] = 'Mark'
author['Mat'] = 'Matthew'
author['Pe1'] = 'Peter'
author['Pe2'] = 'Peter'
author['Phi'] = 'Paul'
author['Plm'] = 'Combo'
author['Rev'] = 'John'
author['Rom'] = 'Paul'
author['Th1'] = 'Paul'
author['Th2'] = 'Paul'
author['Ti1'] = 'Paul'
author['Ti2'] = 'Paul'
author['Tit'] = 'Paul'


with io.open('ugntdat.txt') as f:
    lines = f.readlines()
    nt = {}
    book = getBookName(lines[0])
    words = []
    for line in lines:
        if getBookName(line) == book:
            words.extend(getListofWords(line))
        else:
            nt[book] = words
            book = getBookName(line)
            words = getListofWords(line)
    nt[book] = words


ntWordCounts = {}
for item in nt.items():
    ntWordCounts[item[0]] = collections.Counter(item[1])





d = {}
for book1 in sorted(ntWordCounts.keys()):
    rs = []
    for book2 in sorted(ntWordCounts.keys()):
        corr = compareBooks(book1, book2)
        if author[book1] == author[book2]:
            rs.append([corr])
        else:
            rs.append(corr)
    d[book1] = rs


df = pd.DataFrame(d, index=sorted(ntWordCounts.keys()))
df.to_csv('CorrelationTable.csv')

