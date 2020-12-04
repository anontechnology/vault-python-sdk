## Anontech Python ViziVault Bindings

### Project Description
Anontech vizivault is designed to make the retrieval and storage of personal and sensitive information easy. Our multi-layer encryption/decryption layer will make your data secure and accesable only to memebrs of your organization on a "need-to-use" basis. Data providers, individuals, end users, and even developers can rest safe knownign their personal data is stored securely, access is monitored, and thier most personal data is kept securely seperate from day to day business operations. Personal data is there when you need it most to support business operations and disapers back into the vault when it's not needed. Safe and secure.


### Support
Please report bugs and issues to support@anontech.io

### Requirements
Only `Python 3` is currently supported.

The basic third party dependencies are the requests and pytest. Libraries installation happens automatically during setup.

### Installaion
```
pip install -e git://github.com/anontechnology/vault-python-sdk.git/#egg=vizivault
```

### Importing the Module
```
import vizivault
```

Alternatively you can just take the vault class

```
from vizivault import ViziVault
```

### Authentication
You must provide an application identifier or api key for all operations to identify you and your application to the vault for authenticaion. For data insertion you need to provide a valid encryption key. For data retrieval you need to apply a valid decryption key.

We recommend at a minimum putting your encryption and decryption key locally in a secure location and refer to it with a filehandle.

### Quick start

#### Attaching to your Vault

```
with open('./my_secure_file/test_encryption_key.txt', 'r') as encryption_file:
    encryption_key = encryption_file.read()
with open('./my_secure_file/test_decryption_key.txt', 'r') as decryption_file:
vault = vizivault.ViziVault(base_url='http://localhost:8083', api_key='12345', encryption_key=encryption_key,
                  decryption_key=decryption_key)`
```

#### Attributes

[Attributes](https://docs.anontech.io/glossary/attribute/) are how the ViziVault ecosystem organizes your data. Every data point consists of three main components: a user id, which represents who the data is about; a value, which is some piece of information about the user; and an attribute, which expresses the relationship between the user and the value. For example, in an online retail application, there would be an attribute for shipping addresses, an attribute for billing addresses, and an attribute for credit card information.

#### Adding an Attribute to an Entity or User

[Attributes](https://docs.anontech.io/glossary/attribute/) are stored as key/value pairs of strings. Both Users and Entities can have Attributes set to them. If there is an existing Attribute in the system with the key of the provided Attribute, that Attribute will be updated; otherwise, a new Attribute will be created.

```
// Retrieving all attributes for a user
new_user = User("exampleUser")
new_user.add_attribute(attribute="FIRST_NAME", value="Jane")
vault.save(new_user)

// Adding an Attribute to entity
entity = vault.find_by_entity("exampleClient")
entity.add_attribute(attribute="FULL_ADDRESS", value="1 Hacker Way, Beverly Hills, CA 90210")
vault.save(entity)
```



### Retrieving all Attributes of an Entity or User
Retrieves all [Attributes](https://docs.anontech.io/glossary/attribute/) for the specified entity or user. Returns a list of Attribute objects

```
# Retrieving all attributes for a user
user = vault.find_by_user(entityid = "User1234")
attributes = user.get_attributes()

# Retrieving all attributes for an entity
entity = vault.find_by_entity(entityid = "Client6789")
attributes = entity.get_attributes
````

### Searching

To search a Vault for [Attributes](https://docs.anontech.io/glossary/attribute/) , pass in a SearchRequest. A list of matching Attributes will be returned. For more information, read about ViziVault search.

```
attributes = vault.search(SearchRequest(attribute = "LAST_NAME", value = "Doe"))
```

### Deleting User Attributes
```
// Purging all user attributes
User user = vault.find_by_user(entitiyid = "User1234");
vault.purge(user);

// Removing specific attribute
User user = vault.find_by_user(entityid = "User1234");
user.clear_attribute("LAST_NAME");
vault.save(user);
```

### Attribute Definitions

[Attributes](https://docs.anontech.io/glossary/attribute/) define an object, housing all relevant metadata for the key. This is how Tags and Regulations become associated with attributes. Attributes can be comprised of a schema to further break down the structure of the value of the Attribute. Display names and hints can also be added to the Attribute Definition for ease of use and readability.

#### Storing an Attribute Definition in the Vault

To store an Attribute Definition, create an AttributeDefinition object and save it to the Vault. The following code details the various properties of the AttributeDefinition object.

```
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
    immutable = false,
    mandatory = true,
    indexed = false,
    regulations = ["GDPR", "CCPA"]
    
)

vault.storeAttribute(attribute)
```

### Tags

Similar to [Regulations](https://docs.anontech.io/glossary/regulation/) , [Tags](https://docs.anontech.io/api/tags/) are user-defined strings that can be applied to Attributes to aid in classification and searching.


#### Storing a Tag in the vault

To store a new [Tag](https://docs.anontech.io/api/tags/) , create a Tag object and save it to the Vault.

```
vault.store_tag(tag = "Financial Data")
```

#### Retrieving Tags from the Vault

[Tags](https://docs.anontech.io/api/tags/) can be retrieved as a list of Tag objects or as a single Tag if the specific Tag is specified.

```
# Retrieving all tags
tags = vault.tags

# Retrieving specific tag
tag = vault.get_tag(name = "Financial Data")
```

#### Deleting Tags from the Vault

To remove a [Tag](https://docs.anontech.io/api/tags/) , specify the Tag to be removed. A boolean denoting the status of the operation will be returned.

```

# Removing a specific tag
removed = vault.remove_tag(name = "Financial Data")

```

### Regulations

A regulation object represents a governmental regulation that impacts how you can use the data in your vault. Each data point can have a number of regulations associated with it, which makes it easier to ensure your use of the data is compliant. You can tag data points with regulations when entering them into the system, or specify rules that the system will use to automatically tag regulations for you.

#### Storing a Regulation in the Vault

To store a [Regulation](https://docs.anontech.io/glossary/regulation/) to the Vault, create a new Regulation object and save it to the Vault. The constructor takes the key, name, and url of the Regulation.


```
# Storing a regulation
regulation = Regulation(key = "GDPR", 
                         name = "General Data Protection Regulation",
                         url =  "https://gdpr.eu/" 
                        )
saved_regulation = vault.save(regulation)

```

#### Retrieving Regulations from the Vault

[Regulations](https://docs.anontech.io/glossary/regulation/) can be retrieved as a list of Regulation objects or as a single Regulation if the specific Regulation is specified.

```
# Retrieving all regulations
regulations = vault.regulations

# Retrieving specific regulation
regulation = vault.get_regulation(key = "GDPR")
```

#### Deleting Regulations from the Vault

To remove a [Regulation](https://docs.anontech.io/glossary/regulation/) , specify the Regulation to be removed. A boolean denoting the status of the operation will be returned.

```
# Removing a specific regulation
removed = vault.remove_regulation(key = "GDPR")
```

