#!/usr/bin/env python
import os
import sys

import dotenv
dotenv.read_dotenv()
sys.path.append('sarvahar.settings.settings_harshit')

#import pdb;pdb.set_trace()
if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sarvahar.sarvahar.settings")
    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
