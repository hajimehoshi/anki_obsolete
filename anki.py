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
        nextDate = (self._lastDate + datetime.timedelta(days=days)).date()
        return nextDate

class Project(object):
    def __init__(self, filepath):
        self._name   = None
        self._number = None
        self._items  = None
        import xml.dom.minidom
        dom = xml.dom.minidom.parse(filepath)
        projectNode = dom.getElementsByTagName('project')[0]
        self._nameNode   = projectNode.getElementsByTagName('name')[0]
        self._numberNode = projectNode.getElementsByTagName('number')[0]
        itemsNode = projectNode.getElementsByTagName('items')[0]
        itemNodes = itemsNode.getElementsByTagName('item')
        self._itemNodes = itemNodes

    @property
    def name(self):
        if self._name is None:
            self._name = self._nameNode.firstChild.data
        return self._name

    @property
    def number(self):
        if self._number is None:
            self._number = int(self._numberNode.firstChild.data)
        return self._number

    @property
    def items(self):
        if self._items is None:
            self._items = []
            for itemNode in self._itemNodes:
                numberNode   = itemNode.getAttribute('number')
                roundNode    = itemNode.getElementsByTagName('round')[0]
                lastDateNode = itemNode.getElementsByTagName('last-date')[0]
                lastDateStr = lastDateNode.firstChild.data
                lastDate = datetime.datetime.strptime(lastDateStr, '%Y-%m-%d')
                item = Item(int(numberNode),
                            int(roundNode.firstChild.data),
                            lastDate)
                self._items.append(item)
        import copy
        return copy.copy(self._items)

def main(argv):
    if argv <= 1:
        return
    filepath = argv[1]
    project = Project(filepath)
    print '{0} ({1})'.format(project.name, project.number)
    print 'Today: {0}'.format(datetime.date.today().strftime('%Y-%m-%d'))
    print
    digits = int(math.log10(project.number)) + 1
    fmt = '{0} {1:0' + str(digits) + 'd}: {2}  {3}  {4}'
    items = project.items
    items = sorted(items, key=lambda i: i.nextDate)
    for item in items:
        number   = item.number
        round    = item.round
        lastDate = item.lastDate.strftime('%Y-%m-%d')
        nextDate = item.nextDate.strftime('%Y-%m-%d')
        if item.nextDate <= datetime.date.today():
            status = '*'
        else:
            status = ' '
        print fmt.format(status, number, round, lastDate, nextDate)

if __name__ == '__main__':
    import sys
    main(sys.argv)
