import unittest

from marci import ObjList, Capture


class TestCapture(unittest.TestCase):
  def test_object_growth(self):
    capture = Capture()
    capture.start()
    new_obj = dict()
    result = capture.end()
    self.assertTrue(new_obj in result)
    self.assertTrue(result not in result)
    self.assertTrue(capture not in result)


class TestObjList(unittest.TestCase):
  def test_new_list(self):
    list = ObjList()
    self.assertNotEqual(len(list), 0)

  def test_list_subtract(self):
    init_list = ObjList(True)
    init_list.append({'a': '1'})
    init_list.append({'b': '2'})
    init_list.append({'c': '3'})
    new_list = ObjList(True)
    new_list.append(init_list[0])
    new_list.append(init_list[2])
    subtracted = init_list - new_list
    self.assertEqual(len(subtracted), 1)
    self.assertTrue(init_list[1] in subtracted)

  def test_extract(self):
    test_list = ObjList().extract(dict)
    for item in test_list:
      self.assertEqual(type(item), dict)

  def test_extract_multi(self):
    test_list = ObjList().extract([dict, tuple])
    for item in test_list:
      self.assertTrue(type(item) is dict or type(item) is tuple)

  def test_sanitize(self):
    test_list = ObjList().sanitize(dict)
    for item in test_list:
      self.assertNotEqual(type(item), dict)

  def test_sanitize_multi(self):
    test_list = ObjList().sanitize([dict, tuple])
    for item in test_list:
      self.assertTrue(type(item) is not dict and type(item) is not tuple)

  def test_refs_to(self):
    obj1 = {'a': 1}
    obj2 = [obj1]
    test_list = ObjList()
    refs_to = test_list.refs_to(obj1)
    self.assertTrue(obj2 in refs_to)

  def test_refs_by(self):
    obj1 = {'a': 1}
    obj2 = [obj1]
    test_list = ObjList()
    refs_by = test_list.refs_by(obj2)
    self.assertTrue(obj1 in refs_by)
