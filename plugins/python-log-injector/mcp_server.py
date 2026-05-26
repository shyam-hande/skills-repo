from mcp.server.fastmcp import FastMCP

mcp = FastMCP("python-log-injector")


@mcp.tool()
def inject_logs(code: str) -> str:
    """
    Adds log statements to python functions.
    """

    lines = code.split("\n")

    modified = []

    for line in lines:
        modified.append(line)

        if line.strip().startswith("def "):
            indent = " " * (len(line) - len(line.lstrip()) + 4)
            fn_name = line.strip().split("def ")[1].split("(")[0]

            modified.append(
                f'{indent}print("[LOG] Entering function: {fn_name}")'
            )

    return "\n".join(modified)


if __name__ == "__main__":
    mcp.run()