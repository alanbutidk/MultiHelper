from Helper import Task, GUI, prefix
from Helper import ArgumentNotGivenError, PrefixFunctionMismatchError, WrongArgumentError

print("=" * 50)
print("Helper.py Test File")
print("=" * 50)

# ── Task.wait ─────────────────────────────────────────────────────────────────
print("\n[1] Task.wait(2) - waiting 2 seconds...")
Task.wait(2)
print("Done waiting.")

# ── Task.FileExists ───────────────────────────────────────────────────────────
print("\n[2] Task.FileExists() - checking for test_Helper.py (exists) and ghost.txt (doesnt exist)...")
Task.FileExists("test_Helper.py")
print(f"SuccessFileExistsCode: {Task.SuccessFileExistsCode}")
Task.FileExists("ghost.txt")
print(f"SuccessFileExistsCode: {Task.SuccessFileExistsCode}")

# ── Task.WriteToFile ──────────────────────────────────────────────────────────
print("\n[3] Task.WriteToFile() - writing to test_output.txt...")
Task.WriteToFile("test_output.txt", data="Hello from WriteToFile")
Task.WriteToFile("test_output.txt", data="Second line appended")
print("Done writing.")

# ── Task.ReadFromFile ─────────────────────────────────────────────────────────
print("\n[4] Task.ReadFromFile() - reading test_output.txt...")
content = Task.ReadFromFile("test_output.txt")
print(f"File contents:\n{content}")

print("\n[4b] Task.ReadFromFile() - reading a file that doesnt exist...")
result = Task.ReadFromFile("doesntexist.txt")
print(f"Returned: '{result}'")

# ── Task.OverWriteToFile ──────────────────────────────────────────────────────
print("\n[5] Task.OverWriteToFile() - overwriting test_output.txt...")
Task.OverWriteToFile("test_output.txt", data="This overwrote the file")
content = Task.ReadFromFile("test_output.txt")
print(f"File contents after overwrite:\n{content}")

# ── Task.CheckArg ─────────────────────────────────────────────────────────────
print("\n[6] Task.CheckArg() - checking for argument 'hello'...")
Task.CheckArg("hello")

print("\n[6b] Task.CheckArg() - with tell=True...")
Task.CheckArg("hello", tell=True)

# ── prefix - basic ────────────────────────────────────────────────────────────
print("\n[7] prefix('os') - injecting os functions into globals...")
prefix("os")
result = getcwd()
print(f"getcwd() without os. prefix: {result}")

print("\n[7b] prefix('os') - calling listdir() without os. prefix...")
files = listdir(".")
print(f"listdir('.') returned {len(files)} items")

# ── prefix - WrongArgumentError ───────────────────────────────────────────────
print("\n[8] prefix WrongArgumentError - this should catch wrong type/count...")
prefix("os.path")
try:
    result = join(123, 456)
except WrongArgumentError as e:
    print(f"WrongArgumentError caught: {e}")
except TypeError as e:
    print(f"TypeError caught (function not annotated, no WrongArgumentError): {e}")

# ── prefix - PrefixFunctionMismatchError ──────────────────────────────────────
print("\n[9] PrefixFunctionMismatchError - defining sleep() then prefixing time...")

def sleep(n):
    print("This is the user defined sleep, not time.sleep")

prefix("time")

print("Calling sleep() - should raise PrefixFunctionMismatchError...")
try:
    sleep(1)
except PrefixFunctionMismatchError as e:
    print(f"PrefixFunctionMismatchError caught: {e}")
except SystemExit as e:
    print(f"SystemExit caught after mismatch: {e}")

# ── Task.ExitWithoutDynamicErrors ─────────────────────────────────────────────
print("\n[10] Task.ExitWithoutDynamicErrors() - verbose=False first...")
try:
    Task.ExitWithoutDynamicErrors("Clean exit test", verbose=False)
except SystemExit as e:
    print(f"SystemExit caught: {e}")

print("\n[10b] Task.ExitWithoutDynamicErrors() - verbose=True...")
try:
    Task.ExitWithoutDynamicErrors("Verbose exit test", verbose=True)
except SystemExit as e:
    print(f"SystemExit caught: {e}")

# ── GUI.Tkinter ───────────────────────────────────────────────────────────────
print("\n[11] GUI.Tkinter - launching a test window...")
print("A window will open. Close it to continue the test.")

def on_click():
    print("Button was clicked!")

GUI.Tkinter.WindowInit("Helper Test Window", 400, 300)
GUI.Tkinter.Label("Hello from Helper!", 100, 50)
GUI.Tkinter.Button("Click Me", 100, 120, on_click)
inp = GUI.Tkinter.Input(100, 180)
GUI.Tkinter.Gravity("center")
GUI.Tkinter.Run()

print("Tkinter window closed, continuing...")

# ── GUI.Kivy ──────────────────────────────────────────────────────────────────
print("\n[12] GUI.Kivy - launching a test window...")
print("A Kivy window will open. Close it to finish the test.")

def on_kivy_click():
    print("Kivy button was clicked!")

try:
    GUI.Kivy.WindowInit("Helper Kivy Test", 400, 300)
    GUI.Kivy.Label("Hello from Kivy!", 100, 200)
    GUI.Kivy.Button("Click Me", 100, 120, on_kivy_click)
    GUI.Kivy.Input(100, 60)
    GUI.Kivy.Run()
    print("Kivy window closed.")
except SystemExit as e:
    print(f"Kivy not installed, skipped: {e}")

# ── Done ──────────────────────────────────────────────────────────────────────
print("\n" + "=" * 50)
print("All tests completed.")
print("=" * 50)