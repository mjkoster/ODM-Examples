"""
txt2json.py
jsonify.py

convert a txt format file to json

bugs:
- handle spaces in keys

"""

import json, string, sys, collections


test_data = \
"""
/* this is a comment block */
info {
  title/**/
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
test_compact = \
"""
info{title"Example file for ODM Simple JSON Definition Format"version"20190424"copyright"Copyright 2019 Example Corp. All rights reserved."license http://example.com/license}namespace{st http://example.com/capability/odm}defaultnamespace st
odmObject{Switch{odmProperty{value{type string enum[on off]}}odmAction{on{}off{}}}}
"""

"""
raw input generator for string, with a previous (backspace) feature
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


"""
The token buffer is a generator with a previous (backspace) feature

The output from the char scanner is tokenized and inserted into the token buffer,
and contains unquoted strings, quoted strings, and block delimiters {}[]
"""
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


"""
called by the scanner when an opening DQUOTE is encountered, makes a token of everything until the closing DQUOTE,
and puts it into the tokenbuffer with enclosing quotes
"""
def quotestring(input_gen):
    result = ""
    nextchar = input_gen.next()
    while ( '"' != nextchar ) and ( -1 != nextchar ) :
        result += nextchar
        nextchar = input_gen.next()
    return '"' + result + '"'


"""
called by the scanner when a non-whitespace char is encountered, signifying the beginning of a string
in the input. follow until a whitespace char or a block delimiter is encountered

when a block delimiter token is encountered, the generator is backed up so the caller can process it

JSON and JSON schema processing will complete the block closure checking for now
"""
def naturalstring(character,input_gen):
    result = "" + character
    nextchar = input_gen.next()
    while not nextchar in string.whitespace :
        if '/' == nextchar :
            if '*' == input_gen.next() :
                input_gen.prev()
                input_gen.prev()
                return result
            else :
                input_gen.prev()
        elif nextchar in "{}[]" or '"' == nextchar:
            input_gen.prev()
            return result
        result += nextchar
        nextchar = input_gen.next()
    return result

def skip_comment(input_gen):
    while True :
        nextchar = input_gen.next()
        if '*' == nextchar :
            if '/' == input_gen.next():
                return

"""
character scanner
apply quoted string rule first, then block delimiter processing (insert block delimiters as tokens)
then process natural strings by placing into the token buffer
"""
def scantokens(input_string):
    input_gen = input(input_string)
    buffer = tokenbuffer()
    try:
        nextchar = input_gen.next()
    except StopIteration:
        return buffer
    while True:
        if '/' == nextchar :
            if '*' == input_gen.next() :
                skip_comment(input_gen)
            else :
                input_gen.prev()
        elif '"' == nextchar :
            buffer.addtoken(quotestring(input_gen))
        elif nextchar in "{}[]":
            buffer.addtoken(nextchar)
        elif ( nextchar in string.printable and not nextchar in string.whitespace ):
            buffer.addtoken(naturalstring(nextchar,input_gen))
        try:
            nextchar = input_gen.next()
        except StopIteration:
            return buffer


"""
process objects signified by open curly brace token {
use ordered dictionary to preserve source file ordering
store the key and its typed value in the dictionary
process all keys until closing curly brace token } is encountered

This is also the entry point for processing TDL instances. The top level is
by default an object, and is currently required to be an object
"""
def object(buffer):
    object = collections.OrderedDict()
    key = ""
    while "}" != key :
        try:
            key = buffer.next()
        except StopIteration:
            return object
        if key != "}":
            object[key] = value(buffer.next(), buffer)
        else:
            return object


"""
process arrays as lists of values starting after opening square bracket token [ is encountered
end array processing when closing square bracket token ] is encountered
"""
def array(buffer):
    array = []
    item = ""
    while "]" != item :
        item = buffer.next()
        if "]" != item :
            array.append(value(item, buffer))
    return array


"""
process a value, either an item of an object or an item of an array
we need the item and the buffer to handle array and object type items
processing order is important, to handle numbers and boolean
before stripping quotes from quoted strings, to enable quoting
numbers and boolean names e.g.schemas
"""
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


"""
test to see if it can be converted to int
"""
def isinteger(string):
    try:
        int(string)
    except ValueError:
        return False
    else:
        return True
"""
test to see if it can be converted to float (also fixed point)
"""


def isfloat(string):
    try:
        float(string)
    except ValueError:
        return False
    else:
        return True


"""
usage python jsonify.py <input TDL filename> <output json filename, including the .json extension>
"""
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
