from mcp.server.fastmcp import FastMCP


class MCPServer:

    def __init__(self):
        self.mcp = FastMCP("sql-post-processing-mcp")
        self.register_tools()

    def register_tools(self):

        @self.mcp.tool()
        def add_two_numbers(a: int, b: int) -> int:
            """
            Add two numbers.

            :param a: First number
            :param b: Second number
            :return: Sum of a and b
            """
            return a + b

    def start(self):
        self.mcp.run(transport="stdio")


if __name__ == "__main__":
    server = MCPServer()
    server.start()