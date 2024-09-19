# tictactoc

A simple library to be able to control the time that certain parts of the code take

## Installation and use

To install this module use:

```sh
pip install tictactoc
```

Run tests to validate:

```sh
tictactoc-tests
```

## Usage

```py
from time import sleep
from tictactoc import tictactoc
from tictactoc import plot


# Basic use, start and end.
tictactoc.tic() # Start
print(tictactoc.toc()) # Finish

# Using tac in loops.
# We can do a tac in each iteration. When we finnish the loop, we do a toc skipping this time.

my_loop=["element1","element2","element3"]
tictactoc.tic("my loop")

for element in my_loop:
    sleep(0.1)
    tictactoc.tac("my loop")

result = tictactoc.toc("my loop", skip_toc=True)
print(f"total: {result["total"]}, each iteration: {', '.join(map(str,result["steps"]))}")
```

```plain
{'name': '__default', 'total': 1.8840000848285854e-06, 'steps': [1.8840000848285854e-06]}
total: 2.2079411439999603, each iteration: 0.5419861169993965, 0.5843896450005559, 0.3017711920001602, 0.4091919909997159, 0.3706021990001318
```

```py
# Print a plot.
# We can use the return value of toc for draw a plot.

plot.print(result)
```

```plain
========================================
my loop
--------------------
 0 | ##################     0.54
 1 | #################### ! 0.58
 2 | ##########             0.30
 3 | ##############         0.41
 4 | ############           0.37
--------------------
quantile value: 0.5504668225996283
========================================
```

## Credits

Developed and maintained by felipem775. [Contributions](CONTRIBUTING.md) are welcomed.
