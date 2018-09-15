import gc


class Capture:
  def __init__(self, start=False):
    if start is True:
      self.start()

  def start(self):
    self.begin = gc.get_objects()

  def end(self):
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
  def __init__(self, empty=False):
    if not empty:
      for item in gc.get_objects():
        t = type(item)
        if t is not ObjList and t is not Capture:
          self.append(item)

  def __sub__(self, other):
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
    if len(self) >= pos:
      return self.refs_to(self[pos])
    return ObjList(empty=True)

  def refs_to(self, obj):
    new_list = ObjList(empty=True)
    refs = gc.get_referrers(obj)
    for item in refs:
      t = type(item)
      if t is not ObjList and t is not Capture:
        new_list.append(item)
    return new_list

  def refs_by_at(self, pos):
    if len(self) >= pos:
      return self.refs_by(self[pos])
    return ObjList(empty=True)

  def refs_by(self, obj):
    new_list = ObjList(empty=True)
    refs = gc.get_referents(obj)
    for item in refs:
      t = type(item)
      if t is not ObjList and t is not Capture:
        new_list.append(item)
    return new_list

  def pprint(self, obj_len=None):
    if obj_len is not None and type(obj_len) is int and obj_len > 0:
      f_str = '{:.' + str(obj_len) + '}'
      for i in range(0, len(self)):
        print(i, f_str.format(str(self[i])))
    else:
      for i in range(0, len(self)):
        print(i, self[i])

  def pprintt(self, obj_len=None):
    if obj_len is not None and type(obj_len) is int and obj_len > 0:
      f_str = '{:.' + str(obj_len) + '}'
      for i in range(0, len(self)):
        print(i, type(self[i]), f_str.format(str(self[i])))
    else:
      for i in range(0, len(self)):
        print(i, type(self[i]), self[i])

  def psummary(self):
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
