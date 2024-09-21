from typing import List, Generator, Tuple
from pathlib import Path
from json import loads, JSONDecodeError

from referencing import Registry
from referencing.exceptions import Unresolvable
from jsonschema import Draft202012Validator

from .schema import Schema
from .types import BuildError, ErrorSeverity

class MissingKeyException (Exception):
    pass

class JSONSchemaResource:
    path : Path
    raw : str
    json : dict
    id : str
    spec : str

    def __init__(self, path, build_errors : List[BuildError]):
        self.path = path
        self.raw = path.read_text()
        self.json = loads(self.raw)
        if "$id" in self.json.keys():
            self.id = self.json['$id']
        else:
            raise MissingKeyException("Schema has no $id key")
        if '$schema' in self.json.keys():
            self.spec = self.json['$schema']
        else:
            build_errors.append(BuildError(path, ErrorSeverity.WARNING, MissingKeyException("Schema {id} has no specification ('$schema') key")))
            self.spec = "https://json-schema.org/draft/2020-12/schema"
            self.json['$schema'] = "https://json-schema.org/draft/2020-12/schema"

class JSONSchema(Schema):
    def __init__(self, core_schema : Path, supporting_schemas : List[Path]):
        super().__init__(core_schema, supporting_schemas, ["schema.json"])

    def build(self) -> bool:
        self.build_errors.clear()
        self.built_ok = False

        try:
            self.core_schema = JSONSchemaResource(self.core_schema_path, self.build_errors)
        except Exception as ex:
            self.build_errors.append(BuildError(self.core_schema_path, ErrorSeverity.ERROR, ex))
            self.core_schema = None

        self.supporting_schemas = []
        for path in self.supporting_schemas_paths:
            try:
                self.supporting_schemas.append(JSONSchemaResource(path, self.build_errors))
            except Exception as ex:
                self.build_errors.append(BuildError(path, ErrorSeverity.ERROR, ex))
        
        if self.core_schema is None:
            return False
        
        try:
            self.registry = Registry().with_contents([(r.id, r.json) for r in self.supporting_schemas] + [(self.core_schema.id, self.core_schema.json)])
            self.validator = Draft202012Validator(self.core_schema.json, registry=self.registry)
            Draft202012Validator.check_schema(self.core_schema.json)
        except Exception as ex:
            self.build_errors.append(BuildError(None, ErrorSeverity.ERROR, ex))
            return False
        
        ref_errors = self._check_all_refs()
        if len(ref_errors) > 0:
            self.build_errors += ref_errors
            return False
        
        self.built_ok = True
        return True

    def _check_all_refs(self) -> List[Exception]:
        errors = self._check_refs(self.core_schema)
        for other_schema in self.supporting_schemas:
            errors += self._check_refs(other_schema)
        return errors
    
    def _check_refs(self, schema) -> List[Exception]:
        refs = list(self._recursively_find_refs(schema.json))
        resource = self.registry.get(schema.id)
        resolver = self.registry.resolver_with_root(resource)
        errors = []
        for key, ref in refs:
            try:
                resolver.lookup(ref)
            except Unresolvable as ex:
                errors.append(BuildError(schema.path, ErrorSeverity.ERROR, ex))
        return errors
    
    def _recursively_find_refs(self, j) -> Generator[Tuple[str, str], None, None]:
        if isinstance(j, dict):            
            for k,v in j.items():
                if k == "$ref":
                    yield k,v
                else:
                    yield from self._recursively_find_refs(v)
        elif isinstance(j, list):
            for i in j:
                yield from self._recursively_find_refs(i)
        else:
            return

    def validate(self, instance_doc: Path) -> List[Exception]:
        try:
            instance_json = loads(instance_doc.read_text())
        except JSONDecodeError as ex:
            return [ex]
        return list(self.validator.iter_errors(instance_json))
