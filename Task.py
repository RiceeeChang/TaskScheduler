# --------------------------------------------------------
#
# Task - a class of task that is in long term queue.
#        multi-type task
#        1. first enter queue
#        2. build automata
#        3. generate trace
#        4. run trace
#
# --------------------------------------------------------
from functools import total_ordering

@total_ordering
class Task(object):
    def __init__(self, task_type = 'task', user = 'user', app_name = 'app_name', 
        app_package = 'package', app_arugment = 'arugment', algorithm = 'algorithm'):
        self.task_type = task_type
        self.user = user
        self.app_name = app_name
        self.app_package = self.app_package
        self.app_arugment = app_arugment
        self.algorithm = algorithm
        self.priority = 1


    def __lt__(self, other):
        return self.priority < other.priority

    def __eq__(self, other):
        return self.priority == other.priority

if __name__ == '__main__':
