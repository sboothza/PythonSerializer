# My Simple Json Serializer and Naming Utilities
Anybody who's actually tried to use `json.dumps` and `json.loads` knows that it only works properly with dictionaries.  Any strongly-typed stuff just breaks.  And forget about deserializing - you just get dictionaries again.   
That's fine for some people, but I wanted something that would actually serialize **any** object, and be able to deserialize it back into an instance of the original class.


## The main class is the serializer - HardSerializer
It's hard-typed, doesn't try to infer anything about the class to deserialize.
It's fairly picky about the format of the class - you need to use typing **EVERYWHERE** or it doesn't work.  It uses a lot of reflection to 
figure stuff out, and the typing is critical.  
  
It can figure out enums, lists, hierarchies, inheritance, etc.    
**Note** It can't deserialize lists of a base type to different inherited types.  (later version with discriminators)   
The json is standard, no type-tags or anything, and compatible with other languages and libraries
like System.Text.Json or NewtonSoft in .NET

I haven't performance tested it, it's not the bottleneck in any of my projects though.  But python isn't particularly fast anyway, so I don't imagine it's as fast as the C# equivalent....

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

### Usage

Create the `Naming` class instance from the 2 dictionaries, the standard word list and the bigwords list.  
The standard list is just a list of words, 1 per line (like `account`)  
The big-word list is a list of comma-separated compound words (like `account,holder`) 
specifies common word combinations that confuse the main dictionary.  
Test words, and add them to the dictionary when it gets confused.

Create `Name` class instances by using `naming.string_to_name()` 
This will try to map words from the various dictionaries, and separate them into individual words that can be processed.  
The `Name` class instance has different methods on it like `Pascal`, `Snake`, etc.  

eg: `naming.string_to_name('accountholder').pascal()` returns `AccountHolder`
`naming.string_to_name('accountholder').snake()` returns `account_holder`


## Installation

`pip install sb-serializer`

