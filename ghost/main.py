from rich.console import Console
console = Console()

def main():
    console.print("[bold purple]Ghost CLI — Ready![/bold purple]")
    while True:
        cmd = input("ghost> ")
        if cmd in ("exit", "quit"):
            break
        console.print(f"You typed: {cmd}")

if __name__ == "__main__":
    main()
