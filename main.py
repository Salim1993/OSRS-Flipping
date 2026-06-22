import requests

from src.infrastructure.osrs_api_client import OsrsApiClient
from src.application.use_cases import FetchItemsUseCase, AnalyzeFlipsUseCase
from src.presentation.cli import console, display_flip_opportunities


def main() -> None:
    client = OsrsApiClient()

    try:
        console.print("[bold blue]Fetching OSRS item data...[/bold blue]")
        items = FetchItemsUseCase(client).execute()

        console.print("[bold blue]Analyzing flip opportunities...[/bold blue]")
        opportunities = AnalyzeFlipsUseCase(client).execute(items, top_n=20, sort_by="profit")

        display_flip_opportunities(opportunities)
    except requests.exceptions.ConnectionError:
        console.print("[bold red]Error:[/bold red] Could not reach the OSRS prices API. Check your internet connection.")
    except requests.exceptions.HTTPError as e:
        console.print(f"[bold red]Error:[/bold red] API returned an unexpected response: {e}")
    except Exception as e:
        console.print(f"[bold red]Unexpected error:[/bold red] {e}")


if __name__ == "__main__":
    main()
