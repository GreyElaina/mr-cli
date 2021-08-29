import typer
from pathlib import Path
import rich.console
import subprocess
import sys

app = typer.Typer()
console = rich.console.Console(markup=True)

def create_and_return(p: Path) -> Path:
    if not p.exists():
        p.mkdir()
    return p

MR_MAIN_PATH = create_and_return(Path("./.mr"))
MR_REPOS_PATH = create_and_return(MR_MAIN_PATH / "repos")
MR_TEMP_FILE = MR_MAIN_PATH / ".temp_file"
PYPROJECT_FILE = Path("./pyproject.toml")
PYPROJECT_FILE_TEMP = Path("./.pyproject.toml.temp")

@app.command()
def ls():
    """列出所有已经存在的子包"""
    repos = [i.name[5:-5] for i in list(MR_REPOS_PATH.glob("repo.*.toml"))]
    return console.print("\n".join([
        "该项目下存在的子包:",
        *[f" - [bold underline]{i}[/]" for i in repos]
    ]))

@app.command()
def new(name: str):
    """新建一个子包"""
    subpkg = MR_REPOS_PATH / f"repo.{name}.toml"
    if subpkg.exists():
        return console.print(f"[bold yellow]?[/] 子包 [bold underline]{name}[/] 已经存在, 跳过该次操作.")
    else:
        if not typer.confirm(f"你确定要为你的项目新建一个名为 {name} 的子包吗?", abort=False):
            return console.print(f"[bold red]![/] 本次操作已放弃.")
        if PYPROJECT_FILE.exists():
            console.print(f"已检测到当前环境中的 pyproject.toml 文件., 对其进行临时更名.")
            PYPROJECT_FILE.rename(".pyproject.toml.temp")
        console.print(f"[bold cyan]I[/] 即将调用 poetry 创建子包 [bold underline]{name}[/], 请注意, 你不必将 package name 作为你填入的子包名称.")
        subprocess.call(["poetry", "init"], stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr)
        if PYPROJECT_FILE.exists():
            console.print(f"[bold cyan]I[/] 检测到 pyproject.toml 已经被创建.")
            typer.pause(f"要立即将现在的 pyproject.toml 作为子包 [{name}] 的配置保存, 请按回车键继续...")
            subpkg.touch()
            subpkg.write_text(PYPROJECT_FILE.read_text(encoding="utf-8"), encoding="utf-8")
            console.print(f"[bold cyan]I[/] 配置已保存, 工作区配置已自动切换.")
            if typer.confirm("需要恢复至您之前的工作区状态吗?"):
                PYPROJECT_FILE.unlink()
                PYPROJECT_FILE_TEMP.rename("pyproject.toml")
                console.print("[bold cyan]I[/] 已恢复至您之前的工作区状态.")
            console.print(f"[bold cyan]I[/] 子包 [bold underline]{name}[/] 创建流程已结束.")
        else:
            console.print(f"[bold red]![/] 检测到 pyproject.toml 不存在, 子包 [bold underline]{name}[/] 的创建流程中止...")
            raise typer.Exit(-1)

@app.command()
def use(name: str):
    """将一个子包的配置载入当前工作区"""
    subpkg = MR_REPOS_PATH / f"repo.{name}.toml"
    if not subpkg.exists():
        console.print(f"[bold red]![/] 子包 [bold underline]{name}[/] 不存在.")
        raise typer.Exit(-1)
    PYPROJECT_FILE.write_text(subpkg.read_text(encoding="utf-8"), encoding="utf-8")
    return console.print(f"[bold cyan]I[/] 工作区配置已切换至子包 [bold underline]{name}[/].")

@app.command()
def reset():
    """恢复当前工作区"""
    if PYPROJECT_FILE.exists():
        PYPROJECT_FILE.unlink()
        return console.print(f"[bold cyan]I[/] 工作区配置已清理.")
    console.print(f"[bold red]![/] 当前不存在任何可用配置.")
    raise typer.Exit(-1)

@app.command()
def remove(name: str):
    """删除一个子包"""
    subpkg = MR_REPOS_PATH / f"repo.{name}.toml"
    if not subpkg.exists():
        console.print(f"[bold red]![/] 子包 [bold underline]{name}[/] 不存在.")
        raise typer.Exit(-1)
    if typer.confirm(f"你确定要删除子包 [bold underline]{name}[/] 吗?"):
        subpkg.unlink()
        return console.print(f"[bold cyan]I[/] 子包 [bold underline]{name}[/] 已被删除.")
    else:
        return console.print(f"[bold red]![/] 子包 [bold underline]{name}[/] 的删除流程已经中止.")

@app.command()
def save(name: str, confirmed: bool = False):
    """将当前工作区的配置保存为指定子包的配置"""
    subpkg = MR_REPOS_PATH / f"repo.{name}.toml"
    if subpkg.exists() and (confirmed or not typer.confirm(f"? 子包 {name} 已存在, 是否覆盖?", default=False, abort=False)):
        raise typer.Exit(-1)
    subpkg.write_text(PYPROJECT_FILE.read_text(encoding="utf-8"), encoding="utf-8")
    return console.print(f"[bold cyan]I[/] 工作区配置已保存至子包 [bold underline]{name}[/].")
