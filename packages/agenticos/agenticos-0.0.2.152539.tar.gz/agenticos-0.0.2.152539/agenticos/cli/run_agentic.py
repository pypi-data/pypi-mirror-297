from subprocess import run


def run_agentic(mode: str, dev: bool) -> None:
    if mode == "httpserver":
        if dev:
            run(
                ["fastapi", "dev", "--reload", "src/agentic/agentic_node.py"],
                check=True,
            )
        else:
            run(["fastapi", "run", "src/agentic/agentic_node.py"], check=True)
    else:
        raise ValueError("Invalid mode")
