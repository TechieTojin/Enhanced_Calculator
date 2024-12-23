import tkinter as tk
from tkinter import ttk, messagebox
import math
import matplotlib.pyplot as plt
import numpy as np

class Calculator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Enhanced Calculator")
        self.geometry("400x600")
        self.resizable(False, False)

        self.entry = ttk.Entry(self, justify="right", font=("Arial", 20))
        self.entry.grid(row=0, column=0, columnspan=4, sticky="nsew", padx=10, pady=10)

        self.memory = 0
        self.history = []
        self.is_advanced = False  # Toggle for basic/advanced mode
        self.theme = "light"

        # Currency conversion data
        self.currencies = {
            'USD': 'United States Dollar',
            'EUR': 'Euro',
            'GBP': 'British Pound',
            'JPY': 'Japanese Yen',
            'INR': 'Indian Rupee',
            'AUD': 'Australian Dollar',
            'CAD': 'Canadian Dollar',
            'CHF': 'Swiss Franc',
            'CNY': 'Chinese Yuan',
            'MXN': 'Mexican Peso'
        }

        self.create_buttons()
        self.bind_keys()
        self.apply_theme()

    def apply_theme(self):
        if self.theme == "light":
            self.configure(bg="#FFFFFF")
            style = ttk.Style()
            style.configure("TButton", background="#DDDDDD", foreground="#000000", font=("Arial", 16))
            style.map("TButton", background=[("active", "#FF6600")])
        else:
            self.configure(bg="#2E2E2E")
            style = ttk.Style()
            style.configure("TButton", background="#4B4B4B", foreground="#FFFFFF", font=("Arial", 16))
            style.map("TButton", background=[("active", "#FF6600")])

    def create_buttons(self):
        self.basic_buttons = [
            '7', '8', '9', '/',
            '4', '5', '6', '*',
            '1', '2', '3', '-',
            '0', '.', '=', '+',
            'C', 'M+', 'M-', 'MR'
        ]

        self.advanced_buttons = [
            'sin', 'cos', 'tan', 'log',
            'exp', '√', 'History', 'Switch Theme', 'Graph'
        ]

        self.update_button_layout()

    def update_button_layout(self):
        for widget in self.winfo_children():
            widget.grid_forget()

        self.entry.grid(row=0, column=0, columnspan=4, sticky="nsew", padx=10, pady=10)

        buttons = self.advanced_buttons if self.is_advanced else self.basic_buttons
        row, col = 1, 0

        for button in buttons:
            ttk.Button(self, text=button, command=lambda b=button: self.on_button_click(b)).grid(
                row=row, column=col, sticky="nsew", padx=5, pady=5
            )
            col += 1
            if col > 3:
                col = 0
                row += 1

        ttk.Button(self, text='Currency Converter', command=self.show_currency_converter).grid(
            row=row, column=0, columnspan=4, sticky="nsew", padx=5, pady=5
        )

        for i in range(4):
            self.grid_columnconfigure(i, weight=1)
        for i in range(row + 1):
            self.grid_rowconfigure(i, weight=1)

    def on_button_click(self, char):
        if char == '=':
            self.calculate()
        elif char in ['M+', 'M-', 'MR', 'C']:
            self.memory_function(char)
        elif char == 'Switch Theme':
            self.toggle_theme()
        elif char == 'History':
            self.show_history()
        elif char == 'Graph':
            self.plot_graph()
        else:
            self.entry.insert(tk.END, char)

    def calculate(self):
        input_expr = self.entry.get()
        try:
            if 'sin' in input_expr:
                result = str(math.sin(math.radians(float(input_expr.split('sin')[1]))))
            elif 'cos' in input_expr:
                result = str(math.cos(math.radians(float(input_expr.split('cos')[1]))))
            elif 'tan' in input_expr:
                result = str(math.tan(math.radians(float(input_expr.split('tan')[1]))))
            elif 'log' in input_expr:
                result = str(math.log(float(input_expr.split('log')[1]), 10))
            elif 'exp' in input_expr:
                result = str(math.exp(float(input_expr.split('exp')[1])))
            elif '√' in input_expr:
                result = str(math.sqrt(float(input_expr.split('√')[1])))
            else:
                result = str(eval(input_expr.strip()))

            self.history.append(f"{input_expr} = {result}")
            self.clear()
            self.entry.insert(tk.END, result)
        except ZeroDivisionError:
            messagebox.showerror("Error", "Cannot divide by zero!")
            self.clear()
        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.clear()

    def memory_function(self, operation):
        try:
            if operation == 'M+':
                self.memory += float(self.entry.get())
                self.clear()
                messagebox.showinfo("Memory", f"Added to memory: {self.memory}")
            elif operation == 'M-':
                self.memory -= float(self.entry.get())
                self.clear()
                messagebox.showinfo("Memory", f"Subtracted from memory: {self.memory}")
            elif operation == 'MR':
                self.clear()
                self.entry.insert(tk.END, str(self.memory))
            elif operation == 'C':
                self.clear()
        except ValueError:
            messagebox.showerror("Error", "Invalid input for memory operation.")

    def clear(self):
        self.entry.delete(0, tk.END)

    def show_history(self):
        history_window = tk.Toplevel(self)
        history_window.title("Calculation History")
        history_window.geometry("300x400")

        for idx, item in enumerate(self.history):
            ttk.Label(history_window, text=item).pack(anchor='w', padx=10)

    def toggle_theme(self):
        self.theme = "dark" if self.theme == "light" else "light"
        self.apply_theme()
        self.update_button_layout()

    def show_currency_converter(self):
        converter_window = tk.Toplevel(self)
        converter_window.title("Currency Converter")

        amount_label = ttk.Label(converter_window, text="Amount:")
        amount_label.grid(row=0, column=0, padx=5, pady=5)

        amount_entry = ttk.Entry(converter_window)
        amount_entry.grid(row=0, column=1, padx=5, pady=5)

        currency_label = ttk.Label(converter_window, text="Convert to:")
        currency_label.grid(row=1, column=0, padx=5, pady=5)

        currency_combo = ttk.Combobox(converter_window, values=list(self.currencies.keys()))
        currency_combo.grid(row=1, column=1, padx=5, pady=5)

        def convert_currency():
            try:
                amount = float(amount_entry.get())
                to_currency = currency_combo.get()
                # Simple conversion rates (hardcoded for example)
                rates = {
                    'USD': 1.0,
                    'EUR': 0.85,
                    'GBP': 0.75,
                    'JPY': 110.0,
                    'AUD': 1.3,
                    'CAD': 1.25,
                    'CHF': 0.9,
                    'CNY': 6.5,
                    'MXN': 20.0
                }
                converted_amount = amount * rates[to_currency]
                messagebox.showinfo("Currency Converter", f"{amount} USD = {converted_amount:.2f} {to_currency}")
            except ValueError:
                messagebox.showerror("Error", "Invalid input for conversion.")

        convert_button = ttk.Button(converter_window, text="Convert", command=convert_currency)
        convert_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

    def plot_graph(self):
        input_expr = self.entry.get()
        x = np.linspace(-10, 10, 400)
        try:
            # Create a function from the input expression
            func = eval("lambda x: " + input_expr.replace("x", "x"))  # Ensures 'x' is recognized
            y = func(x)
            plt.plot(x, y, label=input_expr)
            plt.title("Graph of " + input_expr)
            plt.xlabel("X-axis")
            plt.ylabel("Y-axis")
            plt.axhline(0, color='black', lw=0.5, ls='--')
            plt.axvline(0, color='black', lw=0.5, ls='--')
            plt.legend()
            plt.grid()
            plt.show()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def bind_keys(self):
        for i in range(10):
            self.bind(str(i), lambda event, num=i: self.entry.insert(tk.END, str(num)))
        self.bind('+', lambda event: self.entry.insert(tk.END, '+'))
        self.bind('-', lambda event: self.entry.insert(tk.END, '-'))
        self.bind('*', lambda event: self.entry.insert(tk.END, '*'))
        self.bind('/', lambda event: self.entry.insert(tk.END, '/'))
        self.bind('.', lambda event: self.entry.insert(tk.END, '.'))
        self.bind('<Return>', lambda event: self.calculate())
        self.bind('<BackSpace>', lambda event: self.clear())

if __name__ == "__main__":
    app = Calculator()
    app.mainloop()
