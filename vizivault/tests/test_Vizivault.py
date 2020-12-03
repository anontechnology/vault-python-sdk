import pytest
import os
from vizivault import ViziVault, SearchRequest, User, AttributeDefinition, Attribute, Tag, \
    VaultResponseException, Regulation, ConjunctiveRule, AttributeRule, AttributeListOperator, \
    UserRule, UserValuePredicate


@pytest.fixture
def vault():
    path = os.getcwd()
    with open('./resources/test_encryption_key.txt', 'r') as encryption_file:
        encryption_key = encryption_file.read()
    with open('./resources/test_decryption_key.txt', 'r') as decryption_file:
        decryption_key = decryption_file.read()
    vault = ViziVault(base_url='http://localhost:8083', api_key='12345', encryption_key=encryption_key,
                      decryption_key=decryption_key)
    return vault


@pytest.fixture
def attribute_def1(vault):
    # Create attributes
    attribute_def1 = AttributeDefinition("TestAttribute1")
    vault.store_attribute_definition(attribute_definition=attribute_def1)
    return attribute_def1


@pytest.fixture
def attribute_def2(vault):
    # Create attributes
    attribute_def2 = AttributeDefinition("TestAttribute2")
    attribute_def2.Repeatable = True
    vault.store_attribute_definition(attribute_definition=attribute_def2)
    return attribute_def2


@pytest.fixture
def new_user(vault, attribute_def1, attribute_def2):
    # Create User
    new_user = User("exampleUser")
    new_user.add_attribute(attribute=attribute_def1.name, value="Example1")
    new_user.add_attribute(attribute=attribute_def2.name, value="ExampleA")
    new_user.add_attribute(attribute=attribute_def2.name, value="ExampleB")

    vault.save(new_user)
    yield new_user
    vault.purge(new_user)


def test_load(vault):
    ## Create Attribute
    attribute_def1 = AttributeDefinition("TestAttribute1")
    vault.store_attribute_definition(attribute_definition=attribute_def1)
    new_user = User("exampleUser")

    try:
        new_user.add_attribute(attribute=attribute_def1.name, value="Example1")
        vault.save(new_user)
        user_response = vault.find_by_user('exampleUser')
        assert user_response.get_attribute('TestAttribute1').value == 'Example1'

    finally:
        vault.purge(new_user)


def test_repearted_attribute_save(vault):
    ## Create Attribute
    attribute_def2 = AttributeDefinition("TestAttribute2")
    vault.store_attribute_definition(attribute_definition=attribute_def2)
    new_user = User("example2User")

    try:
        new_user.add_attribute(attribute=attribute_def2.name, value="ExampleA")
        new_user.add_attribute(attribute=attribute_def2.name, value="ExampleB")
        attribute_def2.Repeatable = True
        vault.save(new_user)
        user_response = vault.find_by_user('example2User')
        assert sorted(list(map(lambda x: x.value, user_response.get_attribute('TestAttribute2')))) == ['ExampleA',
                                                                                                       'ExampleB']

    finally:
        vault.purge(new_user)


def test_search(vault):
    attribute_def1 = AttributeDefinition("TestAttribute1")
    attribute_def1.indexed = True
    attribute_def2 = AttributeDefinition("TestAttribute2")
    attribute_def2.Repeatable = True
    vault.store_attribute_definition(attribute_definition=attribute_def1)
    vault.store_attribute_definition(attribute_definition=attribute_def2)
    new_user = User("ExampleUser")
    new_user_2 = User("ExampleUser2")

    new_user.add_attribute(attribute=attribute_def1.name, value="ExampleA")
    vault.save(new_user)

    new_user_2.add_attribute(attribute=attribute_def1.name, value="ExampleA")
    new_user_2.add_attribute(attribute=attribute_def2.name, value="ExampleB")
    vault.save(new_user_2)

    try:
        search_request = SearchRequest()
        search_request.add_value_query(attribute_def1.name, "ExampleA")
        search_request.attributes = [attribute_def2.name]

        results = vault.search(search_request, 0, 10)
        assert len(results) == 3
        assert len([result for result in results if
                    (result.userId == new_user.id and result.attribute == attribute_def1.name)]) == 1
        assert len([result for result in results if
                    (result.userId == new_user_2.id and result.attribute == attribute_def1.name)]) == 1
        assert len([result for result in results if
                    (result.userId == new_user_2.id and result.attribute == attribute_def2.name)]) == 1
    finally:
        vault.purge(new_user)
        vault.purge(new_user_2)


