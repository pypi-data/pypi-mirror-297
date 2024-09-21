# PyGCA
**PYTHON OPERATOR DETECTION & ANALYSIS**

| ![Mental Calculation](https://upload.wikimedia.org/wikipedia/commons/thumb/9/9c/Mental_calculation_at_primary_school.jpg/320px-Mental_calculation_at_primary_school.jpg) |
|:--:|
| Mental Calculation |

## Overview
**PyGCA** is a Python library, independently developed and actively maintained to detect, analyze, and optimize operator usage in Python codebases. With a focus on efficiency and ease of use, this tool empowers developers to identify performance bottlenecks and potential vulnerabilities stemming from operator misuse.

The library covers __all major operator categories__, providing insights into how operators interact within the code and where optimizations can improve overall performance. As an actively maintained project, __PyGCA__ continually evolves to stay relevant with Python’s latest updates and to incorporate user feedback for better functionality.

<p align="center">
  <strong>Important Notice:</strong> This project is not affiliated with or related to the <a href="https://pypi.org/project/PyGC/">PyGC package on PyPI</a>.
</p>

## Key Features
- **Multi-operator detection**:
  - Arithmetic (`+`, `-`, `*`, `/`, etc.)
  - Bitwise (`&`, `|`, `^`, etc.)
  - Comparison (`==`, `!=`, `>`, etc.)
  - Identity (`is`, `is not`)
  - Logical (`and`, `or`, `not`)
  - Membership (`in`, `not in`)
- **Actionable suggestions** for performance improvements
- **Detailed reporting** on operator misuse
- **Customizable settings** for different project needs

> **[!TIP]**
> To better understand the __functional__ areas of each operator category and where they overlap, the following  diagram visually represents the __scope__ of PyGCA:

```plaintext
      +----------------------------+
      |        Logical Operators   |
      |                            |
      |                            |      +---------------------------+
      | +---------+    +---------+ |      |                           |
      | | Bitwise |--> |Comparison |      |   Arithmetic Operators    |
      | +---------+    +---------+ |      |                           |
      |                            |      +---------------------------+
      +----------------------------+  
                                   |
                            +------+---------------------+
                            | Identity & Membership Ops  |
                            +----------------------------+
```
## [Go to Installation](#installation)

**1. Clone the `repository`:**
```bash
   git clone https://github.com/clintaire/PyGCA.git
   cd PyGCA
```
**2. `Install` dependencies:**
```bash
   pip install -r requirements.txt
```

## Usage

__Run__ the __Operator__ Analysis

You can analyze __any__ Python script for __operator__ usage with a simple __command__:

```bash
   python3 -m bot.operator_analysis path/to/your_script.py
```
Here’s a basic Python script with various operators that __PyGCA__ can analyze:

```python
    def analyze_example(a, b):
    # Arithmetic operators
    sum_result = a + b
    diff = a - b
    
    # Logical operators
    if a and b:
        return True
    elif a or b:
        return False

    # Bitwise operators
    result = a & b
    return result
```

**Run PyGCA and Inspect Output / __Basically__ to inspect the code above**

```bash
   python3 -m bot.operator_analysis analyze_example.py
```
**Sample Output:**

```bash
   ["Arithmetic Addition detected at line 4", "Logical AND detected at line 7", "Bitwise AND detected at line 12"]
```
__The following truth table demonstrates logical operator results and their detection by PyGCA:__

|       Expression        |       Expected Result            |     Detected Issue     |
| ----------------------- | -------------------------------- | ---------------------- |
|    True and False       |      False                       |    No issue            |
|    False or True        |      True                        |    No issue            |
|    True and False       |      Data                        |    No issue            |
|    not True             |      False                       |    No issue            |
|    a and not b          |      Depends on vars             |    No issue            |
|    a & b (bitwise AND)  |      Depends on bits             |   Misuse 🔴 Alert!     |


> [!NOTE]
> You can modify PyGCA’s behavior to handle special cases or focus on specific operator categories. To run only the arithmetic or comparison checks, you can adjust configuration files or pass custom flags during execution

**To only check for Arithmetic Operators**

```bash
   python3 -m bot.operator_analysis --check-arithmetic path/to/script.py
```


- When running PyGCA on a larger codebase or a real-world project, it’s important to use modular analysis and profiling techniques to measure performance impact. Here’s how to profile the performance:

```python
   import time
   from bot.arithmetic.arithmetic_checker import ArithmeticOperatorChecker
   from bot.utils import set_parents
   import ast

   # Load large source code
   source_code = """
   def large_function():
    x = 1
   """ * 10000  # Replicate a small function 10,000 times

   # Time the performance
   start_time = time.time()
   tree = ast.parse(source_code)
   set_parents(tree)
   checker = ArithmeticOperatorChecker()
   checker.visit(tree)
   end_time = time.time()

   print(f"Analysis completed in {end_time - start_time} seconds")
```
Running the above :top: code will allow you to test PyGCA on __large__ scripts, and the output will help measure its __efficiency__.

# Testing

**To ensure everything is working, you can run _PyGCA’s_ test suite using pytest. This will validate the detection algorithms against various test cases:**

```bash
   PYTHONPATH=. pytest tests/
```

**Upon successful execution, the terminal output should ⇙ appear as below:**

```python
======================================== test session starts =================================
platform linux -- Python 3.11.2, pytest-8.3.3, pluggy-1.5.0
rootdir: /home/username/PyGCA
collected 10 items                                                                                  

tests/test_arithmetic_checker.py .                                                      [ 10%]
tests/test_bitwise_checker.py .                                                         [ 20%]
tests/test_comparison_checker.py .                                                      [ 30%]
tests/test_identity_checker.py .                                                        [ 40%]
tests/test_logical_checker.py .                                                         [ 50%]
tests/test_membership_checker.py .                                                      [ 60%]
tests/test_operator_detection.py ....                                                   [100%]

======================================== 10 passed in 0.21s ==================================
```


## Contributing

I welcome contributions! If you'd like to contribute to PyGCA, follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bugfix, replacing `my-new-feature` with a descriptive name: `git checkout -b my-feature-name`
3. Make your changes and commit them: `git commit -am 'Add new feature'`
4. Push the branch: `git push origin my-feature-name`
5. Create a new Pull Request.

Make sure to run the tests with `pytest` and ensure everything is working before submitting your PR.

For more details, see the [Contributing Guide](https://github.com/clintaire/PyGCA/blob/PyGCA/CONTRIBUTING.md).

## How to Follow

Join the community and stay updated with the latest changes to PyGCA by following the repository on GitHub:

- Watch the repository to get notifications for updates.
- Star the repository if you find it useful.
- Follow [Clint Airé](https://github.com/clintaire) for updates on PyGCA and other projects.

## Credits

- Image Credit: [Wikipedia](https://en.wikipedia.org/wiki/Arithmetic)

## LICENSE

Copyright 2024-Present Clint Airé.

The [PyGCA](https://github.com/clintaire/PyGCA) repository is released under the [MIT](https://github.com/clintaire/PyGCA/blob/main/LICENSE) license.