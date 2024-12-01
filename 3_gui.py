import tkinter as tk
from tkinter import messagebox, simpledialog
import subprocess
import os

def run_command():
    args = []
    
    for i in range(number_f_or_c):
        feature_or_constant = feature_or_constant_vars[i].get()
        value = value_entries[i].get().strip()
        
        if value:
            if feature_or_constant == 'feature':
                args.append(f"--feature {value}")
            elif feature_or_constant == 'constant':
                args.append(f"--constant {value}")
    
    output_file = output_entry.get().strip()
    if output_file:
        args.append(f"--o {output_file}")
    else:
        messagebox.showerror("Error", "Output file must be specified!")
        return

    model_file = model_entry.get().strip()
    if model_file:
        args.append(f"--model {model_file}")
    
    command = f"python {os.path.join(script_dir, 'scripts/3_gen_pred_pool.py')} " + " ".join(args)
    print("Running command:", command)

    try:
        subprocess.run(command, shell=True, check=True)
        messagebox.showinfo("Success", "Command executed successfully!")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"Error executing command: {e}")

def show_help():
    help_message = (
        "Example Format:\n\n"
        "--feature feature1=1,5,1\n"
        "--constant constant1=55\n\n"
        "You can leave fields empty, and the application will ignore them. "
        "For each row, select either 'feature' or 'constant' and then enter a value.\n\n"
        "Defaults:\n"
        "--o output.csv\n"
        "--model model.joblib"
    )
    messagebox.showinfo("Help", help_message)

number_f_or_c = simpledialog.askinteger("Input", "Enter the number of features/constants:", minvalue=1, maxvalue=20)

if number_f_or_c is None:
    print("No valid number entered. Exiting.")
    exit()

root = tk.Tk()
root.title("Command Line Tool GUI")
root.geometry("500x750")

script_dir = os.path.dirname(os.path.realpath(__file__))

feature_or_constant_vars = []
value_entries = []

for i in range(number_f_or_c):
    row_label = tk.Label(root, text=f"Row {i+1}:")
    row_label.grid(row=i, column=0, padx=10, pady=5, sticky="w")
    
    var = tk.StringVar(value="feature")
    feature_or_constant_vars.append(var)
    dropdown = tk.OptionMenu(root, var, "feature", "constant")
    dropdown.grid(row=i, column=1, padx=10, pady=5)
    
    entry = tk.Entry(root)
    value_entries.append(entry)
    entry.grid(row=i, column=2, padx=10, pady=5)

output_label = tk.Label(root, text="Output file (e.g., output.csv):")
output_label.grid(row=(number_f_or_c+1), column=0, padx=10, pady=5, sticky="w")
output_entry = tk.Entry(root)
output_entry.insert(0, "output.csv")
output_entry.grid(row=(number_f_or_c+1), column=1, padx=10, pady=5, columnspan=2)

model_label = tk.Label(root, text="Model file (e.g., model.joblib):")
model_label.grid(row=(number_f_or_c+2), column=0, padx=10, pady=5, sticky="w")
model_entry = tk.Entry(root)
model_entry.insert(0, "model.joblib")
model_entry.grid(row=(number_f_or_c+2), column=1, padx=10, pady=5, columnspan=2)

run_button = tk.Button(root, text="Run Command", command=run_command)
run_button.grid(row=(number_f_or_c+3), column=0, columnspan=3, pady=20)

help_button = tk.Button(root, text="Help", command=show_help)
help_button.grid(row=(number_f_or_c+4), column=0, columnspan=3, pady=5)

root.mainloop()
