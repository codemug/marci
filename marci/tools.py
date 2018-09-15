import gc


class Capture:
  """
  A ``Capture`` object is used to capture all the objects created during the
  execution of the code that is between it's ``start`` and ``end`` methods as
  an ``ObjList``. The ``Capture`` object is recyclable in the sense that each
  new ``start`` creates a new checkpoint, discarding the last one. The
  constructor also takes a boolean ``start`` argument which, if set to true,
  also creates the first checkpoint.

  Example::

    from marci import Capture
    capture = Capture()
    capture.start()
    myObject.MyMethod()
    obj_list = capture.end()

  """

  def __init__(self, start=False):
    """
    Initialize a new ``Capture`` instance
    :param start: Also create the first checkpoint
    """
    if start is True:
      self.start()

  def start(self):
    """
     Creates a new checkpoint of the memory
    """
    self.begin = gc.get_objects()

  def end(self):
    """
    Ends the capture, finds out the new objects created between the ``start``
    call and the moment ``end`` is called.
    :return: An ``ObjList`` of newly created objects
    """
    end = gc.get_objects()
    obj_list = ObjList(empty=True)
    for item in end:
      if item is self or item is self.begin or item is end:
        continue
      found = False
      for other in self.begin:
        if item is other:
          found = True
          break
      if not found:
        obj_list.append(item)
    del (self.begin)
    del (end)
    return obj_list


class ObjList(list):
  """
  A ``list()`` with additional methods for memory analysis and object graph
  traversal
  """

  def __init__(self, empty=False):
    """
    Initialize a new ``ObjList``
    :param empty: Create an empty ``ObjList``, otherwise fill it with current
      memory objects
    """
    if not empty:
      for item in gc.get_objects():
        t = type(item)
        if t is not ObjList and t is not Capture:
          self.append(item)

  def __sub__(self, other):
    """
    Subtract another ``ObjList`` from this one. This method doesn't mutate the
    original ``ObjList``s
    :param other: The other ``ObjList``
    :return: An `ObjList` containing the subtraction result
    """
    if type(other) is not ObjList:
      raise TypeError(
          "Cannot subtract " + str(type(other)) + ' from an ObjList')
    result = ObjList(empty=True)
    for item_b in self:
      found = False
      for item_a in other:
        if item_b is item_a:
          found = True
          break
      if not found:
        result.append(item_b)
    return result

  def extract(self, ex_type):
    """
    Extract specific type(s) of objects from this ``ObjList``. This does not
    mutate the existing ``ObjList``
    :param ex_type: A ``type()`` or a ``list()`` of ``type()`` that should be
      included
    :return: ``ObjList`` that only contains the objects of the specified type(s)
    """
    new_list = ObjList(empty=True)
    if type(ex_type) is list:
      for item in self:
        if type(item) in ex_type:
          new_list.append(item)
    else:
      for item in self:
        if type(item) is ex_type:
          new_list.append(item)
    return new_list

  def sanitize(self, ex_type):
    """
    Exclude specific type(s) of object from this ``ObjList``. This does not
    mutate the existing ``ObjList``
    :param ex_type: ex_type: A ``type()`` or a ``list()`` of ``type()``
      that should be included
    :return: ``ObjList`` that does not contain the objects of the
      specified type(s)
    """
    new_list = ObjList(empty=True)
    if type(ex_type) is list:
      for item in self:
        if type(item) not in ex_type:
          new_list.append(item)
    else:
      for item in self:
        if type(item) is not ex_type:
          new_list.append(item)
    return new_list

  def refs_to_at(self, pos):
    """
    Get the objects that hold a reference to the object as a specified position
    in this ``ObjList``
    :param pos: Index position of the object that is being referenced
    :return: ``ObjList`` containing the referrer objects
    """
    if len(self) >= pos:
      return self.refs_to(self[pos])
    return ObjList(empty=True)

  def refs_to(self, obj):
    """
    Get the objects that hold a reference to the specified object
    :param obj: The object that is being referenced
    :return: ``ObjList`` containing the referrer objects
    """
    new_list = ObjList(empty=True)
    refs = gc.get_referrers(obj)
    for item in refs:
      t = type(item)
      if t is not ObjList and t is not Capture:
        new_list.append(item)
    return new_list

  def refs_by_at(self, pos):
    """
    Get the objects that are referred by the object at a specified position in
    this ``ObjList``
    :param pos: Index position of the object that is referencing
    :return: ``ObjList`` containing the referee objects
    """
    if len(self) >= pos:
      return self.refs_by(self[pos])
    return ObjList(empty=True)

  def refs_by(self, obj):
    """
    Get the objects that are referred by the  specified object
    :param obj: The object that is referring
    :return: ``ObjList`` containing the referee objects
    """
    new_list = ObjList(empty=True)
    refs = gc.get_referents(obj)
    for item in refs:
      t = type(item)
      if t is not ObjList and t is not Capture:
        new_list.append(item)
    return new_list

  def pprint(self, obj_len=None):
    """
    Pretty print the list with index values
    :param obj_len: Maximum length of the string that represents the objects
    """
    if obj_len is not None and type(obj_len) is int and obj_len > 0:
      f_str = '{:.' + str(obj_len) + '}'
      for i in range(0, len(self)):
        print(i, f_str.format(str(self[i])))
    else:
      for i in range(0, len(self)):
        print(i, self[i])

  def pprintt(self, obj_len=None):
    """
    Pretty print the list with index values and object types
    :param obj_len: Maximum length of the string that represents the objects
    """
    if obj_len is not None and type(obj_len) is int and obj_len > 0:
      f_str = '{:.' + str(obj_len) + '}'
      for i in range(0, len(self)):
        print(i, type(self[i]), f_str.format(str(self[i])))
    else:
      for i in range(0, len(self)):
        print(i, type(self[i]), self[i])

  def psummary(self):
    """
    Print a summary of all the objects. Prints a table containing counts for
     every object type initialized
    """
    histo = dict()
    llen = 0
    for item in self:
      t = type(item)
      if t in histo:
        histo[t] += 1
      else:
        histo[t] = 1
        t_str = str(t)
        if len(t_str) > llen:
          llen = len(t_str)
    f_str = '{:>' + str(llen) + '}'
    for k in histo:
      print(f_str.format(str(k)) + '\t' + str(histo[k]))
