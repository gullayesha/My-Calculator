import ast
import operator
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput

# Safe mathematical operations
OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}

def calculate(node):
    if isinstance(node, ast.Expression):
        return calculate(node.body)

    if isinstance(node, ast.Constant) and type(node.value) in (int, float):
        return node.value

    if isinstance(node, ast.BinOp) and type(node.op) in OPS:
        return OPS[type(node.op)](
            calculate(node.left), calculate(node.right)
        )

    if isinstance(node, ast.UnaryOp) and type(node.op) in OPS:
        return OPS[type(node.op)](calculate(node.operand))

    raise ValueError("Invalid expression")


class CalculatorApp(App):
    def build(self):
        self.expression = ""

        root = BoxLayout(orientation="vertical", padding=8, spacing=8)

        self.display = TextInput(
            text="0",
            font_size=36,
            readonly=True,
            halign="right",
            multiline=False,
            size_hint=(1, 0.22)
        )
        root.add_widget(self.display)

        buttons = [
            ["C", "DEL", "(", ")"],
            ["7", "8", "9", "/"],
            ["4", "5", "6", "*"],
            ["1", "2", "3", "-"],
            ["0", ".", "=", "+"],
        ]

        grid = GridLayout(cols=4, spacing=6)

        for row in buttons:
            for symbol in row:
                button = Button(
                    text=symbol,
                    font_size=28
                )
                button.bind(on_press=self.press)
                grid.add_widget(button)

        root.add_widget(grid)
        return root

    def press(self, button):
        value = button.text

        if value == "C":
            self.expression = ""

        elif value == "DEL":
            self.expression = self.expression[:-1]

        elif value == "=":
            try:
                result = calculate(
                    ast.parse(self.expression, mode="eval")
                )
                self.expression = str(result)
            except Exception:
                self.expression = "Error"

        elif self.expression == "Error":
            self.expression = value

        else:
            self.expression += value

        self.display.text = self.expression or "0"


if __name__ == "__main__":
    CalculatorApp().run()
