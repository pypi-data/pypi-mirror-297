# Circular Python API

Brief description of the Python package, including its main purpose and key features.

## Installation

You can install the package via pip. Here's how to do it:

```bash
pip install .
```

## Usage

Explain how to use the package and provide some basic examples to get users started.

```python
from circular_api import Circular

# Example usage
circular = Circular()
blockchain = 0x8a20baa40c45dc5055aeb26197c203e576ef389d9acb171bd62da11dc5ad72b2
test_addr = 0xbd1d7ff426d094605a0902c78812dded6bbebdb42b20d9c722dc87bde0f30f44

print(circular.getWallet(blockchain, test_addr))

```

### Access data

The result is a Python dictionary so you could access values via the `.get()` method.

## License

MIT License (MIT)

## Contact

- Author: Danny De Novi
- Email: dannydenovi29@gmail.com

---
