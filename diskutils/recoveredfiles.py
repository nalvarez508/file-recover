import pandas as pd

class RecoveredFiles():
  def __init__(self, path: str):
    self.files = self.read_file(path)
    try:
      if self.files == None:
        raise TypeError("File could not be read.")
    except ValueError: pass
    self.model, self.bytes, self.sectors = self.read_device_info(path)
    try: self.size = self.bytes/(1024*3)
    except (TypeError, ZeroDivisionError): self.size = 0.0
    self.sector_size = int(self.bytes/self.sectors) # Naive?

  def read_file(self, path: str) -> pd.DataFrame:
    try:
      file_info = pd.read_csv(path, sep=',', header=8, parse_dates=[3,4,5])
      return file_info
    except pd.errors.ParserError:
      return None

  def read_device_info(self, path: str) -> list:
    try:
      device_info = pd.read_csv(path, sep=',', header=None, names=["Attribute", "Value"], skiprows=4, nrows=3)
      model, _bytes, sectors = list(device_info["Value"])
      return [model, int(_bytes), int(sectors)]
    except (pd.errors.ParserError, ValueError):
      return [None, None, None]