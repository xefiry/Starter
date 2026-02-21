# Starter

An executable starter/stopper written in python. Uses a toml configuration file.

## Arguments

```plain
usage: main.py [-h] [-v] [-d] [-s N] [config_file]

positional arguments:
  config_file    config file to use (default: config.toml)

options:
  -h, --help     show this help message and exit
  -v, --verbose  verbose mode
  -d, --dry_run  dry run (nothing done, only printing)
  -s, --sleep N  sleep for N seconds at the end
```

## Configuration

Configuration is read from a toml file (by default config.toml).

It contains a list of entries describing the executable to start/stop.

If an executable is already running, it will not be started unless threshold is set.

Here are a few examples.

```toml
# StartOne entry with the minimum parameters required
[[entry]]
type = "StartOne"
exe = "program.exe"

# StartMany entry with the minimum parameters required
# if args is an empty list (args = []) it will do nothing
# here it will star once
[[entry]]
type = "StartMany"
exe = "program.exe"
args  = [[]]

# You can start the executable multiple times without arguments
# here, it will start twice
[[entry]]
type = "StartMany"
exe = "program.exe"
args  = [[], []]

# Stop entry with the minimum parameters required
[[entry]]
type = "Stop"
exe = "program.exe"

# StartOne entry with all the available parameters
[[entry]]
type = "StartOne"
exe = "program.exe",
path = "%var%/directory"
args = ["args"]
cwd = "%var%/directory"
threshold = 2
wait_before = 1.2
wait_after = 2.8

# StartMany entry with all the available parameters
[[entry]]
type = "StartMany"
exe = "program.exe"
path = "/some/path"
args = [["argA1", "argA2"], ["argB1", "argB2"], "argC1"]
cwd = "%var%/directory"
threshold = 2
wait_before = 1.2
wait_after = 2.8

# Stop entry with all the available parameters
[[entry]]
type = "Stop"
exe = "program.exe"
wait_before = 1.2
wait_after = 2.8
```

### type

string, mandatory

The type of entry : StartOne, StartMany or Stop

- StartOne : execute a program with arguments (if given)
- StartMany : execute a program multiple times with a list of arguments
- Stop : stop the executable (sends SIGTERM) to all instances of the executable

### exe

string, mandatory

The executable to start/stop. Do not include the path to the executable, otherwise the search for running executable will fail.

### path

string, optionnal

The path for the executable. Environment variables are managed (example: %AppData% for Windows).

### args

str or list, optionnal for StartOne, mandatory for StartMany, unused for Stop

The list of arguments to use.

#### For StartOne

An argument (str) or a list of arguments to use with the executable.

Example :

- "arg" will execute `program.exe "arg"`
- ["arg1", "arg2"] will execute `program.exe "arg1" "arg2"`

#### For StartMany

A list of list of arguments.

Examples :

- ["arg"] will execute `program.exe "arg"`
- ["argA1", "argB1"] will execute `program.exe "argA1"`, then `program.exe "argB1"`
- [["argA1", "argA2"], ["argB1"], "argC1"] will execute `program.exe "argA1" "argA2"`, then `program.exe "argB1"`, then `program.exe "argC1"`

### cwd

str, optionnal, unused for Stop

Set the curent working directory. Environment variables are managed (example: %AppData% for Windows).

If not set, the value of path will be used.

### threshold

int, optional, unused for Stop

Before starting an executable, the program checks if it is already running. By default, if at least one instance is found, the executable will not be started.

If you put n, it allows to run the executable even if up to n instances of it are already running.

Example : if set to 2, it will start the execuable even if it is running 2 times, but not if it is already running 3 or more times.

### wait_before

float, optionnal

How much time, in seconds, wait before running/stopping the executable

### wait_after

float, optionnal

How much time, in seconds, wait after running/stopping the executable
