```
# PLEGUI (Python Library for Easy GUI Development)

`plegui` is a Python library that simplifies the creation and management of graphical user interfaces (GUIs) using `tkinter`. The library also provides utility functions for working with system processes, hiding command prompts, and more.

## Installation

To install the library, use pip:

```bash
pip install plegui
```

## Features

- Create and manage multiple GUI windows
- Add buttons, labels, text entries, and dropdown menus
- Hide or show the command prompt window
- Utility functions for working with processes
- Message box display support

## Getting Started

To get started, import the library and create your first window using the `GUI` class.

```
from plegui import GUI, messagebox, system
```


# Create a window with a specific title and resolution
GUI.create("My First Window", width=500, height=400)

# Add a button to the window
GUI.add_button("My First Window", "Click Me", lambda: print("Button clicked!"))

# Add a text entry field
entry = GUI.add_entry("My First Window")

# Add a dropdown menu
dropdown = GUI.add_dropdown("My First Window", ["Option 1", "Option 2", "Option 3"])

# Display a messagebox
messagebox.form("Hello, this is a message box!")

# Set the window title to a new value
GUI.set_title("My First Window", "New Title")

# Hide the command prompt window
GUI.set_cmd_hidden(True)

# Close the window
GUI.close_window("My First Window")
```

### Creating Windows

To create a new window, use the `GUI.create` method. You can specify a custom width, height, and codename for the window.

```python
GUI.create("Window Name", width=500, height=400)
```

### Adding Widgets

#### Buttons

To add a button to a window, use the `GUI.add_button` method. You can specify the window name, button text, and an optional command that will execute when the button is clicked.

```python
GUI.add_button("Window Name", "Click Me", lambda: print("Button clicked!"))
```

#### Text Entry

To add a text entry field, use the `GUI.add_entry` method. This will return the `Entry` widget, allowing you to interact with the input.

```python
entry = GUI.add_entry("Window Name")
```

#### Dropdown Menu

To add a dropdown menu, use the `GUI.add_dropdown` method. You can specify a list of options, and the method will return the selected option.

```python
dropdown = GUI.add_dropdown("Window Name", ["Option 1", "Option 2", "Option 3"])
```

#### Labels

You can also add a label to display text using the `GUI.label.create` method.

```python
GUI.label.create("Window Name", "This is a label")
```

### Window Management

#### Set Window Title

To update the title of a window, use the `GUI.set_title` method.

```python
GUI.set_title("Window Name", "New Title")
```

#### Close a Window

To close a window, use the `GUI.close_window` method.

```python
GUI.close_window("Window Name")
```

### System Utilities

#### Hiding the Command Prompt

You can hide or show the command prompt using the `GUI.set_cmd_hidden` method. 

```python
# Hide the command prompt
GUI.set_cmd_hidden(True)

# Show the command prompt
GUI.set_cmd_hidden(False)
```

#### Process Management

The `system.process_add` method allows you to modify the process name.

```python
# Rename the process to "main.py"
system.process_add(True)

# Restore the original process name
system.process_add(False)
```

### Message Boxes

To display a message box, use the `messagebox.form` method.

```python
messagebox.form("This is a message!")
```

## License

`plegui` is released under the MIT License.
```