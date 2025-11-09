from tkinter import *
from functools import partial


class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculator")
        self.root.geometry("400x600")
        self.frame = Frame(root, highlightthickness=5, highlightbackground="black", bg="gray")
        self.frame.pack(padx=10, pady=20)

        # Display Screen
        self.screen = Label(
            self.frame,
            width=23,
            height=4,
            text=" ",
            font=("arial", 14),
            relief=SUNKEN,
            bd=15,
            anchor="se",
        )
        self.screen.grid(row=0, column=0, columnspan=4, sticky=N)

        # Initialize variables
        self.output = ""
        self.decimal = False
        self.buttons = []
        self.values = [
            "C", "sqrt", "^", "%",
            "1", "2", "3", "+",
            "4", "5", "6", "-",
            "7", "8", "9", "*",
            "0", ".", "=", "/"
        ]

        self.create_buttons()

    def create_buttons(self):
        y = 1
        for j in range(2, 7):
            for i in range(0, 4):
                value = self.values[y - 1]
                if value in "0123456789.":
                    btn = Button(
                        self.frame,
                        width=2,
                        height=2,
                        text=value,
                        bg="light gray",
                        relief=RAISED,
                        bd=5,
                        font=("arial", 18),
                        command=partial(self.on_button_click, value))
                elif value != "=":
                    btn = Button(
                        self.frame,
                        width=2,
                        height=2,
                        text=value,
                        bg="gray",
                        relief=RAISED,
                        bd=5,
                        font=("arial", 18),
                        command=partial(self.on_button_click, value),
                        state=DISABLED)
                else:
                    btn = Button(
                        self.frame,
                        width=2,
                        height=2,
                        text=value,
                        bg="orange",
                        relief=RAISED,
                        bd=5,
                        font=("arial", 18),
                        command=partial(self.on_button_click, value),
                        state=DISABLED)

                btn.grid(row=j, column=i)
                self.buttons.append(btn)
                y += 1

    def on_button_click(self, value):
        if value in "0123456789.":
            self.handle_number(value)
        elif value == "C":
            self.clear()
        elif value in "%+-/*x^y":
            self.handle_operator(value)
        elif value == "=":
            self.calculate()
        elif value == "sqrt":
            self.square_root()

    def handle_number(self, value):
        self.output += value
        self.screen["text"] = self.output

        # Enable all numeric buttons again
        for btn in self.buttons:
            if self.values[self.buttons.index(btn)] != "." or not self.decimal:
                btn["state"] = NORMAL

        if value == ".":
            self.buttons[17]["state"] = DISABLED
            self.decimal = True

        if " " in self.output:
            self.buttons[1]["state"] = DISABLED  # disable sqrt after operator

    def clear(self):
        self.output = ""
        self.screen["text"] = self.output
        for btn in self.buttons:
            val = self.values[self.buttons.index(btn)]
            if val in "%+-/*x^y=sqrtC":
                btn["state"] = DISABLED
            else:
                btn["state"] = NORMAL

    def handle_operator(self, value):
        self.output += f" {value} "
        self.screen["text"] = self.output

        for btn in self.buttons:
            val = self.values[self.buttons.index(btn)]
            if val in "%+-/*x^y=sqrt" or (val=="0" and value=="/"):
                btn["state"] = DISABLED                
        self.buttons[17]["state"] = NORMAL  # enable decimal

    def calculate(self):
        calc = self.output.split()
        new_calc = calc.copy()

        while True:
            calc = new_calc
            stop = False
            cont = False

            # Exponentiation
            for i in range(len(calc) - 1):
                if len(calc) >= 3 and calc[i] == "^":
                    new_calc = calc.copy()
                    num1, num2 = calc[i - 1], calc[i + 1]
                    new_calc[i] = float(num1) ** float(num2)
                    new_calc.remove(num1)
                    new_calc.remove(num2)
                    cont = True
                    break
            if cont:
                continue

            # Multiplication, Division, Modulus
            for i in range(len(calc) - 1):
                if len(calc) < 3:
                    stop = True
                    break

                op = calc[i]
                if op in ["*", "/", "%"]:
                    new_calc = calc.copy()
                    num1, num2 = float(calc[i - 1]), float(calc[i + 1])
                    if op == "*":
                        result = num1 * num2
                    elif op == "/":
                        result = num1 / num2
                    else:
                        result = num1 % num2
                    new_calc[i] = result
                    new_calc.remove(calc[i - 1])
                    new_calc.remove(calc[i + 1])
                    cont = True
                    break
            if cont:
                continue

            # Addition, Subtraction
            for i in range(len(calc)):
                if len(calc) < 3:
                    stop = True
                    break

                op = calc[i]
                if op in ["+", "-"]:
                    new_calc = calc.copy()
                    num1, num2 = float(calc[i - 1]), float(calc[i + 1])
                    result = num1 + num2 if op == "+" else num1 - num2
                    new_calc[i] = result
                    new_calc.remove(calc[i - 1])
                    new_calc.remove(calc[i + 1])
                    break

            if stop:
                break

        # Display result
        result = round(float(calc[0]), 9)
        self.output = str(int(result)) if result.is_integer() else str(result)
        self.screen["text"] = self.output

        # Enable buttons
        for btn in self.buttons:
            btn["state"] = NORMAL

        if "." in self.output:
            self.buttons[17]["state"] = DISABLED

    def square_root(self):
        self.output = str(round(float(self.output) ** 0.5, 9))
        if "." in self.output:
            self.buttons[17]["state"] = DISABLED
        self.screen["text"] = self.output


if __name__ == "__main__":
    root = Tk()
    Calculator(root)
    root.mainloop()

