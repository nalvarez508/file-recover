import os

WELCOME_MSG = "Welcome to the unofficial DiskDigger recovery wizard. You'll be guided through the setup process and will be able to select which files to save at the end. Please ensure you've completed a DiskDigger scan and saved the report (via the Advanced tab) to somewhere accessible.\n\nClick Next to begin."

if os.name == 'nt':
  BACKGROUND = 'SystemButtonFace'
  SYSTEM_FONT = "Tahoma"
elif os.name == 'posix':
  BACKGROUND = 'gray93'
  SYSTEM_FONT = "Tahoma"