def test_datapoint(vault, new_user):
    received_user = vault.find_by_user(new_user.id)
    for attribute in received_user.get_attributes():
        assert attribute.dataPointId == vault.get_data_point(attribute.dataPointId).dataPointId


def test_tags(vault):
    # Create attributes
    attribute_def1 = AttributeDefinition("TestAttribute1")
    attribute_def1.tags = ['tag1']
    vault.store_attribute_definition(attribute_definition=attribute_def1)

    # Create User
    new_user = User("exampleUser")
    new_user.tags = ['tag2']

    try:
        # Check tags
        attribute1 = Attribute(attribute=attribute_def1.name)
        attribute1.value = 'ExampleA'
        attribute1.tags = ['tag3']
        new_user.add_attribute(attribute1)
        vault.save(new_user)
        received_attribute = vault.find_by_user("exampleUser").get_attribute(attribute_def1.name)
        assert len(received_attribute.tags) == 3
        assert sorted(received_attribute.tags) == ['tag1', 'tag2', 'tag3']

        # Add tag and get all tags
        new_tag = Tag("tag4")
        vault.store_tag(new_tag)
        all_tags = vault.get_tags()
        assert sorted(list(map(lambda x: x.name, all_tags))) == ['tag1', 'tag2', 'tag3', 'tag4']

        # Get Tag
        with pytest.raises(VaultResponseException):
            vault.get_tag("tag5")

        assert vault.delete_tag("tag5") == False

        # Delete Tags
        vault.delete_tag("tag1")
        vault.delete_tag("tag2")
        vault.delete_tag("tag3")
        vault.delete_tag("tag4")

        all_tags = vault.get_tags()
        assert sorted(list(map(lambda x: x.name, all_tags))) == []

    finally:
        vault.purge(new_user)
        vault.delete_tag("tag1")
        vault.delete_tag("tag2")
        vault.delete_tag("tag3")
        vault.delete_tag("tag4")


def test_regulations(vault):
    test_regulation = Regulation(name="RegulationName", key="RegulationKey")
    attribute_def1 = AttributeDefinition("TestAttribute1")

    vault.store_attribute_definition(attribute_definition=attribute_def1)

    # Load one regulation
    rootrule = ConjunctiveRule()
    rootrule.add_rule(AttributeRule(attributes=[attribute_def1.name], operator=AttributeListOperator.ANY))
    rootrule.add_rule(
        UserRule(attribute=attribute_def1.name, predicate=UserValuePredicate.EQUALS, value="Test AttributeValue"))

    test_regulation.rule = rootrule
    vault.store_regulation(test_regulation)
    received_regulation = vault.get_regulation(key=test_regulation.key)

    # Test regulation is there
    assert test_regulation.name == received_regulation.name
    all_regulations = vault.get_regulations()

    # Test getting all regulations
    assert test_regulation.name in sorted(list(map(lambda x: x.name, all_regulations)))

    # Test Deleting a regulation
    vault.delete_regulation(test_regulation.key)

    # Test getting all regulations
    all_regulations = vault.get_regulations()
    assert test_regulation.name not in sorted(list(map(lambda x: x.name, all_regulations)))


def test_attribute_definition(vault):
    attribute_def1 = AttributeDefinition("TestAttribute1")
    attribute_def1.indexed = True
    vault.store_attribute_definition(attribute_definition=attribute_def1)

    received_definition = vault.get_attribute_definition(attribute_def1.name)

    assert received_definition.indexed

    attribute_definitions = vault.get_attribute_definitions()
    assert received_definition in attribute_definitions


def test_error_condition(vault, new_user):
    attribute_def3 = AttributeDefinition(name='InvalidAttribute')
    new_user.add_attribute(attribute=attribute_def3.name, value="ExampleA")

    with pytest.raises(VaultResponseException):
        vault.save(new_user)
