import os
import time
from hashlib import md5

# from django.conf import settings


def get_upload_path(section):
    def get_section_path(instance, filename):
        ext = filename.rsplit('.', 1)[-1]
        # if ext not in ('jpg', 'png', 'gif', 'jpeg', 'xls'):
        #     ext = 'jpg'
        hash = md5(str(time.time())).hexdigest()
        return os.path.join('', section, '%s.%s' % (hash, ext))
    return get_section_path
