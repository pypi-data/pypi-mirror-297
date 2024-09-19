import os
from typing import Any, TypeVar, Generic, List, Optional

T = TypeVar('T')

class ConstantClass:
    def __setattr__(self, name, value) -> None:
        if name in self.__dict__:
            raise AttributeError(f"Cannot reassign constant {name}")
        self.__dict__[name] = value

class Constant():

    def __init__(self, value: Any, expectType: Optional[type] = None) -> None:
        # Check if the value is of the correct type. But only is the correct type is given
        expectType = type(value) if expectType is None else expectType
        
        if type is not None and not isinstance(value, expectType):
            try:
                from colorama import Fore
                print(Fore.RED)
                raise TypeError(f"Expected type {expectType} but got {type(value)}")
            except:
                raise TypeError(f"Expected type {expectType} but got {type(value)}")
        self.__value = value
    
    @property
    def v(self):
        """Returns the value of the constant"""
        return self.__value
    
    @v.setter
    def v(self, value: Any) -> None:
        ConstantM.__constantError__()

    def __setattr__(self, name, value) -> None:
        if name in self.__dir__():
            ConstantM.__constantError__()
        self.__dict__[name] = value
    
    def __repr__(self) -> str:
        return str(self.__value)

class ConstantM:
    @staticmethod
    def __constantError__() -> None:
        raise AttributeError("Cannot reassign constant")
    
    @staticmethod
    def ConstantProperty(setFunc) -> property:
        Property = property(fget=setFunc, fset=ConstantM.__constantError__)
        return Property