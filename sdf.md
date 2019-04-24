# A Simple Definition Format for One Data Model definitions

## Introduction

The Simple Definition Format is meant to be used as a format for domain experts
to use in the creation and maintenance of OneDM definitions.

This document describes definitions of OneDM Objects and their associated
Events, Actions, Properties, and Data types.

The JSON format of an SDF definition is described in this document.

## SDF structure

A SDF definition file has two sections, the information block and the definitions
section.

### Information block
The information block contains generic meta data for the file itself
and all included definitions.

The keyword that defines an information block is "info". It contains a set of
key-value pairs that represent qualities that apply to the included definition.

Qualities of the information block are shown in the following table:

Title
Version
Copyright
License

### Definitions block

The Definitions block contains the namespace and default namespace declarations.
The namespace declaration is a map containing one or more definitions of short
names for URIs. The defaultnamespace declaration defines one of the short names
in the namespace map to be the default namespace.

The following example declares a set of namespaces and defines  "st"" as the
default namespace.
```
"namespace": {
  "st": "smartthings.example.com/odmterms",
  "zcl"" "zigbee.example.com/odm"
},
"defaultnamespace": "st",
```
The definitions block contains one or more type definitions according to the
class name keywords for type definition (see below).

Each class may have zero or more type definitions associated with it. Each defined
identifier creates a new type and has a scope of the current definition block.
A definition may in turn contain other definitions. Each definition consists of
the newly defined identifier and a set of key value pairs that represent the
defined qualities and contained type definitions.

for example, an Object definition looks like this:

```
"object": {
  "foo": {
    "id": 3001,
    "property": {
      "bar": {
        "type": "boolean"
        "id": 5150
      }
    }
  }
}
```
An Object "foo" is defined in the default namespace, with an ID of 3001,
containing a property "foo.bar", with an ID of 5150 and of type boolean.

## Keywords for type definitions

The following SDF keywords are used to create type definitions in the target
namespace. The target namespace is defined by the default namespace, or by
an explicit prefix on the identifier separated by a semicolon ":". For example
if the default namespace in the example above is "baz", then you could refer
to "baz:foo.bar" to point to the property "bar" in the namespace.

### Object

- Description
The object keyword denotes one or more Object definitions. A object may contain
or include definitions of events, actions, properties, and data types.

- Qualities of Object

| Quality | Type | Required | Description |
|---|---|---|---|
|id| integer, string | no | internal unique identifier for the definition |
|name|string|no|human readable name|
|description|string|no|human readable description|

- Types Object may contain

|Type|
|---|
|property|
|action|
|event|
|data|


### Property

- Description
The property keyword denotes zero or more property definitions.

- Qualities of Property

| Quality | Type | Required | Description |
|---|---|---|---|
|id| integer, string | no | internal unique identifier for the definition |
|name|string|no|human readable name|
|description|string|no|human readable description|

- Types Property may contain
|Type|
|---|
|data|

### Action

- Description

- Qualities of Action

| Quality | Type | Required | Description |
|---|---|---|---|
|id| integer, string | no | internal unique identifier for the definition |
|name|string|no|human readable name|
|description|string|no|human readable description|

- Types Action may contain

|Type|
|---|
|data|


### Event

- Description

- Qualities of Event

| Quality | Type | Required | Description |
|---|---|---|---|
|id| integer, string | no | internal unique identifier for the definition |
|name|string|no|human readable name|
|description|string|no|human readable description|

- Types Event may contain

|Type|
|---|
|data|


### Data

- Description

- Qualities of Data

| Quality | Type | Required | Description |
|---|---|---|---|
|id| integer, string | no | internal unique identifier for the definition |
|name|string|no|human readable name|
|description|string|no|human readable description|

- Types Data may contain

|Type|
|---|
|N/A|


## Scope of Identifiers
### namespace resolution order:
0. identifiers with an explicit namespace prefix
1. keywords and quality names in the ODM and JSON Schema namespaces, defined in the JSON Schema for SDF
2. identifier defined in the most local block
3. identifier defined in the next closest enclosing block recursively
4. identifier defined in the file
5. identifier defined in the default namespace

### Identifier name expansion from JSON path

When a type is defined, the identifier is internally prefixed with the JSON path
that locates the definition in the file.

Types defined at the top level in the file go into the namespace as they are.

Types defined within another definition are prefixed with the path to the
enclosing definition. For example, if there is an Object "foo" defined, and an
definition for "bar" with Object foo, the path to bar will be "foo.bar" within
the default namespace. The Action name "foo.bar" can be used as a reference
within some other definition, provided that the scope can be resolved.

## example OneDM Object Definition for the SmartThings Switch Capability:
```
{
  "info": {
    "title": "Example file for ODM Simple JSON Definition Format",
    "version": "20190424",
    "copyright": "Copyright 2019 Example Corp. All rights reserved.",
    "license": "http://example.com/license"
  },
  "namespace": {
    "st": "http://example.com/capability/odm"
  },
  "defaultNamespace": "st",
  "object": {
    "Switch": {
      "property": {
        "value": {
          "type": "string",
          "enum": ["on", "off"]
        }
      },
      "action": {
        "on": {},
        "off": {}
      }
    }
  }
}
```
