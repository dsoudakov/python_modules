"""Console script for tg_message."""
from tg_message import send_message
from datetime import datetime
import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer()
console = Console()

@app.command()
def main(text: str = typer.Argument(..., help="Text of the message to send"),
          debug: bool = typer.Option(False, help="Enable debug mode to print message details")):
    """
    Send a message to Telegram using the send_message function.
    """
    try:
        response = send_message(text)
        if response and response.get('ok'):
            console.print("[green]Message sent successfully![/green]", style="bold")
            if debug:
                result = response.get('result', {})
                message_details = {
                    'Message ID': result.get('message_id'),
                    'From': result.get('from', {}).get('first_name', 'N/A'),
                    'Username': result.get('from', {}).get('username', 'N/A'),
                    'Chat ID': result.get('chat', {}).get('id'),
                    'Recipient': f"{result.get('chat', {}).get('first_name', '')} {result.get('chat', {}).get('last_name', '').strip()}",
                    'Date': datetime.fromtimestamp(result.get('date')).strftime('%Y-%m-%d %H:%M:%S'),
                    'Text': result.get('text')
                }
                display_message_details(message_details)
        else:
            console.print("[yellow]Message was sent, but no response from server.[/yellow]", style="bold")
    except ValueError as ve:
        console.print(f"[red]Error: {ve}[/red]", style="bold")
    except EnvironmentError as ee:
        console.print(f"[red]Setup Error: {ee}[/red]", style="bold")
    except Exception as e:
        console.print(f"[red]An unexpected error occurred: {str(e)}[/red]", style="bold")

def display_message_details(details):
    table = Table(title="Message Details")
    for key in details.keys():
        table.add_column(key, justify="left", style="cyan", no_wrap=True)
    table.add_row(*[str(value) for value in details.values()])
    console.print(table)

if __name__ == "__main__":
    app()
