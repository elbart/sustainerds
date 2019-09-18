from sustainerds.api.core.resource import (
    RequestSchemaSpec,
    ResourceSchemaSpec,
    ResponseSchemaSpec,
    SchemaSpec,
)


def test_resource_schema_spec_get_methods():
    spec = ResourceSchemaSpec(name="Test")
    assert len(spec.get_methods()) == 0

    spec = ResourceSchemaSpec(
        name="Test2",
        GET=SchemaSpec(request=RequestSchemaSpec(), response=ResponseSchemaSpec()),
        HEAD=SchemaSpec(request=RequestSchemaSpec(), response=ResponseSchemaSpec()),
    )

    op_names = [x[0] for x in spec.get_methods()]
    assert len(op_names) == 2
    assert "GET" in op_names
    assert "HEAD" in op_names
