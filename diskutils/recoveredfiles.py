import pandas as pd

class RecoveredFiles():
  """Stores the disk report."""
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
    self.drive = None
    self.physical_drive = None
    self.friendly_drive = None

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

  def read_file(self, path: str) -> pd.DataFrame:
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
      file_info = pd.read_csv(path, sep=',', header=8, parse_dates=[3,4,5])
      return file_info
    except pd.errors.ParserError:
      return None

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
      device_info = pd.read_csv(path, sep=',', header=None, names=["Attribute", "Value"], skiprows=4, nrows=3)
      model, _bytes, sectors = list(device_info["Value"])
      return [model, int(_bytes), int(sectors)]
    except (pd.errors.ParserError, ValueError):
      return [None, None, None]