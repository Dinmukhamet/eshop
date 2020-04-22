from django.core.files.storage import FileSystemStorage
from django.conf import settings
import os
import re

class OverwriteStorage(FileSystemStorage):
    
    def get_available_name(self, name, max_length):
        i = 0
        if self.exists(name):
            i += 1
        filebase, extension = name.rsplit('.',1)
            #tmp = int(re.search(r'\d+', filebase).group())
        new_filebase = ''.join([e for e in filebase if not e.isdigit()])
        new_name = '{}{}.{}'.format(new_filebase, i, extension)

