# generate_joblib_pred_gui
# Command Line Tool GUI for Joblib Model Predictions

This Python-based GUI tool allows users to run a command-line script that generates predictions from a trained model saved in `.joblib` format. The user inputs features and constants, specifies the output file, and runs the prediction script via a simple GUI interface.

## Features

- **User-friendly GUI**: Built using `tkinter` to make running a Python prediction script easy without needing to use the command line.
- **Dynamic Input Rows**: Users can specify the number of feature/constant rows, and the corresponding input fields are created automatically.
- **Argument Parsing**: The tool collects user input, formats it into the correct command-line arguments, and runs the prediction script.
- **Help**: Provides help information for using the tool.

## Requirements

- Python 3.x
- `tkinter` (usually comes with Python)
- `joblib` (for loading model files)
- Ensure you have a `.joblib` model file for predictions

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/Rouschop/generate_joblib_pred_gui
   cd generate_joblib_pred_gui
   python 3_gui.py


<p xmlns:cc="http://creativecommons.org/ns#" xmlns:dct="http://purl.org/dc/terms/"><a property="dct:title" rel="cc:attributionURL" href="https://github.com/Rouschop/generate_joblib_pred_gui">generate_joblib_pred_gui</a> by <a rel="cc:attributionURL dct:creator" property="cc:attributionName" href="https://github.com/Rouschop">Jordy Rouschop</a> is licensed under <a href="https://creativecommons.org/licenses/by-nc-sa/4.0/?ref=chooser-v1" target="_blank" rel="license noopener noreferrer" style="display:inline-block;">CC BY-NC-SA 4.0<img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/cc.svg?ref=chooser-v1" alt=""><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/by.svg?ref=chooser-v1" alt=""><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/nc.svg?ref=chooser-v1" alt=""><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/sa.svg?ref=chooser-v1" alt=""></a></p> 
