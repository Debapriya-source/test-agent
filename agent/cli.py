"""CLI interface."""
import click
from pathlib import Path
from rich.console import Console
from rich.table import Table
from .core import Agent

console = Console()

@click.group()
@click.option("--path", "-p", type=click.Path(exists=True), help="Project path")
@click.pass_context
def main(ctx, path):
    """Autonomous coding agent."""
    ctx.ensure_object(dict)
    ctx.obj["agent"] = Agent(Path(path) if path else None)

@main.command()
@click.pass_context
def init(ctx):
    """Initialize agent in project."""
    agent = ctx.obj["agent"]
    console.print("[bold]Initializing agent...[/bold]")

    result = agent.init()

    if result["success"]:
        console.print("[green]Initialized![/green]")
        console.print(f"Languages: {', '.join(result['languages']) or 'none detected'}")
        console.print(f"Frameworks: {', '.join(result['frameworks']) or 'none detected'}")
        console.print(f"Test framework: {result['test_framework'] or 'none detected'}")
        console.print(f"Files: {result['file_count']}")
        console.print(f"Git: {'yes' if result['has_git'] else 'no'}")
    else:
        console.print(f"[red]Error: {result['error']}[/red]")

@main.command()
@click.argument("file", required=False)
@click.option("--interactive", "-i", is_flag=True, help="Create plan interactively")
@click.pass_context
def plan(ctx, file, interactive):
    """Load or create a plan."""
    agent = ctx.obj["agent"]

    if interactive:
        result = agent.plan(interactive=True)
    elif file:
        result = agent.plan(file_path=file)
    else:
        console.print("[red]Provide a plan file or use -i for interactive[/red]")
        return

    if result["success"]:
        console.print(f"[green]Plan created: {result['title']}[/green]")
        console.print(f"Tasks: {result['task_count']}")
    else:
        console.print(f"[red]Error: {result['error']}[/red]")

@main.command()
@click.option("--task", "-t", type=int, help="Run specific task ID")
@click.option("--all", "-a", "all_tasks", is_flag=True, help="Run all pending tasks")
@click.pass_context
def run(ctx, task, all_tasks):
    """Execute tasks."""
    agent = ctx.obj["agent"]

    if task:
        console.print(f"[bold]Running task {task}...[/bold]")
        result = agent.run(task_id=task)
    elif all_tasks:
        console.print("[bold]Running all tasks...[/bold]")
        result = agent.run(all_tasks=True)
    else:
        console.print("[bold]Running next task...[/bold]")
        result = agent.run()

    if result.get("success"):
        msg = result.get("message", "Done")
        console.print(f"[green]{msg}[/green]")
        if "tasks_executed" in result:
            console.print(f"Tasks executed: {result['tasks_executed']}")
    else:
        console.print(f"[red]Error: {result.get('error', 'Failed')}[/red]")

@main.command()
@click.pass_context
def status(ctx):
    """Show current status."""
    agent = ctx.obj["agent"]
    result = agent.status()

    console.print(f"\n[bold]Plans:[/bold] {result['plans']}")

    tasks = result["tasks"]
    console.print(f"\n[bold]Tasks:[/bold]")
    console.print(f"  Total: {tasks['total']}")
    console.print(f"  Pending: {tasks['pending']}")
    console.print(f"  In Progress: {tasks['in_progress']}")
    console.print(f"  Completed: {tasks['completed']}")
    console.print(f"  Failed: {tasks['failed']}")

    if result["pending_tasks"]:
        console.print("\n[bold]Pending:[/bold]")
        table = Table()
        table.add_column("ID")
        table.add_column("Title")
        table.add_column("Type")
        for t in result["pending_tasks"][:10]:
            table.add_row(str(t["id"]), t["title"][:50], t["task_type"])
        console.print(table)

    if result["failed_tasks"]:
        console.print("\n[bold red]Failed:[/bold red]")
        for t in result["failed_tasks"]:
            console.print(f"  [{t['id']}] {t['title']}: {t.get('result', '')[:50]}")

@main.command("knowledge")
@click.pass_context
def show_knowledge(ctx):
    """Show knowledge base summary."""
    agent = ctx.obj["agent"]
    result = agent.knowledge_summary()

    if not result:
        console.print("[yellow]No knowledge yet. Run 'agent init' first.[/yellow]")
        return

    console.print("\n[bold]Project Knowledge:[/bold]")
    for key, value in result.items():
        if isinstance(value, list):
            value = ", ".join(str(v) for v in value) or "none"
        console.print(f"  {key}: {value}")

@main.command()
@click.confirmation_option(prompt="Clear all tasks and plans?")
@click.pass_context
def reset(ctx):
    """Reset all tasks and plans."""
    agent = ctx.obj["agent"]
    result = agent.reset()
    console.print(f"[green]{result['message']}[/green]")

@main.command()
@click.pass_context
def validate(ctx):
    """Run validation (tests + review)."""
    agent = ctx.obj["agent"]
    console.print("[bold]Running validation...[/bold]")

    result = agent.validate()

    if result.get("tests"):
        test_status = "[green]passed[/green]" if result["tests"]["success"] else "[red]failed[/red]"
        console.print(f"Tests: {test_status}")

    if result.get("review"):
        console.print(f"Review: {result['review'].get('message', 'done')}")

    if result["success"]:
        console.print("\n[green]Validation passed![/green]")
    else:
        console.print("\n[red]Validation failed[/red]")

if __name__ == "__main__":
    main()
