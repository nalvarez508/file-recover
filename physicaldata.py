class PhysicalData():
  def __init__(self, physical_name: str, sector_size: int) -> None:
    self.physical_name = physical_name
    self.sector_size = sector_size
    try:
      self.disk = open(self.physical_name, 'rb')
    except PermissionError as e:
      raise PermissionError(e)

  def __del__(self):
    self.disk.close()

  def search(self, start: int, length: int) -> bytes:
    self.disk.seek(start*self.sector_size)
    _data = self.disk.read(length)
    return _data
  
  def save(self, path: str, data: bytes) -> bool:
    try:
      with open(path, 'wb') as f:
        f.write(data)
      return True
    except (FileNotFoundError, OSError) as e:
      print(e)
      return False