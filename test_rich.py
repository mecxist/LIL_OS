from rich.console import Console
from rich.panel import Panel
from rich.box import DOUBLE_EDGE, ROUNDED

console = Console()

console.print(Panel("This is a test box", title="LIL OS Test", box=DOUBLE_EDGE))
console.print()
console.print(Panel("Rounded box style", box=ROUNDED))