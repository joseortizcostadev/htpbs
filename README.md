# Hprogressbars

Hprogressbars is a Python library that creates horizontal progress bars to keep 
track of the progress of threaded jobs. 

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install hprogressbars.

```bash
pip install hprogressbar
```

## Usage

The following are examples about how to use this library for threaded and non threaded bars

### Threaded horizontal bars

```python
from hprogressbars import *
import time # used only as example

progressbars = ProgressBars(num_bars=5)
progressbars.set_last_bar_as_total_progress(prefix="Total Progress: ")

# threaded bars using works. This functions represent works threaded
def work(progressbars, bar_index, work_value, work_name):
    progressbars.set_bar_prefix(bar_index=bar_index, prefix=work_name)
    for i in range(101):
             # your work here. we use the time.sleep() as example
             # Real work could be downloading a file and show progress
             time.sleep(work_value)
             progressbars.update(bar_index=bar_index, value=i)
    progressbars.finish()

# start all the threaded works
Work.start(work, (progressbars, 0, 0.1, "work1: "))
Work.start(work, (progressbars, 1, 0.01, "work2: "))
Work.start(work, (progressbars, 2, 0.2, "work3: "))
Work.start(work, (progressbars, 3, 0.05, "work4: "))      
    
```

### Using the same thread

```python
from hprogressbars import *
import time # used only as example

progressbars = ProgressBars(num_bars=5)
progressbars.set_last_bar_as_total_progress(prefix="Total Progress: ")

# using the same thread 
for i in range(101):
    # zero is assigned to start the value of the total progress
    time.sleep(0.1)
    values = [i, i+5, i+10, i+15, 0] 
    progressbars.update_all(values) # update bars in the same thread
progressbars.finish_all() # avoid memory leaks. 
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)