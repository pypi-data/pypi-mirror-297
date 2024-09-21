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

class MaterialDBException(Exception):
    def __init__(self, message):
        self.message = message

class MaterialProperty():
    def __init__(self, name, values):
        logging.basicConfig(format="{asctime} [{levelname}:{name}]: {message}",
                            style="{",
                            datefmt="%Y-%m-%d %H:%M",
                            level=logging.INFO)
        self._logger = logging.getLogger('MaterialProperty')
        self._logger.debug(f'__init__: {name}')

        self.__Name = name
        
        if name not in globals():
            raise MaterialDBException(f"MaterialProperty '{name}' unknown")
            
        self.__Value = globals()[name](float(values['Value']), values['Unit'])
        
        if 'T' in values.keys() and 'Tunit' in values.keys():
            self.__Tref = Temperature(float(values['T']), values['Tunit'])
        else:
            self.__Tref = Temperature(20.0, '°C')

        self.__Axis = None
        if 'Axis' in values.keys():
            a = values['Axis'].upper()
            if a!='X' and a!='Y' and a!='Z':
                raise MaterialDBException(f"Material axis '{a}' unknown")
            self.__Axis = a
            
    def name(self):
        return self.__Name
            
    def axis(self):
        return self.__Axis
    
    def value(self):
        return self.__Value
    
    def referencetemperature(self):
        return self.__Tref
    
    def __str__(self):
        t = ""
        if self.__Axis is not None:
            n = self.__Name + ' ' + self.__Axis
            t += f"{n:30s}"
        else:
            t += f"{self.__Name:30s}"
        t += f"{self.__Value.value(self.__Value.getPreferredUnit()):9.3f} "
        t += f"{self.__Value.getPreferredUnit()}"
        t += f" (@{self.__Tref.asString()})"
        return t

class Material():
    
    def __init__(self, name, title, category):
        logging.basicConfig(format="{asctime} [{levelname}:{name}]: {message}",
                            style="{",
                            datefmt="%Y-%m-%d %H:%M",
                            level=logging.INFO)
        self._logger = logging.getLogger('Material')
        self._logger.debug(f'__init__: {name}, {title}')
        
        self.__Name = name
        self.__Title = title
        self.__Category = category
        self.__Groups = []
        self.__Properties = {}
        
        self.__MaterialDB = None
        #self.__MaterialDB = MaterialDB()

    def name(self):
        return self.__Name

    def title(self):
        return self.__Title

    def category(self):
        return self.__Category
    
    def addToGroup(self, group):
        self.__Groups.append(group)
        #print(group)
    
    def addProperty(self, prop):
        self._logger.debug(f'addProperty: {prop.name()}')
        self.__Properties[(prop.name(), prop.axis())] = prop
        #print(group)
    
    def getProperty(self, prop: str, axis: str = None) -> MaterialProperty:
        if (prop, axis) in self.__Properties:
            return self.__Properties[(prop, axis)]
        raise MaterialDBException(f"Property {prop} {axis} not known to material {self.__Name}")
    
    def __str__(self):
        t =  f"{self.__class__.__name__}\n"
        t += f"Name:     {self.__Name}\n"
        t += f"Title:    {self.__Title}\n"
        t += f"Category: {self.__Category}\n"
        t += "Groups:   "
        for i,g in enumerate(self.__Groups):
            if i > 0:
                t += ', '
            t += g
        t += "\n"
        t += "Properties:\n"
        for n,p in self.__Properties.items():
            t += '  ' + str(p) + '\n'
        return t

class IsotropicMaterial(Material):
    def __init__(self, name, title, category):
        super().__init__(name, title, category)
        self._logger.name = 'IsotropicMaterial'
        self._logger.debug(f'__init__: {name}, {title} 2')

class OrthotropicMaterial(Material):
    def __init__(self, name, title, category):
        super().__init__(name, title, category)
        self._logger.name = 'OrthotropicMaterial'
        self._logger.debug(f'__init__: {name}, {title} 2')

