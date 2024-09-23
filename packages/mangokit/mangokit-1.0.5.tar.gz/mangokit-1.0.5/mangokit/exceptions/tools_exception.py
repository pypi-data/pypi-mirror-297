# -*- coding: utf-8 -*-
# @Project: MangoActuator
# @Description: 
# @Time   : 2023-07-16 15:17
# @Author : 毛鹏
from mangokit.exceptions import TestKitError


class JsonPathError(TestKitError):
    pass


class ValueTypeError(TestKitError):
    pass


class SendMessageError(TestKitError):
    pass


class FileDoesNotEexistError(TestKitError):
    pass


class CacheIsEmptyError(TestKitError):
    pass


class MethodDoesNotExistError(TestKitError):
    pass
