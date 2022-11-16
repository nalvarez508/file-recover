class PhysicalData():
  """Drive handler."""
  def __init__(self, physical_name: str, sector_size: int) -> None:
    """
    Initializes the drive handler and opens it for reading.

    Parameters
    ----------
    physical_name : str
        System-friendly name.
    sector_size : int
        Sector size, in bytes.

    Raises
    ------
    PermissionError
        System denied read access to the drive.
    """
    self.physical_name = physical_name
    self.sector_size = sector_size
    try:
      self.disk = open(self.physical_name, 'rb')
    except PermissionError as e:
      raise PermissionError(e)

  def __del__(self):
    self.disk.close()

  def search(self, start: int, length: int) -> bytes:
    """
    Finds file data on the drive.

    Parameters
    ----------
    start : int
        Starting sector.
    length : int
        File size, in bytes.

    Returns
    -------
    bytes
        File data.
    """
    self.disk.seek(start*self.sector_size)
    _data = self.disk.read(length)
    return _data
  
  def save(self, path: str, data: bytes) -> bool:
    """
    Saves file data to a new file.

    Parameters
    ----------
    path : str
        Path to the destination file.
    data : bytes
        Recovered file data from drive.

    Returns
    -------
    bool
        Success of the operation.
    """
    try:
      with open(path, 'wb') as f:
        f.write(data)
      return True
    except (FileNotFoundError, OSError) as e:
      print(e)
      return False