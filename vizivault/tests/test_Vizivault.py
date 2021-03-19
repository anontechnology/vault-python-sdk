import pytest
import os
import csv
from vizivault import ViziVault, SearchRequest, User, AttributeDefinition, Attribute, Tag, VaultResponseException,\
    Regulation
from vizivault.rules import ConjunctiveRule, AttributeRule, AttributeListOperator, UserRule, UserValuePredicate


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
    attribute_def2.repeatable = True
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
    vault.purge(new_user.id)


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
        vault.purge(new_user.id)


def test_repearted_attribute_save(vault):
    ## Create Attribute
    attribute_def2 = AttributeDefinition("TestAttribute2")
    vault.store_attribute_definition(attribute_definition=attribute_def2)
    new_user = User("example2User")

    try:
        new_user.add_attribute(attribute=attribute_def2.name, value="ExampleA")
        new_user.add_attribute(attribute=attribute_def2.name, value="ExampleB")
        attribute_def2.repeatable = True
        vault.save(new_user)
        user_response = vault.find_by_user('example2User')
        assert sorted(list(map(lambda x: x.value, user_response.get_attribute('TestAttribute2')))) == ['ExampleA',
                                                                                                       'ExampleB']

    finally:
        vault.purge(new_user.id)


def test_search(vault):
    attribute_def1 = AttributeDefinition("TestAttribute1")
    attribute_def1.indexed = True
    attribute_def2 = AttributeDefinition("TestAttribute2")
    attribute_def2.repeatable = True
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
        vault.purge(new_user.id)
        vault.purge(new_user_2.id)


def test_datapoint(vault, new_user):
    received_user = vault.find_by_user(new_user.id)
    for attribute in received_user.get_attributes():
        assert attribute.dataPointId == vault.get_data_point(attribute.dataPointId).dataPointId

def test_get_user_attribute(vault, new_user):
    received_data = vault.get_user_attribute("exampleUser", 'TestAttribute1')
    assert len(received_data) == 1
    assert received_data[0].value == 'Example1'

    received_data = vault.get_user_attribute("exampleUser", "TestAttribute2")
    assert len(received_data) == 2
    assert received_data[0].value == 'ExampleA'
    assert received_data[1].value == 'ExampleB'

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
        vault.purge(new_user.id)
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


def test_quickstart():
    # 1. Replace 'my_encryption_file.txt'  with the path to your encryption file

    with open('./resources/test_encryption_key.txt', 'r') as encryption_file:
        encryption_key = encryption_file.read()

    # 2 Replace 'my_decryption_file.txt' with the path to your decryption file
    with open('./resources/test_decryption_key.txt', 'r') as decryption_file:
        decryption_key = decryption_file.read()


    # Connect to the vault
    # 3 Replace 'https://my.host:8080' with the web address and port of your vault server
    # 4 replace '12345' with the api key (application key) of your application.

    vault = ViziVault(base_url='http://localhost:8083', api_key='12345', encryption_key=encryption_key,
                      decryption_key=decryption_key)

    eye_color_attribute_def = AttributeDefinition(name="EyeColor", hint="Green")
    age_attribute_def = AttributeDefinition(name="Age", hint="18")

    vault.store_attribute_definition(attribute_definition=eye_color_attribute_def)
    vault.store_attribute_definition(attribute_definition=age_attribute_def)

    name_attribute_def = AttributeDefinition(
        name="ClientName",
        hint="{first_name: \"Agnes\","
             "last_name: \"Driscoll\","
             "middle_name: \"May\","
             "nickname: \"Madame X\","
             "company: \"Hebern Electric\"}",
        schema={
            "first_name": "string",
            "last_name": "string",
            "middle_name": "string",
            "nickname": "string",
            "company": "string"})

    address_attribute_def = AttributeDefinition(
        name="BillingAddress",
        hint="{street: \"1 Hacker Way\","
             "apt: \"Apt. 53\", "
             "city: \"Menlo Park\", "
             "state: \"California\", "
             "postal_code: \"94025-1456\", "
             "country: \"USA\"}",
        schema={
            "street": "string",
            "apt": "string",
            "city": "string",
            "state": "string",
            "postal_code": "string",
            "country": "string"
        })


    vault.store_attribute_definition(attribute_definition=name_attribute_def)
    vault.store_attribute_definition(attribute_definition=address_attribute_def)

    with open('./resources/tutorial_test.csv', 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        header_row = True

        user_data = {}
        for row in csv_reader:
            if header_row:
                headers = row
                header_row = False
            else:
                for index, name in enumerate(headers, start=0):
                    user_data[name] = row[index]

                # Create a User
                new_user = User(user_data['USERID'])

                # Add the "lat attribute values
                new_user.add_attribute(attribute=eye_color_attribute_def.name, value=user_data["EYE_COLOR"])
                new_user.add_attribute(attribute=age_attribute_def.name, value=user_data["AGE"])

                # Create a dictionary for the user
                user_name = {
                    "first_name": user_data["FIRST_NAME"],
                    "last_name": user_data["LAST_NAME"],
                    "middle_name": user_data["MIDDLE_NAME"],
                    "company": user_data["COMPANY"]
                }

                # Save the User
                new_user.add_attribute(attribute=name_attribute_def.name, value=user_name)

                # Create a dictionary for the address
                address = {
                    "street": user_data["STREET"],
                    "city": user_data["CITY"],
                    "state": user_data["STATE"],
                    "country": user_data["COUNTRY"]
                }

                # Save the Address
                new_user.add_attribute(attribute=address_attribute_def.name, value=address)

                vault.save(new_user)


    with open('./resources/tutorial_test.csv', 'r') as csv_file_2:
        csv_reader = csv.reader(csv_file_2, delimiter=',')
        header_row = True

        user_data = {}
        for row in csv_reader:
            if header_row:
                  headers = row
                  header_row = False
            else:
                for index, name in enumerate(headers, start=0):
                    user_data[name] = row[index]
                user = User(user_data['USERID'])
                received_user = vault.find_by_user(entity_id=user.id)
                for attribute in received_user.get_attributes():
                    print('Attribute:' + attribute.attribute + 'Value:' + str(attribute.value))

                vault.purge(entity_id=user.id)
