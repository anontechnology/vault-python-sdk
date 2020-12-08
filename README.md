## Anontech Python ViziVault Bindings

### Project Description
AnonTech's ViziVault system is designed to make the retrieval and storage of personal and sensitive information easy. Our multi-layer encryption/decryption system will make your data secure and accessible only to memebrs of your organization on a "need-to-use" basis. Data providers, individuals, end users, and even developers can rest safe knowing that their personal data is stored securely, access is monitored, and their most personal data is kept securely, seperate from day-to-day business operations. Personal data is there when you need it most to support business operations, and disappears back into the vault when it's not needed, so that your system can be safe and secure.


### Support
Please report bugs and issues to support@anontech.io

### Requirements
Only `Python 3` is currently supported.

The basic third party dependencies are `requests` and `pytest`, which are set up automatically by pip on installation.

### Installaion
```
pip install -e git://github.com/anontechnology/vault-python-sdk.git/#egg=vizivault
```

### Importing the Module
```python
import vizivault
```

Alternatively, it is possible to just take the vault class:

```python
from vizivault import ViziVault
```

### Authentication
You must provide an application identifier or api key for all operations, to identify you and your application to the vault for authenticaion. For data insertion, a valid encryption key is necessary. For data retrieval, a valid decryption key is necessary.

We recommend at a minimum putting your encryption and decryption key locally in a secure location, such as a local file on disk.

### Quick start

#### Attaching to your Vault

```python
with open('./my_secure_file/test_encryption_key.txt', 'r') as encryption_file:
    encryption_key = encryption_file.read()
with open('./my_secure_file/test_decryption_key.txt', 'r') as decryption_file:
    decryption_key = decryption_file.read()
vault = vizivault.ViziVault(base_url='http://localhost:8083', api_key='12345', encryption_key=encryption_key,
                  decryption_key=decryption_key)`
```

#### Attributes

[Attributes](https://docs.anontech.io/glossary/datapoint/) are how the ViziVault ecosystem organizes your data. Every attribute consists of three main components: a user id, which represents who the data is about; a value, which is some piece of information about the user; and an attribute name, which expresses the relationship between the user and the value. For example, in an online retail application, there would be an attribute for shipping addresses, an attribute for billing addresses, and an attribute for credit card information.

#### Adding an Attribute to an Entity or User

```python
# Retrieving all attributes for a user
new_user = User("exampleUser")
new_user.add_attribute(attribute="FIRST_NAME", value="Jane")
vault.save(new_user)

# Adding an Attribute to entity
entity = vault.find_by_entity("exampleClient")
entity.add_attribute(attribute="FULL_ADDRESS", value="1 Hacker Way, Beverly Hills, CA 90210")
vault.save(entity)
```



### Retrieving all Attributes of an Entity or User
Retrieves all [Attributes](https://docs.anontech.io/glossary/datapoint/) for the specified entity or user. Returns a list of attribute objects.

```python
# Retrieving all attributes for a user
user = vault.find_by_user(entityid = "User1234")
attributes = user.get_attributes()

# Retrieving all attributes for an entity
entity = vault.find_by_entity(entityid = "Client6789")
attributes = entity.get_attributes()
```

### Searching

To search a vault for [Attributes](https://docs.anontech.io/glossary/datapoint/) , pass in a SearchRequest. A list of matching Attributes will be returned. For more information, read about [ViziVault Search](https://docs.anontech.io/tutorials/search/).

```python
attributes = vault.search(SearchRequest(attribute = "LAST_NAME", value = "Doe"))
```

### Deleting User Attributes
```
# Purging all user attributes
User user = vault.find_by_user(entitiyid = "User1234");
vault.purge(user);

# Removing specific attribute
User user = vault.find_by_user(entityid = "User1234");
user.clear_attribute("LAST_NAME");
vault.save(user);
```

### Attribute Definitions

[Attribute definitions](https://docs.anontech.io/glossary/attribute/) define an object that contains all relevant metadata for attributes with a given `key`. This is how tags and regulations become associated with attributes. Attributes can contain a schema to further break down the structure of their value. Display names and hints can also be added to the Attribute Definition for ease of use and readability.

#### Storing an Attribute Definition in the Vault

To store an Attribute Definition, create an AttributeDefinition object and save it to the Vault. The following code details the various properties of the AttributeDefinition object.

```python
attribute = AttributeDefinition(
    name = "Billing Address",
    tags = ["geographic_location", "financial"],
    hint = "{ line_one: \"1 Hacker Way\", line_two: \"Apt. 53\", city: \"Menlo Park\", state: \"California\", postal_code: \"94025-1456\" country: \"USA\" }",
    schema = json.dumps({ 
                    "line_one": "string",
                    "line_two": "string",
                    "city": "string",
                    "state": "string",
                    "postal_code": "string",
                    "country": "string"
                  })
    repeatable = false,
    indexed = false,
    regulations = ["GDPR", "CCPA"]
)

vault.storeAttribute(attribute)
```

### Tags

Similar to [Regulations](https://docs.anontech.io/glossary/regulation/) , [Tags](https://docs.anontech.io/api/tags/) are user-defined strings that can be applied to Attributes to aid in classification and searching.


#### Storing a Tag in the vault

To store a new [Tag](https://docs.anontech.io/api/tags/) , create a Tag object and save it to the Vault.

```python
vault.store_tag(tag = "Financial Data")
```

#### Retrieving Tags from the Vault

[Tags](https://docs.anontech.io/api/tags/) can be retrieved as a list of Tag objects or as a single Tag if the specific Tag is specified.

```python
# Retrieving all tags
tags = vault.tags

# Retrieving specific tag
tag = vault.get_tag(name = "Financial Data")
```

#### Deleting Tags from the Vault

To remove a [Tag](https://docs.anontech.io/api/tags/) , specify the Tag to be removed. A boolean denoting the status of the operation will be returned.

```python
# Removing a specific tag
removed = vault.remove_tag(name = "Financial Data")

```

### Regulations

A regulation object represents a governmental regulation that impacts how you can use the data in your vault. Each data point can have a number of regulations associated with it, which makes it easier to ensure your use of the data is compliant. You can tag data points with regulations when entering them into the system, or specify rules that the system will use to automatically tag regulations for you.

#### Storing a Regulation in the Vault

To store a [Regulation](https://docs.anontech.io/glossary/regulation/) to the Vault, create a new Regulation object and save it to the Vault. The constructor takes the key, name, and url of the Regulation.


```python
# Storing a regulation
regulation = Regulation(key = "GDPR", 
                         name = "General Data Protection Regulation",
                         url =  "https://gdpr.eu/" 
                        )
saved_regulation = vault.save(regulation)

```

#### Retrieving Regulations from the Vault

[Regulations](https://docs.anontech.io/glossary/regulation/) can be retrieved as a list of Regulation objects or as a single Regulation if the specific Regulation is specified.

```python
# Retrieving all regulations
regulations = vault.regulations

# Retrieving specific regulation
regulation = vault.get_regulation(key = "GDPR")
```

#### Deleting Regulations from the Vault

To remove a [Regulation](https://docs.anontech.io/glossary/regulation/) , specify the Regulation to be removed. A boolean denoting the status of the operation will be returned.

```python
# Removing a specific regulation
removed = vault.remove_regulation(key = "GDPR")
```

