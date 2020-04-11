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
import time # required for demostration purposes only

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
import time # required for demostration purposes only

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
### Remove bars when job is done and init the next bar
```python
# clearing and initializing new progress bars:
from hprogressbars import *
import time # required for demostration purposes only

progressbars = ProgressBars(num_bars=3)
progressbars.set_last_bar_as_total_progress(prefix="Total Progress: ")
# hide the bars that are not being used at the moment
# multiple bars can be hidden at the same time
progressbars.set_hidden_bars([1]) 

# non threaded work 1 starts
for i in range(101):
    time.sleep(0.1)
    progressbars.update(bar_index=0, value=i)
progressbars.finish()
progressbars.clear_bar(bar_index=0) # clears the bar that was completed from screen
progressbars.reset_bar(index=1, prefix="new bar: ") # resets the new bar that will appear in screen 

# non threaded work 2 starts
for i in range(101):
    time.sleep(0.1)
    progressbars.update(bar_index=1, value=i)
progressbars.finish()

```
## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)