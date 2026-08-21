from mcp.server.fastmcp import FastMCP

mcp = FastMCP("sql-post-processing-mcp")


@mcp.tool()
def add_two_numbers(a: int, b: int)->int:
    """


    :param a:
    :param b:
    :return: a + b
    """
    return a + b


if __name__ == "__main__":
    mcp.run(transport="stdio")
