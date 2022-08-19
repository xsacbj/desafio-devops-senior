from sqlalchemy.inspection import inspect
import datetime
class Serializer(object):

  def serialize(self):
    serial = {}
    for c in inspect(self).attrs.keys():
      serial[c] = getattr(self, c)
      if isinstance(serial[c], datetime.datetime):
        serial[c] = serial[c].isoformat()
    return serial

  @staticmethod
  def serialize_list(l):
    return [m.serialize() for m in l]