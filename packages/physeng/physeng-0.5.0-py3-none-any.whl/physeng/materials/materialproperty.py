#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: mussgill
"""

import importlib.resources as pkg_resources
import xml.etree.ElementTree as ET

import logging

from physeng.singleton import Singleton
from physeng.units import *

from physeng.materials.utilities import MaterialDBException

class MaterialProperty():
    def __init__(self, name, Value, Tref, Axis = None):
        logging.basicConfig(format="{asctime} [{levelname}:{name}]: {message}",
                            style="{",
                            datefmt="%Y-%m-%d %H:%M",
                            level=logging.INFO)
        self._logger = logging.getLogger('MaterialProperty')
        self._logger.debug(f'__init__: {name}')

        self._Name = name
        self._Value = Value
        self._Tref = Tref
        self._Axis = Axis
        
    @classmethod
    def fromXML(cls, name, values):
        
        if name not in globals():
            raise MaterialDBException(f"MaterialProperty '{name}' unknown")
            
        Value = globals()[name](float(values['Value']), values['Unit'])
        
        if 'T' in values.keys() and 'Tunit' in values.keys():
            Tref = Temperature(float(values['T']), values['Tunit'])
        else:
            Tref = Temperature(20.0, '°C')
            
        Axis = None
        if 'Axis' in values.keys():
            a = values['Axis'].upper()
            if a!='X' and a!='Y' and a!='Z':
                raise MaterialDBException(f"Material axis '{a}' unknown")
            Axis = a
            
        return cls(name, Value, Tref, Axis)
            
    def name(self):
        return self._Name
            
    def axis(self):
        return self._Axis
    
    def value(self):
        return self._Value
    
    def referencetemperature(self):
        return self._Tref
    
    def __str__(self):
        t = ""
        if self._Axis is not None:
            n = self._Name + ' ' + self._Axis
            t += f"{n:30s}"
        else:
            t += f"{self._Name:30s}"
        t += f"{self._Value.value(self._Value.getPreferredUnit()):9.3f} "
        t += f"{self._Value.getPreferredUnit()}"
        t += f" (@{self._Tref.asString()})"
        return t

class DerivedMaterialProperty(MaterialProperty):
    def __init__(self, name, Value, Tref, Axis = None):
        super().__init__(name, Value, Tref, Axis)
        self._logger.name = 'DerivedMaterialProperty'
        self._logger.debug(f'__init__: {name}')
        
    def __str__(self):
        t = ""
        if self._Axis is not None:
            n = self._Name + ' ' + self._Axis + ' *'
            t += f"{n:30s}"
        else:
            n = self._Name + ' *'
            t += f"{n:30s}"
        t += f"{self._Value.value(self._Value.getPreferredUnit()):9.3f} "
        t += f"{self._Value.getPreferredUnit()}"
        t += f" (@{self._Tref.asString()})"
        return t
