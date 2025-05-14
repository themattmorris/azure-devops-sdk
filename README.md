# azure-devops-sdk

Just because [the existing one](https://github.com/microsoft/azure-devops-python-api) is a little clunky without type hinting.

## Usage

```python
from ado import Client


client = Client(organization="my_organization", project="my_project")

# List all repos
repos = client.git.repositories.list_all()
```
