import pandas as pd

class RecoveredFiles():
  """Stores the disk report."""
  def __init__(self, path: str, is_deeper: bool=False):
    self.files = self.read_file(path, is_deeper)
    try:
      if self.files == None:
        raise TypeError("File could not be read.")
      elif type(self.files) == str:
        raise RuntimeError(f"An issue was encountered when reading the file. Please make sure all columns line up, such as a file with commas in its name.\n\n{self.files}")
    except ValueError: pass
    self.model, self.bytes, self.sectors = self.read_device_info(path)
    try: self.size = self.bytes/(1024*3)
    except (TypeError, ZeroDivisionError): self.size = 0.0
    self.sector_size = int(self.bytes/self.sectors) # Naive?
    self.drive = None
    self.physical_drive = None
    self.friendly_drive = None
    self.deeper = is_deeper

  def set_drive(self, drive_df: pd.DataFrame) -> None:
    """
    Sets working drive information.

    Parameters
    ----------
    drive_df : pd.DataFrame
        Drive info from wizard.driveselect
    """
    self.drive = drive_df
    self.physical_drive = drive_df["DeviceID"]
    self.friendly_drive = drive_df["Caption"]

  def read_file(self, path: str, deeper: bool) -> pd.DataFrame:
    """
    Loads report information.

    Parameters
    ----------
    path : str
        Path to CSV report.

    Returns
    -------
    pd.DataFrame
        Report information.
    """
    try:
      if deeper == False:
        file_info = pd.read_csv(path, sep=',', header=8, parse_dates=[3,4,5])
        return file_info
      elif deeper == True:
        file_info = pd.read_csv(path, sep=',', header=8)
        return file_info
    except pd.errors.ParserError as e:
      print(e)
      return str(e)

  def read_device_info(self, path: str) -> list:
    """
    Reads device information as returned from search list.

    Parameters
    ----------
    path : str
        Path to the CSV.

    Returns
    -------
    list
        Device model, number of bytes, number of sectors
    """
    try:
      device_info = pd.read_csv(path, sep=',', header=None, names=["Attribute", "Value"], skiprows=4, nrows=3, usecols=[0,1])
      model, _bytes, sectors = list(device_info["Value"])
      return [model, int(_bytes), int(sectors)]
    except (pd.errors.ParserError, ValueError):
      return [None, None, None]