import textwrap
from datetime import datetime, timezone
from typing import List, Optional

from ..models import Property, ClassType


class Generator:
    _indent_char = "    "

    _class_name: str
    _properties: List[Property] = []

    def __init__(self, class_name: str, properties: List[Property]):
        self._class_name = class_name
        self._properties = properties

    def build(self) -> str:
        pass

    def _generate_property_list(self, joiner: str = "\n") -> str:
        lines = []
        for prop in self._properties:
            lines.append(f"""
    {prop.api_name}: {prop.wrapped()} = None
                    """.strip())

        return joiner.join(lines)

    def _i_property_handler(self, pname: str, ptype: str, depth: int = 0) -> str:
        line = ""
        if ptype in ["bool", "str", "int", "float"]:
            line = f"""
{pname}
                        """.strip()
        elif ptype.startswith("list"):
            inner = ptype[len("list["):-1]
            line = f"""
[{self._i_property_handler(f"e{depth}", inner, depth+1)} for e{depth} in {pname}]
                    """.strip()
        else:
            line = f"""
{ptype}.parse({pname})
                        """.strip()

        return line

    def _property_handler(self, prop: Property, source_name: str, assignment: str) -> str:
        line = self._i_property_handler(f"{source_name}[\"{prop.api_name}\"]", prop.type)

        if not prop.nullable:
            return f"{assignment}{line}"

        return f"""
{assignment}{line} if "{prop.api_name}" in {source_name} else None
                        """.strip()


class ModelGenerator(Generator):
    _class_type: ClassType

    def __init__(self, class_name: str, properties: List[Property], class_type: ClassType):
        super().__init__(class_name, properties)
        self._class_type = class_type

    def build(self) -> str:
        if self._class_type == ClassType.RESPONSE:
            return ResponseModelGenerator(self._class_name, self._properties).build()

        return GeneralModelGenerator(self._class_name, self._properties).build()


class GeneralModelGenerator(Generator):
    check_all = False

    def __init__(self, class_name: str, properties: List[Property], is_response: bool = False):
        super().__init__(class_name, properties)

    def build(self) -> str:
        return f"""
@dataclass
class {self._class_name}:
    \"\"\"https://join-lemmy.org/api/interfaces/{self._class_name}.html\"\"\"

{textwrap.indent(self._generate_property_list(), self._indent_char)}
    
    @classmethod
    def parse(cls, data: dict[str, Any]):
{textwrap.indent(self._generate_cls_parse(), self._indent_char * 2)}
            """.strip()

    def _generate_cls_parse(self) -> str:
        lines = []
        for prop in self._properties:
            lines.append(f"{self._property_handler(prop, 'data', f'{prop.api_name}=')}")

        lines = ",\n".join(lines)

        return f"""
return cls(
{textwrap.indent(lines, self._indent_char)}
)
        """.strip()

class ResponseModelGenerator(Generator):
    check_all = False

    def __init__(self, class_name: str, properties: List[Property], is_response: bool = False):
        super().__init__(class_name, properties)

    def build(self) -> str:
        joiner = ",\n"
        return f"""
class {self._class_name}(ResponseWrapper):
    \"\"\"https://join-lemmy.org/api/interfaces/{self._class_name}.html\"\"\"

{textwrap.indent(self._generate_property_list(), self._indent_char)}
    
    def parse(self, data: dict[str, Any]):
{textwrap.indent(self._generate_parse(), self._indent_char * 2)}

    @classmethod
    def data(
        cls, 
{textwrap.indent(self._generate_property_list(joiner=joiner), self._indent_char * 2)}
    ):
        obj = cls.__new__(cls)
{textwrap.indent(self._generate_constructor(), self._indent_char * 2)}
        return obj
            """.strip()

    def _generate_parse(self) -> str:
        lines = []
        for prop in self._properties:
            lines.append(f"{self._property_handler(prop, 'data', f'self.{prop.api_name} = ')}")

        return "\n".join(lines)

    def _generate_constructor(self) -> str:
        lines = []
        for prop in self._properties:
            lines.append(f"obj.{prop.api_name} = {prop.api_name}")

        return "\n".join(lines)

