# Hprogressbars

Hprogressbars is a Python library that creates horizontal progress bars to keep 
track of the progress of threaded jobs. 

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install foobar.

```bash
pip install hprogressbar
```

## Usage

```python
from hprogressbars import *

progressbars = ProgressBars(num_bars=5)
progressbars.set_last_bar_as_total_progress(prefix="Total Progress: ")

# using the same thread 
for i in range(101):
    # zero is assigned to start the value of the total progress
    values = [i, i+5, i+10, i+15, 0] 
    progressbars.update_all(values) # update bars in the same thread
progressbars.finish_all() # avoid memory leaks. 

```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)