class MaterialDB(metaclass=Singleton):
    def __init__(self):
        logging.basicConfig(format="{asctime} [{levelname}:{name}]: {message}",
                            style="{",
                            datefmt="%Y-%m-%d %H:%M",
                            level=logging.INFO)
        self.__logger = logging.getLogger('MaterialDB')

        self.__logger.debug('__init__')
        
        self.__materials = []
        self.__materialsByName = {}
        self.__materialsByTitle = {}
        self.__groups = {}
        self.__categories = {}
        
        self.__readDB()
    
    def getMaterials(self) -> list[Material]:
        return self.__materials
        
    def getMaterial(self, name: str) -> Material:
        return self.getMaterialByName(name)
    
    def getMaterialByName(self, name: str) -> Material:
        if name not in self.__materialsByName:
            raise MaterialDBException(f"Material '{name}' (name) not found")
        return self.__materialsByName[name]
    
    def getMaterialByTitle(self, title: str) -> Material:
        if title not in self.__materialsByTitle:
            raise MaterialDBException(f"Material '{title}' (title) not found")
        return self.__materialsByTitle[title]

    def getGroups(self) -> list[str]:
        return list(self.__groups.keys())

    def getMaterialsForGroup(self, group: str) -> list[Material]:
        if group not in self.__groups:
            return []
        return self.__groups[group]

    def getCategories(self) -> list[str]:
        return list(self.__categories.keys())

    def getMaterialsForCategory(self, category: str) -> list[Material]:
        if category not in self.__categories:
            return []
        return self.__categories[category]
    
    def __processFile(self, xmlfile):
        try:
            self.__logger.debug(f'processing {xmlfile}')
            tree = ET.parse(xmlfile)
            root = tree.getroot()
            for child in root:
                self.__logger.debug(f'processing {child.tag}')
                
                name = child.find('Name').text
                title = child.find('Title').text
                category = child.find('Category').text
                
                if child.tag == 'IsotropicMaterial':
                    material = IsotropicMaterial(name, title, category)
                elif child.tag == 'OrthotropicMaterial':
                    material = OrthotropicMaterial(name, title, category)
                else:
                    print(child.tag)
                    continue
                
                groups = child.find('Groups')
                if groups is not None:
                    for group in groups:
                        if group.text not in self.__groups:
                            self.__groups[group.text] = []
                        self.__groups[group.text].append(material)
                        material.addToGroup(group.text)
                
                props = child.find('Properties')
                if props is not None:
                    for prop in props:
                        prop = MaterialProperty(prop.tag, prop.attrib)
                        material.addProperty(prop)
                
                if category not in self.__categories:
                    self.__categories[category] = []
                self.__categories[category].append(material)
                
                self.addMaterial(material)
        except:
            raise MaterialDBException(f"could not process file {xmlfile}")
        
    def __readDB(self):
        filenames = ['MaterialDB_elements.xml',
                     'MaterialDB_alloys.xml',
                     'MaterialDB_polymers.xml',
                     'MaterialDB_ceramics.xml',
                     'MaterialDB_compounds.xml',
                     'MaterialDB_composites.xml']
        for filename in filenames:
            self.__logger.debug(f'reading {filename}')
            xmlfile = pkg_resources.files('physeng.data').joinpath(filename)
            self.__processFile(xmlfile)
    
    def addMaterial(self, material):
        self.__materials.append(material)
        self.__materialsByName[material.name()] = material
        self.__materialsByTitle[material.title()] = material
        self.__logger.debug(f'addMaterial: {material.name()}, {material.title()}')


if __name__ == '__main__':
    matDB = MaterialDB()
    
    groups = matDB.getGroups()
    print(groups)
    
    categories = matDB.getCategories()
    print(categories)
    
    mat = matDB.getMaterial('Entegris PocoFoam')
    print(mat)
    prop = mat.getProperty('ThermalConductivity', 'X')
    print(prop.value())

    mat = matDB.getMaterial('Keratherm KP12')
    print(mat)
    
 