"""
convert a tdl format thing definition to json

bugs:
- key order is recursively or alphabetically sorted

"""
import json, string, sys


test_data = """
info {
  title
      "Example file for ODM Simple JSON Definition Format"
  version
      "20190424"
  copyright
      "Copyright 2019 Example Corp.
        All rights reserved."
  license
      http://example.com/license
}
namespace {
  st http://example.com/capability/odm
}
defaultnamespace st
object {
  Switch {
    property {
      value {
        type string
        enum [on off]
      }
    }
    action {
      on{}
      off{}
    }
  }
}
"""

class input():
    def __init__(self, string):
        self.buffer = list(string)
        self.index = 0
        
    def __iter__(self):
        return self
    
    def __next__(self):
        return self.next
    
    def next(self):
        self.index += 1
        if self.index <= len(self.buffer) : 
            return self.buffer[self.index-1]
        else :
          raise StopIteration
      
    def prev(self):
        if self.index > 0 :
            self.index -= 1
        
class tokenbuffer():
    def __init__(self):
        self.buffer = []
        self.index = 0
        
    def __iter__(self):
        return self
    
    def next(self):
        self.index += 1
        if self.index <= len(self.buffer) : 
            return self.buffer[self.index-1]
        else :
          raise StopIteration
    def prev(self):
        if self.index > 0 :
            self.index -= 1
    
    def addtoken(self, token):
        self.buffer.append(token)


def quotestring(input_gen):
    result = ""
    nextchar = input_gen.next()
    while ( '"' != nextchar ) and ( -1 != nextchar ) :
        result += nextchar
        nextchar = input_gen.next()
    return '"' + result + '"'

def naturalstring(character,input_gen):
    result = "" + character
    nextchar = input_gen.next()
    while (nextchar not in string.whitespace) :
        if "[" == nextchar or "]" == nextchar or "{" == nextchar or "}" == nextchar:
            input_gen.prev()
            return result
        result += nextchar
        nextchar = input_gen.next()
    return result

def scantokens(input_string):
    input_gen = input(input_string)
    buffer = tokenbuffer()
    try:
        nextchar = input_gen.next()
    except StopIteration:
        return buffer
    while True:
        if '"' == nextchar :
            buffer.addtoken(quotestring(input_gen))
        elif ("{" == nextchar or "}" == nextchar or "[" == nextchar or "]" == nextchar ):
            buffer.addtoken(nextchar)
        elif ( nextchar in string.printable and not nextchar in string.whitespace ):
            buffer.addtoken(naturalstring(nextchar,input_gen))          
        try: 
            nextchar = input_gen.next()
        except StopIteration:
            return buffer

def object(buffer):
    object = {}
    key = ""
    while "}" != key :
        try:
            key = buffer.next()
        except StopIteration:
            return object
        if key != "}":
            object[key] = value(buffer.next(), buffer)
    return object

def array(buffer):
    array = []
    item = ""
    while "]" != item :
        item = buffer.next()
        if "]" != item :
            array.append(value(item, buffer))
    return array

def value(item, buffer):
    if "{" == item :
        return object(buffer)
    elif "[" == item :
        return array(buffer)
    elif isinteger(item) :
        return int(item)
    elif isfloat(item) :
        return float(item)
    elif "true" == item :
        return True
    elif "false" == item :
        return False
    elif any((c in '"') for c in item):
        return item.strip('"')
    else:
        return item 


def isinteger(string):
    try:
        int(string)
    except ValueError:
        return False
    else:
        return True

def isfloat(string):
    try:
        float(string)
    except ValueError:
        return False
    else:
        return True

if __name__ == '__main__' :
    if len(sys.argv) > 2:
        inputfilename = sys.argv[1]
        outputfilename = sys.argv[2]
        infile = open(inputfilename, "r")
        input_string = infile.read()
        outfile = open(outputfilename, "w")
        outfile.write(json.dumps(object(scantokens(input_string)), indent=2, sort_keys=False))
    elif len(sys.argv) > 1:
        inputfilename = sys.argv[1]
        infile = open(inputfilename, "r")
        input_string = infile.read()
        print json.dumps(object(scantokens(input_string)), indent=2, sort_keys=False)
    else:
        print json.dumps(object(scantokens(test_data)), indent=2, sort_keys=False)
                 

