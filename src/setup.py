# -*- coding: utf-8 -*-
import os
import sys

PLATFORM      = sys.platform
PYTHON        = sys.executable
APP           = os.path.join(os.path.abspath(__file__).split('setup.py')[0], 'main.py')
CALL          = PYTHON + ' ' + APP

def main():
    # Detect OS and add alias via .bashrc or .bash_profile
    if 'linux' in PLATFORM:
        LINUX_COMMAND = """grep -q -F "alias eda='{}'" ~/.bashrc || echo "alias eda='{}'" >> ~/.bashrc""".format(CALL, CALL)
        os.system(LINUX_COMMAND)
        os.system("source ~/.bashrc")
        print("\n\n**Alias 'eda' set in ~/.bashrc file. Restart terminal to use alias")
    
    elif 'darwin' in PLATFORM:
        MAC_COMMAND = """grep -q -F "alias eda='{}'" ~/.bash_profile || echo "alias eda='{}'" >> ~/.bash_profile""".format(CALL, CALL)
        os.system(MAC_COMMAND)
        os.system("source ~/.bash_profile")
        print("\n\n**Alias 'eda' set in ~/.bash_profile file. Restart terminal to use alias")
    
    else:
        print("Windows OS detected -- need to manually set alias to EDA Viewer app")

if __name__ == "__main__":
	main()