import os
import json
from typing import List, Dict, Set

class MapObject:
    def __init__(self, name: str, categories: str, iconFile: str, contour: str):
        self.name = name
        self.categories = categories
        self.iconFile   = iconFile
        self.contour    = contour

    @classmethod
    def from_json(cls, json_data: Dict, base_path: str):
        return cls(
            name=json_data.get('name', ''),
            categories=json_data.get('categories', ''),
            iconFile=os.path.join(base_path, json_data.get('iconFile', '')),
            contour=json_data.get('contour', ''),
        )
        
    def isContour(self):
        return len(self.contour) > 0

class ObjectsCollection:
    def __init__(self, searchpaths: List[str]):
        self.searchpaths = searchpaths
        self.objects: Dict[str, MapObject] = {}
        self._load_objects()

    def _load_objects(self):
        for searchpath in self.searchpaths:
            for root, dirs, files in os.walk(searchpath):
                if 'object.json' in files:
                    with open(os.path.join(root, 'object.json'), 'r') as file:
                        data = json.load(file)
                        map_object = MapObject.from_json(data, root)
                        self.objects[map_object.name] = map_object

    def allObjectCategories(self) -> List[str]:
        categories: Set[str] = set()
        for map_object in self.objects.values():
            for category in map_object.categories.split(','):
                categories.add(category.strip())
        return list(categories)

    def allObjectTypes(self) -> List[str]:
        return list(self.objects.keys())

    def getTypesInCategory(self, category: str) -> List[str]:
        types_in_category: List[str] = []
        for map_object in self.objects.values():
            if category in map_object.categories.split(','):
                types_in_category.append(map_object.name)
        return types_in_category

    def getIcon(self, objname: str) -> str:
        map_object = self.objects.get(objname)
        if map_object:
            return map_object.iconFile
        else:
            return None

    def isContour(self, objname: str) -> bool:
        map_object = self.objects.get(objname)
        if map_object is None:
            return False
        return map_object.isContour()
        
    def getObject(self, objname: str) -> MapObject:
        return self.objects.get(objname)
