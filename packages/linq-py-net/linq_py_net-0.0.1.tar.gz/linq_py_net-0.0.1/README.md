# linq_py_net

The linq_py_net package is used to manage list collections:

| methods          | description                                            |
| ---------------- | ------------------------------------------------------ |
| where            | filter itens by lambda predicate                       |
| count            | count itens, lambda predicate is optiona               |
| first_or_default | find first item on the sequence, predicate is optional |
| select           | project data from list                                 |

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install linq_py_net

```bash
pip install linq_py_net
```

# Usage

```python
from linq_py_net import List

linq = List([1,2,3,4,5,6,7,8,9,10])

linq.first_or_default() # 1

pares = linq.where(lambda x: x % 2 == 0) # [2,4,6,8,10]
pares.count() # 5
pares.count(lambda x: x > 6) # 2

project = (
    linq.where(lambda x: x % 2 == 0)
        .select(lambda x: { "item": x })
)
```

## Author

Wellington Junior
