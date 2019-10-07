# -*- coding: utf-8 -*-
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile

from apps.importer.exceptions import ReaderException
from apps.catalog.models import ImportTask
from utils.timer_profile import TimerProfile

from time import sleep

import datetime
import requests
import socket
import os

import logging

socket.setdefaulttimeout(60)


class BaseReader(object):
    """BaseReader"""
    def __init__(self, importtask_id, logger=None):
        """
            Args:
                importtask_id - pk value from model ImportTask.id
        """
        super(BaseReader, self).__init__()
        self.importtask_id = importtask_id
        self.old_file = None
        self.source_file = None
        self.timer = None
        self.logger = logger if logger else logging.getLogger('importer')
        self._start_process()

    def _start_process(self):
        try:
            self.import_catalog = ImportTask.objects.get(id=self.importtask_id)
        except ImportTask.DoesNotExist:
            raise ReaderException(code='R001', message="Import task ID - %s" % self.importtask_id)

        self.logger.info(
            u"[%s]Starting importer id" % self.importtask_id)
        self.timer = TimerProfile(
            name='[ImportTask_%s]' % self.importtask_id,
        )

        self.catalog = self.import_catalog.catalog
        self.site = self.import_catalog.site
        self.import_url = self.import_catalog.url
        self.old_file = \
            self.import_catalog.data.path if self.import_catalog.data else None
        if not self.import_url:
            raise ReaderException(code='R002')
        self.import_catalog.status = self.import_catalog.STATUS.PROCESSING
        self.import_catalog.start = datetime.datetime.now()
        self.import_catalog.save()

    def _err_finish_process(self, err_msg=None):
        self.import_catalog.error = err_msg if err_msg else "Unknown error"
        self.import_catalog.status = self.import_catalog.STATUS.ERROR
        self.import_catalog.save()
        self.logger.error(
            u"[%s]Can't import task. Error: %s" % (
                self.importtask_id, err_msg))

    def _success_finish_process(self):
        if self.old_file:
            self.remove_old_file(self.old_file)
        self.import_catalog.complete = datetime.datetime.now()
        self.import_catalog.validity = True
        self.import_catalog.status = self.import_catalog.STATUS.DONE
        self.import_catalog.error = ''
        self.import_catalog.save()
        self.logger.info(self.timer.checkpoint('Finish import'))

    @staticmethod
    def get_content(import_url, retries=3, retry_pause=10):
        """
        Function to get file from server.
        Args:
            import_url: url
            retries: int number of retries.
            retry_pause: int number of seconds to pause between retries
        Returns:
            content
        Raises:
             ReaderException: code R0003
        """
        retry = 0
        while retry < retries:
            try:
                r = requests.get(import_url)
                if r.status_code == 404:
                    raise ReaderException(code='R003')
                return r.content
            except (
                requests.exceptions.Timeout,
                requests.exceptions.HTTPError,
                requests.exceptions.ConnectionError
            ):
                retry += 1
                if retry < retries:
                    sleep(retry_pause)
        raise ReaderException(code='R003')

    @staticmethod
    def remove_old_file(filename):
        if os.path.exists(filename):
            try:
                os.remove(filename)
            except OSError:
                pass
        else:
            pass

    def _file_process(self):
        tmp_file = NamedTemporaryFile(delete=True)
        try:
            tmp_file.write(
                self.get_content(self.import_url)
            )
        except ReaderException:
            # TODO disable product from search
            self._err_finish_process("R003")
            raise ReaderException(code='R003')
        tmp_file.flush()
        self.import_catalog.data.save(
            "temp." + self.import_catalog.FORMATS.get_name(
                self.import_catalog.format)[:3].lower(), File(tmp_file))
        self.source_file = self.import_catalog.data.path

    def __call__(self):
        """
            processing
        """
        self._file_process()
        self.logger.debug(self.timer.checkpoint('function file_process()'))
