# Starter

An executable starter/stopper written in python.

## Configuration

Configuration is done in config.toml. It contains a list of entries describing the executable to start/stop.

Here is a skeleton of an entry with all the available parameters.

See example_config.toml for some examples.

```toml
[[entry]]
type = "StartOne"
exe = "program.exe",
path = "%var%/directory"
args = ["args"]
cwd = "%var%/directory"
threshold = 2
wait_before = 1.2
wait_after = 2.8

[[entry]]
type = "StartMany"
exe = "program.exe"
path = "/some/path"
args = [["argA1", "argA2"], ["argB1", "argB2"]]
cwd = "%var%/directory"
threshold = 2
wait_before = 1.2
wait_after = 2.8

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

The path for the executable. Environment variables are managed (example: %AppData% for Windows)

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

Set the curent working directory.

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
