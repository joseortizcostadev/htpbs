"""
package:          hprogressbars
file:             progressbars.py
Author:           Jose Ortiz <jortizcocs@gmail.com>
Date Created:     04/09/2020
Last Modified:    04/10/2020
Licence:          MIT (see LICENSE.txt)

This script belongs to the hprogressbars package and is internally imported
by the file progressbars.py in the same package.

This scripts imports the following libraries:
sys
threading

It also import the following local files:
bar

"""

import sys
import threading

from bar import *


class ProgressBars:
    """
    This class is used to represent a wrapper for one or more progress bars.
    Progress bars created using this class will be presented in a horizontal fashion
    i.e: bar1 |******|  bar2 |***** | bar3 |******|  total: |***** |
    Bars created with this class are totally editable by the user using
    the methods described below
    """

    def __init__(self, num_bars=1, total_bar_index=-1, max_progress=100, separator="   "):
        """
        Class constructor
        :param num_bars:
            (optional) the num of bars to be show on screen in horizontal
        :param total_bar_index:
            (optional) the bar that will be used to show the total progress of all the bars together
        :param max_progress:
            (optional) the max progress allowed in all the bars.
            This can be edited later for each individual bar.
            It is highly recommended to keep the max_progress to the default value
        """
        self._num_bars = num_bars
        self._bars = []
        self._init_bars()
        self._total_bar_index = total_bar_index
        # internal boolean to determine if this method is active
        self._is_update_all = False
        self._bars_max = max_progress
        self._separator = separator
        self._total = 0

    def _init_bars(self):
        """
        Create and initialize all the bars.
        :return: VOID
        """
        for i in range(self._num_bars):
            bar = Bar()  # new bar
            bar.index = i  # sets the bar index
            self._bars.append(bar)

    def _get_percentages(self):
        """
        Gets the real time percentages of all the bars in progress
        :return: a list of percentages
        """
        percentages = []
        for bar in self._bars:
            if bar.index != self._total_bar_index:
                percentage = bar.percent
                # progresses come in string form, so they need some cleaning first
                percentage = percentage.replace("%", "").strip()
                percentage = float(percentage)  # cast to float
                percentages.append(percentage)
        return percentages

    def _get_total_value(self):
        """
        Gets the value of the bar representing the total progress of all the bars together
        :return: int representing the total progress
        """
        total = 0
        percentages = self._get_percentages()
        for i in range(len(percentages)):
            percentage = percentages[i]
            total += percentage
        return (total / len(percentages)) + 1  # + 1 to make it accurate and synchronized with all the bars

    def set_hidden_bars(self, indexes):
        """
        Define the bars that are not going to be show in screen.
        Note that progress in hidden bars still count in total progress
        :param indexes:
        :return:
        """
        for bar in self._bars:
            if bar.index in indexes:
                bar.hidden()

    def clear_bar(self, bar_index):
        self._bars[bar_index].hidden()
        self._clear()

    def set_total_bar(self, index, prefix="total"):
        """

        :param index:
        :param prefix:
        :return:
        """
        self._total_bar_index = index
        self._bars[index].prefix = prefix

    def set_max_bar_progress(self, bar_index, max_progress=100):
        """

        :param bar_index:
        :param max_progress:
        :return:
        """
        self._bars[bar_index].total = max_progress

    def set_bar_prefix(self, bar_index, prefix):
        """

        :param bar_index:
        :param prefix:
        :return:
        """
        self._bars[bar_index].prefix = prefix

    def set_bar_formatting(self, bar_index, formatting):
        """

        :param bar_index:
        :param formatting:
        :return:
        """
        self._bars[bar_index].formatting = formatting

    def set_bar_suffix(self, bar_index, suffix):
        """

        :param bar_index:
        :param suffix:
        :return:
        """
        self._bars[bar_index].suffix = suffix

    def set_bar_decimals(self, bar_index, decimals):
        """

        :param bar_index:
        :param decimals:
        :return:
        """
        self._bars[bar_index].decimals = decimals

    def set_bar_length(self, bar_index, length):
        """

        :param bar_index:
        :param length:
        :return:
        """
        self._bars[bar_index].length = length

    def set_bar_fill(self, bar_index, fill):
        """

        :param bar_index:
        :param fill:
        :return:
        """
        self._bars[bar_index].fill = fill

    def set_total_bar_index(self, bar_index):
        """

        :param bar_index:
        :return:
        """
        self._total_bar_index = bar_index

    def set_value(self, bar_index, value):
        """

        :param bar_index:
        :param value:
        :return:
        """
        self._bars[bar_index].set_value(value)

    def get_values(self):
        """

        :return:
        """
        values = []
        for bar in self._bars:
            values.append(bar.get_value())
        return values

    def reset_bar(self, index=0, max_progress=100, prefix='', formatting='', suffix='',
                  num_decimals=2, length=10, fill='█'):
        """

        :param index:
        :param max_progress:
        :param prefix:
        :param formatting:
        :param suffix:
        :param num_decimals:
        :param length:
        :param fill:
        :return:
        """
        bar = Bar(index, max_progress, prefix, formatting, suffix, num_decimals, length, fill)
        self._bars[index] = bar
        self._clear()

    def start(self, bar_index):
        """

        :param bar_index:
        :return:
        """
        bar = self._bars[bar_index].bar()
        print(bar)

    def start_all(self, separator="      "):
        """

        :param separator:
        :return:
        """
        multiple_bars = ""
        for bar in self._bars:
            if bar.is_visible():
                multiple_bars += (bar.bar() + separator)
        print(multiple_bars, end='\r')

    def is_progress_completed(self, bar_index):
        bar = self._bars[bar_index]
        if bar.is_progress_completed():
            return True
        return False

    def is_total_progress_completed(self):
        return self._total >= 100

    def update(self, bar_index, value):
        """

        :param bar_index:
        :param value:
        :return:
        """
        self._bars[bar_index].update(value)
        if self._total_bar_index > -1:
            self._total = self._get_total_value()  # self._get_total_value()
            self._bars[self._total_bar_index].update(self._total)
        # self.finish_work()
        self.start_all()

    def finish_work(self):
        """

        :return:
        """
        percentages = self._get_percentages()
        sum_percentages = sum(percentages)
        len_percentages = len(percentages)
        if (sum_percentages / len_percentages) >= 100:
            self._down()

    def update_all(self, values):
        """
        :param values:
        :return:
        """
        self._is_update_all = True
        if values:
            for i in range(len(self._bars)):
                value = values[i]
                if self._total_bar_index == i:
                    total_value = self._get_total_value()  # self._get_total_value()
                    value = total_value
                self._bars[i].update(value)
        self.start_all()

    def update_total(self):
        """

        :return:
        """
        self.update(self._total_bar_index, 0)

    def finish(self):
        """

        :return:
        """
        if self._total >= 100:
            self.finish_all()

    def finish_all(self):
        self._down()

    def show_bars(self, indexes):
        """

        :param indexes: a list of indexes of the bars that will be show on screen
        :return:
        """
        pass

    def is_work_finished(self):
        percentages = self._get_percentages()
        if sum(percentages) / len(percentages) == 100:
            return True
        return False

    def set_last_bar_as_total_progress(self, prefix="Total Progress: "):
        """

        :return: VOID
        """
        last_bar = self._num_bars - 1
        self.set_total_bar(last_bar, prefix)

    def set_first_bar_as_total_progress(self, prefix="Total Progress: "):
        """

        :return: VOID
        """
        first_bar = 0
        self.set_total_bar(first_bar, prefix)

    def _up(self, level=1):
        """
        Move up one line and put the cursor at the beginning of the line.
        My terminal breaks if we don't flush after the escape-code
        :param level:
        :return: VOID
        """
        for i in range(level):
            sys.stdout.write('\x1b[1A')
            sys.stdout.flush()

    def _down(self, level=1):
        """
        Move down one line and put the cursor at the beginning of the line
        :param level:
        :return: VOID
        """
        for i in range(level):
            sys.stdout.write('\n')
            sys.stdout.flush()

    def _clear(self):
        sys.stdout.write("\033[K")  # clear line


class Work:
    """
    Static class that thread a work in order to run threaded progress bars.
    Call this method directly using Work.start(...)
    """

    @staticmethod
    def start(func, parameters, daemon=False):
        """
        Static method Starts a work
        :param func: the name of the function that contains the work
        :param parameters: a tuple containing all the parameters of the function
        :param daemon: when True it waits until the main program finishes.
        :return: VOID
        """
        thread = threading.Thread(target=func, args=parameters, daemon=daemon)
        thread.start()
        if daemon:
            thread.join()


# from hprogressbars import *
import time  # used only as example

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
    progressbars.finish() # finishes bar threaded


Work.start(work, (progressbars, 0, 0.1, "work1: "))
Work.start(work, (progressbars, 1, 0.01, "work2: "))
Work.start(work, (progressbars, 2, 0.2, "work3: "))
Work.start(work, (progressbars, 3, 0.05, "work4: "))


# using the same thread
for i in range(101):
    # zero is assigned to start the value of the total progress
    time.sleep(0.1)
    values = [i, i+5, i + 10, i + 15, 0]
    progressbars.update_all(values)  # update bars in the same thread
progressbars.finish_all()  # avoid memory leaks.
