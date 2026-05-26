---
name: python-log-injector
description: Adds entry and exit log statements to Python functions
domain: Engineering
namespace: python
version: 1.0.0
visibility: public
author: Shyam Hande
license: MIT

keywords:
  - python
  - logging
  - refactoring
  - observability
---

# Python Log Injector Skill

This skill analyzes Python source files and automatically adds:

- log statement at function start
- log statement before every return
- optional exception logging

Example:

Input:

```python
def add(a, b):
    return a + b

Output:

import logging

logger = logging.getLogger(__name__)

def add(a, b):
    logger.info("Entering add")

    result = a + b

    logger.info("Exiting add")

    return result