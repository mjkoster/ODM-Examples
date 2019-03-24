# A high level language for Thing Definition

### example Thing Definition from SmartThings Switch Capability:
```
context http://onedm.org#tdl
uses [odm js]
scope st
define [
    Switch {
        extends Capability
        hasProperty Switch.value
        hasAction [Switch.on Switch.off]
    }
    Switch.value {
        extends Property
        hasDataItem Switch.valueData
    }
    Switch.on {
        extends Action
    }
    Switch.off {
        extends Action
    }
    Switch.valueData {
        extends DataItem
        type string
        enum [on off]
    }
]
```
### keywords:

context - works like JSON-LD context to define namespaces and terms
uses - specifies one or more default source namespaces, evaluated in order
scope - specifies default namespace that definitions are added to
define - creates a definition in some namespace, args are a new term and a definition block
extends - specifies a class template to use in the definition block

### structure:

keywords
[ list ] items determined by keyword, use where multiple items are allowed
{ block } contains key-value pairs, whitespace delimited, according to the class template defined by extends

### namespace resolution order:
0. keywords
1. local block
2. enclosing block
3. namespace declared with scope keyword
4. namespaces declared with uses keyword, in declared order

additional RDF terms can be added in the definition block:
```
define [
    Switch {
        extends Capability
        comment "Basic on/off capability"
        label "SmartThings Switch"
        seeAlso [ocf:Switch.Binary zcl:onoff]
        hasProperty Switch.value
        hasAction [Switch.on Switch.off]
    }
```
Capabilities can be extracted from ecosystem definitions and augnebted in TDL,
then written back to the ecosystem format with annotation and augmentation

### Extracted definition from OCF Swagger file:
```
define [
    oic.r.switch.binary {
        exends Capability
        hasProperty oic.r.switch.binary.value
    }
    oic.r.switch.binary.value {
        extends Property
        hasDataItem oic.r.switch.binary.valueData
    }
    oic.r.switch.binary.valueData {
        extends DataItem
        type boolean
    }
]
```
### Augmanted definition adding turnOn and turnOff actions:
```
define [
    oic.r.switch.binary {
        exends Capability
        seeAlso [zcl:onoff st:Switch]
        hasProperty oic.r.switch.binary.value
    }
    oic.r.switch.binary.value {
        extends Property
        hasDataItem oic.r.switch.binary.valueData
    }
    oic.r.switch.binary.valueData {
        extends DataItem
        type boolean
    }
    oic.r.switch.binary.turnOn {
        extends Action
        seeAlso [zcl:onoff.on st:Switch.on]
        hasDataItem oic.r.switch.binary.valueData.turnOn
    }
    oic.r.switch.binary.turnOff {
        extends Action
        seeAlso [zcl:onoff.off st:switch.off]
        hasDataItem oic.r.switch.binary.valueData.turnOff
    }
    oic.r.switch.binary.valueData.turnOn {
        extends DataItem
        type boolean
        const true
    }
    oic.r.switch.binary.valueData.turnOff {
        extends DataItem
        type boolean
        const false
    }
]
```
### alternative with inline DataItem Definition:
```
    oic.r.switch.binary.turnOn {
        extends Action
        seeAlso [zcl:onoff.on st:Switch.on]
        hasDataItem {type boolean const true}
    }
    oic.r.switch.binary.turnOff {
        extends Action
        seeAlso [zcl:onoff.off st:switch.off]
        hasDataItem {type boolean const false}
    }
```
