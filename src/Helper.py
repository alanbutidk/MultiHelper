import time
import sys
import os
import inspect
import importlib

# ── Exceptions ———————

class ArgumentNotGivenError(Exception):
    pass

class PrefixFunctionMismatchError(Exception):
    pass

class WrongArgumentError(Exception):
    pass

# ── Task ──────────────────────────────────────────────────────────────────────

class Task:
    SuccessFileExistsCode = 0
    OSErrorCode = 0

    @staticmethod
    def wait(n):
        time.sleep(n)

    @staticmethod
    def FileExists(filename):
        try:
            if os.path.exists(filename):
                Task.SuccessFileExistsCode = 1
                print("File Exists")
            else:
                Task.SuccessFileExistsCode = 0
        except OSError:
            Task.OSErrorCode = 1
            print("OSERROR")

    @staticmethod
    def ReadFromFile(filename):
        try:
            with open(filename, "r") as f:
                return f.read()
        except FileNotFoundError:
            print("File not found")
            return ""

    @staticmethod
    def WriteToFile(filename, **kwargs):
        try:
            with open(filename, "a") as f:
                if kwargs:
                    data = next(iter(kwargs.values()))
                    f.write(str(data) + "\n")
        except OSError:
            print("OSERROR")
            Task.OSErrorCode = 1

    @staticmethod
    def OverWriteToFile(filename, **kwargs):
        try:
            with open(filename, "w") as f:
                if kwargs:
                    data = next(iter(kwargs.values()))
                    f.write(str(data) + "\n")
        except OSError:
            print("OSERROR")
            Task.OSErrorCode = 1

    @staticmethod
    def CheckArg(string, tell=False):
        try:
            if tell:
                print("\nTell is checked on")
                print("\nArguments are:")
                for i, arg in enumerate(sys.argv[1:]):
                    if arg != string:
                        print("\nArgument doesnt match")
                        break
                    print(f"\nArg {i}: {arg}")
            elif string:
                if string in sys.argv[1:]:
                    print(f"\nArgument has string given {string}")
                else:
                    print(f"\nArgument doesnt have string {string} given as a argument")
            else:
                sys.exit(1)
        except OSError:
            pass

    @staticmethod
    def ExitWithoutDynamicErrors(str, verbose=False):
        try:
            if verbose:
                print("\nExitWithoutDynamicErrors.verbose is turned on.")
                print("\nStarting Exit Process via SystemExit")
            raise SystemExit(str)
        except SystemError:
            print("SystemError was recorded, indicating Python is bugging, immediate EXIT is called!")
            sys.exit(1)

# ── Prefix ────────────────────────────────────────────────────────────────────

def prefix(module_name: str):
    caller_frame = inspect.stack()[1]
    caller_globals = caller_frame[0].f_globals

    try:
        module = importlib.import_module(module_name)
    except ImportError:
        raise ImportError(f"prefix(): module '{module_name}' could not be imported.")

    module_functions = {
        name: obj
        for name, obj in inspect.getmembers(module, inspect.isbuiltin)
    }
    module_functions.update({
        name: obj
        for name, obj in inspect.getmembers(module, inspect.isfunction)
    })

    collisions = {}
    for name, func in module_functions.items():
        if name in caller_globals and callable(caller_globals[name]) and caller_globals[name] is not func:
            collisions[name] = (func, caller_globals[name])

    def make_collision_wrapper(lib_func, user_func, func_name, all_collisions):
        def wrapper(*args, **kwargs):
            collision_report = "\n".join(
                f"  '{n}': library function '{lib.__module__}.{n}' collides with user-defined '{usr.__qualname__}'"
                for n, (lib, usr) in all_collisions.items()
            )
            print(f"PrefixFunctionMismatchError: name collision(s) detected when calling '{func_name}':")
            print(collision_report)
            raise PrefixFunctionMismatchError(
                f"Function name '{func_name}' collides between prefixed module and user definition."
            )
        return wrapper

    def make_type_checked_wrapper(lib_func, func_name, sig):
        hints = {}
        for pname, param in sig.parameters.items():
            if param.annotation is not inspect.Parameter.empty:
                hints[pname] = param.annotation

        def wrapper(*args, **kwargs):
            try:
                bound = sig.bind(*args, **kwargs)
            except TypeError as e:
                print(f"WrongArgumentError: wrong number of arguments for '{func_name}'.")
                print(f"  Expected: {sig}")
                print(f"  Got:      {len(args)} positional, {len(kwargs)} keyword")
                raise WrongArgumentError(str(e))

            bound.apply_defaults()
            for pname, value in bound.arguments.items():
                if pname in hints:
                    expected_type = hints[pname]
                    if not isinstance(value, expected_type):
                        print(f"WrongArgumentError: wrong type for argument '{pname}' in '{func_name}'.")
                        print(f"  Expected: {expected_type.__name__}")
                        print(f"  Got:      {type(value).__name__} ({repr(value)})")
                        raise WrongArgumentError(
                            f"Argument '{pname}' expected {expected_type.__name__}, got {type(value).__name__}."
                        )

            return lib_func(*args, **kwargs)
        return wrapper

    for name, func in module_functions.items():
        if name in collisions:
            caller_globals[name] = make_collision_wrapper(func, collisions[name][1], name, collisions)
        else:
            try:
                sig = inspect.signature(func) if callable(func) else None
            except (ValueError, TypeError):
                caller_globals[name] = func
                continue

            has_annotations = bool(sig and any(
                p.annotation is not inspect.Parameter.empty
                for p in sig.parameters.values()
            ))

            if has_annotations:
                caller_globals[name] = make_type_checked_wrapper(func, name, sig)
            else:
                caller_globals[name] = func

