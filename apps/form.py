#!/usr/bin/python3
# _*_ coding: utf-8 _*_


class FormMixin:
    def get_errors(self):
        if hasattr(self, 'errors'):
            raw_errors = self.errors.get_json_data()
            errors = {}
            for element, warnings in raw_errors.items():
                messages = []
                for info in warnings:
                    messages.append(info.get('message'))
                errors[element] = messages
            return errors
        else:
            return {}
