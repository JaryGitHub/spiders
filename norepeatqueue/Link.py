# ! /usr/bin/env python
# -*- coding: utf-8 -*-

class Link():

    def __init__(self):
        self.map = {}
        self.tail = 'head'
        self.map['head'] = {'next':'null'}

    def __contains__(self, item):
        return item in self.map

    def __len__(self):
        return len(self.map) - 1

    def getHead(self):
        return self.map['head']['next']

    def isEmpty(self):
        if self.getHead() == 'null':
            return True
        else:
            return False

    def clearLink(self):
        self.map.clear()

    def getTail(self):
        self.tail

    def add(self,string):
        if string not in self.map:
            self.map[string] = {'next':'null'}
            self.map[self.tail]['next'] = string
            self.tail = string

    def pop(self):
        if not self.isEmpty():
            head_task = self.map['head']['next']
            self.map['head']['next'] = self.map[head_task]['next']
            del self.map[head_task]
            if head_task == self.tail:
                self.tail = 'head'
            return head_task
        return None






