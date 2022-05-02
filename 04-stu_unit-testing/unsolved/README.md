# Task 

Write unit tests for the transformations created in the previous step. 

Unit tests take on the following format: 
1. Assemble: Set up the `test df` and `expected df`
2. Act: pass the `test df` into the function and return the `output df` 
3. Assert: validate that the `output df` matches the `expected df`

Using PyTest for example, the steps look as follows: 

```python
import pandas as pd
from datetime import datetime
from my_functions import *

def test_lowercase_all_columns():
    # ASSEMBLE
    test_data = [
        {
            "ID": 1,
            "First_Name": "Bob",
            "Last_Name": "Builder",
            "Age": 24
        },
        {
            "ID": 2,
            "First_Name": "Sam",
            "Last_Name": "Smith",
            "Age": 41
        }
    ]
    test_df = pd.DataFrame(test_data)

    expected_df = pd.DataFrame({
        "id": [1, 2],
        "first_name": ["Bob", "Sam"],
        "last_name": ["Builder", "Smith"],
        "age": [24, 41]
    })

    # ACT 
    output_df = lowercase_all_column_names(test_df)
    
    # ASSERT
    pd.testing.assert_frame_equal(left=expected_df,right=output_df, check_exact=True)
```

To run all tests in the current directory, run: 
```
pytest .
```

### Pre-requisites 

Install the following libraries: 

```
pip install pytest
```

### Step 1: Write unit tests for both functions 

Write unit tests for both transformation functions written in the previous step. 

You may use the following input_df and expected_df for the `convert_unix_timestamp` function. 

```python
input_df = pd.DataFrame({
        "id": [1,2],
        "timestamp1": [1638368789,1638369080], 
        "timestamp2": [1638369141,1638369162]
})

expected_df = pd.DataFrame({
    "id": [1,2], 
    "timestamp1": [dt.datetime(2021,12,1,14,26,29), dt.datetime(2021,12,1,14,31,20)], 
    "timestamp2": [dt.datetime(2021,12,1,14,32,21), dt.datetime(2021,12,1,14,32,42)]
})
```

Hints: 
- Your python script name must begin with `test_`
- Your test function name must begin with `test_`

### Step 2: Run unit tests 

Run your unit tests by executing: 
```
pytest .
```

You should see the following output if tests run successfully: 

```
==== test session starts ====
platform darwin -- Python 3.7.11, pytest-6.2.5, py-1.11.0, pluggy-1.0.0
rootdir: ~/data-engineering-101/04-stu_unit-testing/solved
collected 2 items                               
==== 2 passed in 0.41s ====
```