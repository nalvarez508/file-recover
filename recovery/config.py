import os

WELCOME_MSG = "Welcome to the unofficial DiskDigger recovery wizard. You'll be guided through the setup process and will be able to select which files to save at the end. Please ensure you've completed a DiskDigger scan and saved the report (via the Advanced tab) to somewhere accessible."
FILE_SELECT_MSG = "Select the DiskDigger report file."
DRIVE_SELECT_MSG = "Select the drive where the files will be recovered from."
WARNING_MSG = "WARNING: Using the affected drive, such as writing a file, may render your data unrecoverable."

PADX = 16
LABEL_SIZE = 16

if os.name == 'nt':
  BACKGROUND = 'SystemButtonFace'
  SYSTEM_FONT = "Tahoma"
elif os.name == 'posix':
  BACKGROUND = 'gray93'
  SYSTEM_FONT = "Tahoma"