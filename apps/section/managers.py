# -*- coding: utf-8 -*-

#Django imports
from django.db import models


class CurrentManager(models.Manager):

    def get_query_set(self):
        return super(CurrentManager, self).get_query_set().filter(deleted=False)


class FullManager(models.Manager):

    def get_query_set(self):
        return super(FullManager, self).get_query_set()


class ParentSectionManage(CurrentManager):

    def get_query_set(self):
        return super(ParentSectionManage, self).get_query_set().filter(deleted=False, parent__isnull=True)


class ChildrenManage(CurrentManager):

    def get_query_set(self):
        return super(ChildrenManage, self).get_query_set().filter(deleted=False, have_child=False)
