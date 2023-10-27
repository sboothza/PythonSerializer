# My Simple Json Serializer and Naming Utilities

## The main class is the serializer - HardSerializer
It's not particularly hard, just doesn't try to infer the class to deserialize (like my previous iterations), you need to specify the class directly.
Also, it's fairly picky about the format of the class - you need to use typing **EVERYWHERE** or it doesn't work.  It uses a lot of reflection to 
figure stuff out, and the typing is critical.  
  
It can figure out enums, lists, hierarchies, etc.  Pretty powerful.  The json is standard, no tags or anything, and compatible with other languages and libraries
like System.Text.Json in .NET

It essentially converts the object model into dicts and then `json.dumps()` them to serialize, the reverse for deserialize.

### Usage
You need to specify the fields in the class definition as well as in the __init__ - like so:
```
class TestClass(object):
    id: int
    name: str
    guid: uuid.UUID
    test_enum: TestEnum

    def __init__(
        self,
        id: int = 0,
        name: str = "",
        guid: uuid.UUID = uuid.uuid4(),
        test_enum: TestEnum = TestEnum.Undefined,
    ):
        self.id = id
        self.name = name
        self.guid = guid
        self.test_enum = test_enum
```
Note the typing hints everywhere

It can handle hierarchies as long as the type hints are there:
```
class ParentClass(object):
    id: int
    name: str
    guid: uuid.UUID
    test_enum: TestEnum
    children: list[TestClass]

    def __init__(
        self,
        id: int = 0,
        name: str = "",
        guid: uuid.UUID = uuid.uuid4(),
        test_enum: TestEnum = TestEnum.Undefined,
        children: list[TestClass] = [],
    ):
        self.id = id
        self.name = name
        self.guid = guid
        self.test_enum = test_enum
        self.children = children
```

Unit tests are included to see usage, but the basics are:  
```
tc = TestClass(12, "Bob", test_enum=TestEnum.Value1)
json = serializer.serialize(tc)
new_tc = serializer.de_serialize(json, TestClass)
```
It will try to deserialize into the `TestClass`

## Naming
The naming is a bit weirder, and uses custom dictionaries to work - not sure how else to do it.    
The project originated from trying to form decent property names from database fieldnames.  

## Usage
Create the `Naming` class instance from the 2 dictionaries, the standard word list and the bigwords list (specifies common word combinations that are hard to infer)  
Create `Name` class instances by using `naming.string_to_name()`  
The `Name` class instance has different methods on it like `Pascal`, `Snake`, etc.  
Simple.


## Building
`python -m build `

## Deploying
`python -m twine upload --repository pypi dist/*`