# ── GUI ───────────────────────────────────────────────────────────────────────

class _TkinterGUI:
    _root = None
    _widgets = []

    @staticmethod
    def WindowInit(title: str, width: int, height: int):
        try:
            import tkinter as tk
            _TkinterGUI._root = tk.Tk()
            _TkinterGUI._root.title(title)
            _TkinterGUI._root.geometry(f"{width}x{height}")
        except ImportError:
            print("tkinter is not available in your Python installation.")
            sys.exit(1)

    @staticmethod
    def Button(text: str, x: int, y: int, command=None):
        if _TkinterGUI._root is None:
            print("GUI.Tkinter.WindowInit() must be called before adding widgets.")
            sys.exit(1)
        import tkinter as tk
        btn = tk.Button(_TkinterGUI._root, text=text, command=command)
        btn.place(x=x, y=y)
        _TkinterGUI._widgets.append(btn)
        return btn

    @staticmethod
    def Label(text: str, x: int, y: int):
        if _TkinterGUI._root is None:
            print("GUI.Tkinter.WindowInit() must be called before adding widgets.")
            sys.exit(1)
        import tkinter as tk
        lbl = tk.Label(_TkinterGUI._root, text=text)
        lbl.place(x=x, y=y)
        _TkinterGUI._widgets.append(lbl)
        return lbl

    @staticmethod
    def Input(x: int, y: int):
        if _TkinterGUI._root is None:
            print("GUI.Tkinter.WindowInit() must be called before adding widgets.")
            sys.exit(1)
        import tkinter as tk
        entry = tk.Entry(_TkinterGUI._root)
        entry.place(x=x, y=y)
        _TkinterGUI._widgets.append(entry)
        return entry

    @staticmethod
    def Gravity(direction: str):
        if _TkinterGUI._root is None:
            print("GUI.Tkinter.WindowInit() must be called before adding widgets.")
            sys.exit(1)
        if not _TkinterGUI._widgets:
            print("GUI.Tkinter.Gravity(): no widgets have been added yet.")
            return
        import tkinter as tk
        gravity_map = {
            "center": tk.CENTER,
            "top":    tk.N,
            "bottom": tk.S,
            "left":   tk.W,
            "right":  tk.E,
        }
        anchor = gravity_map.get(direction.lower())
        if anchor is None:
            print(f"GUI.Tkinter.Gravity(): unknown direction '{direction}'. Use: center, top, bottom, left, right.")
            return
        last = _TkinterGUI._widgets[-1]
        last.place_configure(anchor=anchor)

    @staticmethod
    def Run():
        if _TkinterGUI._root is None:
            print("GUI.Tkinter.WindowInit() must be called before Run().")
            sys.exit(1)
        _TkinterGUI._root.mainloop()
        _TkinterGUI._root = None
        _TkinterGUI._widgets.clear()


class _KivyGUI:

    @staticmethod
    def WindowInit(title: str, width: int, height: int):
        try:
            from kivy.uix.floatlayout import FloatLayout
            from kivy.core.window import Window
            Window.size = (width, height)
            _KivyGUI._layout = FloatLayout()
            _KivyGUI._title = title
        except ImportError:
            print("Kivy is not installed. Install it with: pip install kivy")
            sys.exit(1)

    @staticmethod
    def Button(text: str, x: int, y: int, command=None):
        if not hasattr(_KivyGUI, '_layout'):
            print("GUI.Kivy.WindowInit() must be called before adding widgets.")
            sys.exit(1)
        from kivy.uix.button import Button as KvButton
        btn = KvButton(text=text, size_hint=(None, None), size=(200, 50), pos=(x, y))
        if command:
            btn.bind(on_press=lambda instance: command())
        _KivyGUI._layout.add_widget(btn)
        return btn

    @staticmethod
    def Label(text: str, x: int, y: int):
        if not hasattr(_KivyGUI, '_layout'):
            print("GUI.Kivy.WindowInit() must be called before adding widgets.")
            sys.exit(1)
        from kivy.uix.label import Label as KvLabel
        lbl = KvLabel(text=text, size_hint=(None, None), size=(200, 50), pos=(x, y))
        _KivyGUI._layout.add_widget(lbl)
        return lbl

    @staticmethod
    def Input(x: int, y: int):
        if not hasattr(_KivyGUI, '_layout'):
            print("GUI.Kivy.WindowInit() must be called before adding widgets.")
            sys.exit(1)
        from kivy.uix.textinput import TextInput
        inp = TextInput(size_hint=(None, None), size=(200, 50), pos=(x, y))
        _KivyGUI._layout.add_widget(inp)
        return inp

    @staticmethod
    def Run():
        if not hasattr(_KivyGUI, '_layout'):
            print("GUI.Kivy.WindowInit() must be called before Run().")
            sys.exit(1)
        from kivy.app import App
        layout = _KivyGUI._layout
        title = _KivyGUI._title

        class _HelperApp(App):
            def build(self):
                self.title = title
                return layout

        _HelperApp().run()
        del _KivyGUI._layout
        del _KivyGUI._title


class GUI:
    Tkinter = _TkinterGUI
    Kivy = _KivyGUI