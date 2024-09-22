from dataclasses import is_dataclass
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Type, get_type_hints

from sqlalchemy.orm import Mapped

from automapper.default_mapper import DefaultMapper
from automapper.functions import (
    get_fields_type,
    get_inner_type,
    is_generic_dict,
    is_generic_list,
    is_pydantic,
    is_sqlalchemy,
)
from automapper.mapping_plugin import MappingPlugin
from automapper.sql_alchemy_mapper import SqlAlchemyMapper
from automapper.types import TMapTarget, TSource, TSourceValue, TTarget


class Mapper:
    """Class that maps objects from one class to another based on the type hints

    Returns:
        _type_: _description_
    """

    """List of mapping plugins"""
    mappers: List[MappingPlugin] = [SqlAlchemyMapper(), DefaultMapper()]

    def __init__(self):
        self.custom_mappings = {}

    def add_custom_mapping(
        self, source_class: Type, source_field: str, target_field: str
    ):
        """Add a custom mapping between a source field and a target field

        Args:
            source_class (Type): source class
            source_field (str): name of the source field
            target_field (str): name of the target field
        """
        if source_class not in self.custom_mappings:
            self.custom_mappings[source_class] = {}
        self.custom_mappings[source_class][source_field] = target_field

    def get_source_fields(self, source: TSource) -> Dict[str, Type] | None:
        """Get the fields of the source object and map them to their types

        Args:
            source (TSource): source object

        Returns:
            Dict[str, Type]: a dictionary with the fields and their types
        """
        for mapper in self.mappers:
            if mapper.can_handle(source, None):
                return mapper.get_source_fields(source)

        return None

    def map(self, source: TSource, target_class: Type[TMapTarget]) -> TMapTarget:
        """Recursive function that maps the source object to the target class

        Args:
            source (TSource): source object
            target_class (Type[TMapTarget]): type of the target object

        Returns:
            TMapTarget: _description_
        """

        if source is None:
            return None

        source_fields: Optional[Dict[str, Type]] = self.get_source_fields(source)
        if source_fields is None:
            source_fields = {}
        target_fields: Dict[str, Type] = get_fields_type(target_class)

        target_kwargs = {}

        # TODO: use dictionary comprehension (PEP 274)
        for field_name, field_type in source_fields.items():

            target_field_name = self.custom_mappings.get(type(source), {}).get(
                field_name, field_name
            )

            if target_field_name not in target_fields:
                continue

            source_value = getattr(source, field_name, None)
            target_field_type = target_fields[target_field_name]
            target_kwargs[target_field_name] = self._map_field(
                source_value, target_field_type
            )

        return target_class(**target_kwargs)

    def _map_field(self, source_value: TSourceValue, target_field_type: Type):
        """Map a field from the source object to the target object

        Args:
            source_value (_type_): source value
            target_field_type (_type_): type of the target field

        Returns:
            _type_: _description_
        """

        # lambda t: isinstance(t, DeclarativeMeta): self.map,

        type_mapping: Dict[Callable[[Type], bool], Callable[[Any, Type], Any]] = {
            is_generic_list: lambda val, typ: self.map_list(val, get_inner_type(typ)),
            is_generic_dict: lambda val, typ: self.map_dict(val, get_inner_type(typ)),
            lambda t: is_dataclass(t): self.map,
            lambda t: is_pydantic(t): self.map,
            lambda t: is_sqlalchemy(t): self.map,
            lambda _: isinstance(source_value, Enum): self.map_enum,
        }

        for check, func in type_mapping.items():
            if check(target_field_type):
                return func(source_value, target_field_type)

        return source_value

    def map_enum(self, source_value: Enum, target_field_type):
        """Map an Enum value to another Enum of the target field type

        Args:
            source_value (_type_): _description_
            target_field_type (_type_): _description_

        Returns:
            _type_: _description_
        """
        target_enum_type = self._find_matching_enum(target_field_type, source_value)
        if target_enum_type:
            return getattr(target_enum_type, source_value.name)
        else:
            return source_value

    def map_list(self, source_list: List, target_inner_type: Type) -> List | None:
        """Map a list of objects to another list of objects

        Args:
            source_list (List): _description_
            target_inner_type (Type): _description_

        Returns:
            List | None: _description_
        """
        if source_list is None:
            return None
        return [self.map(item, target_inner_type) for item in source_list]

    def map_dict(self, source_dict: Dict, target_inner_type: Type) -> Dict | None:
        """Map a dictionary of objects to another dictionary of objects

        Args:
            source_dict (Dict): _description_
            target_inner_type (Type): _description_

        Returns:
            Dict | None: _description_
        """
        if source_dict is None:
            return None
        return {k: self.map(v, target_inner_type) for k, v in source_dict.items()}

    def _find_matching_enum(
        self, target_field_type: Type, source_value: Enum
    ) -> Type[Enum] | None:
        """Find a matching Enum type for the source value

        Args:
            target_field_type (Type): _description_
            source_value (Enum): _description_

        Returns:
            Type[Enum] | None: _description_
        """

        # Be careful with sqlalchemy.orm.Mapped
        if (
            hasattr(target_field_type, "__origin__")
            and target_field_type.__origin__ == Mapped
        ):
            target_field_type = target_field_type.__args__[0]
        if isinstance(target_field_type, type) and issubclass(target_field_type, Enum):
            if source_value.name in target_field_type.__members__:
                return target_field_type
        return None


# Init the singleton instance
mapper = Mapper()
