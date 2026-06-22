from rich.console import Console
from rich.table import Table
from src.domain.models import FlipOpportunity

console = Console()


def display_flip_opportunities(opportunities: list[FlipOpportunity]) -> None:
    if not opportunities:
        console.print("[yellow]No flip opportunities found with current filters.[/yellow]")
        return

    table = Table(title="Top OSRS Flip Opportunities", show_lines=True)
    table.add_column("#",           style="dim",         justify="right", no_wrap=True)
    table.add_column("Item",        style="cyan",        no_wrap=True)
    table.add_column("Members",     style="dim",         justify="center")
    table.add_column("Buy Price",   style="green",       justify="right")
    table.add_column("Sell Price",  style="green",       justify="right")
    table.add_column("Tax",         style="red",         justify="right")
    table.add_column("Profit",      style="bold green",  justify="right")
    table.add_column("ROI %",       style="yellow",      justify="right")
    table.add_column("Volume (1h)", style="white",       justify="right")

    for rank, opp in enumerate(opportunities, start=1):
        table.add_row(
            str(rank),
            opp.item.name,
            "P2P" if opp.item.members else "F2P",
            f"{opp.buy_price:,}",
            f"{opp.sell_price:,}",
            f"{opp.tax:,}",
            f"{opp.profit:,}",
            f"{opp.roi_percent:.2f}%",
            f"{opp.volume:,}",
        )

    console.print(table)
