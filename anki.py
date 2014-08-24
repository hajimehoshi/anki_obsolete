#!/usr/bin/env python

import datetime
import math

class Item(object):
    def __init__(self, number, round, lastDate):
        self._number   = number
        self._round    = round
        self._lastDate = lastDate

    @property
    def number(self):
        return self._number

    @property
    def round(self):
        return self._round

    @property
    def lastDate(self):
        return self._lastDate

    @property
    def nextDate(self):
        today = datetime.date.today
        if self._round <= 0:
            return self._lastDate
        r = self._round
        days = math.ceil(2.5 ** (r - 1)) + \
            ((self._number + r) % (r * 2 - 1)) - r + 1
        nextDate = self._lastDate + datetime.timedelta(days=days)
        return nextDate

class Project(object):
    def __init__(self, filepath):
        self._name   = None
        self._number = None
        self._items  = None
        import xml.dom.minidom
        dom = xml.dom.minidom.parse(filepath)
        self._projectNode = dom.getElementsByTagName('project')[0]

    @property
    def name(self):
        if self._name is None:
            nameNode = self._projectNode.getElementsByTagName('name')[0]
            self._name = nameNode.firstChild.data
        return self._name

    @property
    def number(self):
        if self._number is None:
            numberNode = self._projectNode.getElementsByTagName('number')[0]
            self._number = int(numberNode.firstChild.data)
        return self._number

    @property
    def items(self):
        if self._items is None:
            itemsNode = self._projectNode.getElementsByTagName('items')[0]
            itemNodes = itemsNode.getElementsByTagName('item')
            self._items = []
            for itemNode in itemNodes:
                numberNode   = itemNode.getAttribute('number')
                roundNode    = itemNode.getElementsByTagName('round')[0]
                lastDateNode = itemNode.getElementsByTagName('last-date')[0]
                lastDateStr = lastDateNode.firstChild.data
                lastDate = datetime.datetime.strptime(lastDateStr, '%Y-%m-%d')
                lastDate = datetime.date(lastDate.year, lastDate.month, lastDate.day)
                item = Item(int(numberNode),
                            int(roundNode.firstChild.data),
                            lastDate)
                self._items.append(item)
        import copy
        return copy.copy(self._items)

def main(argv):
    if len(argv) <= 1:
        return
    filepath = argv[1]
    project = Project(filepath)
    today = datetime.date.today()
    now = datetime.datetime.now()
    print '{0} ({1})'.format(project.name, project.number)
    print 'Today: {0}'.format(today.strftime('%Y-%m-%d'))
    print
    digits = int(math.log10(project.number)) + 1
    fmt = "\033[{0}m" + '{1:0' + str(digits) + 'd}: {2}  {3}  {4}'
    items = project.items
    items = sorted(items, key=lambda i: i.nextDate)
    itemSum = 0
    roundSum = 0
    for item in items:
        number = item.number
        round  = item.round
        roundSum += round
        if 0 < item.round:
            itemSum += 1
        if 5 <= round:
            continue
        if item.nextDate <= today:
            color = "31" # Red
        else:
            lastDate = item.lastDate
            minDatetime = datetime.datetime(lastDate.year, lastDate.month, lastDate.day)
            maxDatetime = minDatetime + datetime.timedelta(days=1, hours=6)
            if minDatetime <= now and now < maxDatetime:
                color = "32" # Green
            else:
                color = "0"
        lastDateStr = item.lastDate.strftime('%Y-%m-%d')
        nextDateStr = item.nextDate.strftime('%Y-%m-%d')
        print fmt.format(color, number, round, lastDateStr, nextDateStr)
    print
    print "Sum of items: {0}".format(itemSum)
    print "Sum of rounds: {0}".format(roundSum)

if __name__ == '__main__':
    import sys
    main(sys.argv)
