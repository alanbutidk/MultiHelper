# multihelper

Multi-Function Helper for GUI, basic file functions, argument checks, and the advanced `prefix()` feature.

## Installation

```
pip install multihelper
```

For Kivy GUI support:
```
pip install multihelper[kivy]
```

## Usage

```python
from multihelper import Task, GUI, prefix
from multihelper import ArgumentNotGivenError, PrefixFunctionMismatchError, WrongArgumentError
```

---

## Task

Basic file and utility functions.

```python
Task.wait(2)                                      # sleep 2 seconds
Task.FileExists("file.txt")                       # prints result, sets Task.SuccessFileExistsCode
Task.ReadFromFile("file.txt")                     # returns file contents as string
Task.WriteToFile("file.txt", data="hello")        # appends to file
Task.OverWriteToFile("file.txt", data="hello")    # overwrites file
Task.CheckArg("--run")                            # checks sys.argv for string
Task.CheckArg("--run", tell=True)                 # verbose argument listing
Task.ExitWithoutDynamicErrors("bye")              # clean SystemExit
Task.ExitWithoutDynamicErrors("bye", verbose=True)
```

---

## prefix()

Injects all functions from a module into the calling file's global namespace, removing the need for the module prefix.

```python
prefix("os")
cwd = getcwd()      # instead of os.getcwd()
files = listdir(".") # instead of os.listdir(".")
```

### WrongArgumentError
Raised when a type-annotated prefixed function receives the wrong type or wrong number of arguments.
```
WrongArgumentError: wrong type for argument 'n' in 'sleep'.
  Expected: int
  Got:      str ('hello')
```

### PrefixFunctionMismatchError
Raised lazily when a prefixed function name collides with a user-defined function in the same file. Raised on call, prints all collisions, then SystemExit.
```python
def sleep(n):       # collides with time.sleep after prefix("time")
    pass

prefix("time")
sleep(1)            # raises PrefixFunctionMismatchError here
```

---

## GUI

### GUI.Tkinter

```python
from multihelper import GUI

def on_click():
    print("clicked!")

GUI.Tkinter.WindowInit("My App", 800, 600)
GUI.Tkinter.Label("Hello!", 100, 50)
GUI.Tkinter.Button("Click Me", 100, 120, on_click)
inp = GUI.Tkinter.Input(100, 180)
GUI.Tkinter.Gravity("center")
GUI.Tkinter.Run()
```

No `.pack()`, `.grid()`, `.place()`, or `.mainloop()` ever written manually.

**Gravity directions:** `center`, `top`, `bottom`, `left`, `right`

### GUI.Kivy

Requires `pip install multihelper[kivy]`

```python
GUI.Kivy.WindowInit("My App", 800, 600)
GUI.Kivy.Label("Hello!", 100, 200)
GUI.Kivy.Button("Click Me", 100, 120, on_click)
GUI.Kivy.Input(100, 60)
GUI.Kivy.Run()
```

---

## Exceptions

| Exception | When |
|---|---|
| `ArgumentNotGivenError` | Raise manually when a required argument is missing |
| `PrefixFunctionMismatchError` | Name collision between prefixed module function and user-defined function |
| `WrongArgumentError` | Wrong type or count passed to a type-annotated prefixed function |

---

## License

GPLv3 - Copyright (C) 2026 Alan

__LICENSE in the SOURCE CODE!__