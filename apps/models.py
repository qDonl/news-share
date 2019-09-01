#!/usr/bin/python3
# _*_ coding: utf-8 _*_

from django.db import models


class ModelMixin(models.Model):

    def set_attr(self, attr_dict):
        for key, value in attr_dict.items():
            if hasattr(self, key) and key != 'id':
                setattr(self, key, value)

    class Meta:
        abstract = True
