TkShadowfy is a Python library for adding shadow effects to Tkinter widgets. It provides an easy way to add dynamic shadows that respond to hover and click events.

## Installation

You can install TkShadowfy using pip:

```
pip install tkshadowfy
```

## Usage

Here's a simple example of how to use TkShadowfy:

```python
import tkinter as tk
from tkshadowfy import Shadow

root = tk.Tk()
label = tk.Label(root, text="Hello, World!")
label.pack(pady=20)

shadow = Shadow(label, color='#000000', size=5, offset_x=2, offset_y=2, opacity=0.3)

root.mainloop()
```

For more examples and detailed usage instructions, please refer to the documentation.

## Author

- [Documentation](https://tkshadowfy.nakxa.site)
- [PyPI Package](https://pypi.org/project/tkshadowfy)
- [LinkedIn](https://www.linkedin.com/in/nakxa)


## License

This project is licensed under the MIT License - see the LICENSE file for details.
