import unittest

from enum import Enum

import uuid

from src.sb_serializer import HardSerializer


class TestEnum(Enum):
    Value1 = 1
    Value2 = 2
    Undefined = 0


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


class SerializerTests(unittest.TestCase):
    def test_basic(self):
        serializer = HardSerializer()
        tc = TestClass(12, "Bob", test_enum=TestEnum.Value1)
        json = serializer.serialize(tc)

        new_tc = serializer.de_serialize(json, TestClass)
        self.assertEqual(tc.id, new_tc.id)
        self.assertEqual(tc.name, new_tc.name)
        self.assertEqual(tc.guid, new_tc.guid)
        self.assertEqual(tc.test_enum, new_tc.test_enum)

    def test_hierarchy(self):
        serializer = HardSerializer()
        children = []
        children.append(TestClass(12, "Bob", test_enum=TestEnum.Value1))
        children.append(TestClass(13, "Bill", test_enum=TestEnum.Value2))
        children.append(TestClass(14, "Tom", test_enum=TestEnum.Value1))
        parent = ParentClass(5, "Parent", test_enum=TestEnum.Value1, children=children)

        json = serializer.serialize(parent)

        new_parent: ParentClass = serializer.de_serialize(json, ParentClass)
        self.assertEqual(parent.id, new_parent.id)
        self.assertEqual(parent.name, new_parent.name)
        self.assertEqual(parent.guid, new_parent.guid)
        self.assertEqual(parent.test_enum, new_parent.test_enum)

        self.assertEqual(len(parent.children), len(new_parent.children))
