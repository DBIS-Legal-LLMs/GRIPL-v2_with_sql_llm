from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
import traceback

class PostProcessingMcpClient:

    def __init__(self):
        self.max_iteration = 3

    async def get_mcp_client_answer(self):

        try:
            server_params = StdioServerParameters(
                command="python",
                args=[
                    "-m",
                    "app.sql_post_processing_component.post_processing_mcp_server"
                ],
            )

            messages = []

            messages.append({"role": "system", "content": ""})

            messages.append(

                {"role": "user", "content": ""})

            async with stdio_client(server_params) as (reader, writer):
                async with ClientSession(reader, writer) as session:
                    await session.initialize()
                    tools_result = await session.list_tools()

                    mcp_tools = tools_result.tools

                    groq_tools = self.convert_mcp_tool_list_to_groq_schema_tool_list(mcp_tools)

                    print("groq tools")
                    print(groq_tools)

                    return "mcp answer client"





        except Exception as e:
            print("error in mcp client")
            print(traceback.format_exc())

    def convert_mcp_tool_list_to_groq_schema_tool_list(self, mcp_tools: list):
        groq_tools = []
        for tool in mcp_tools:
            params = tool.inputSchema.copy()

            params.pop('title', None)
            params.pop('description', None)

            if 'type' not in params or params['type'] != 'object':
                params['type'] = 'object'

            properties = params.get('properties', {})
            if not isinstance(properties, dict):
                properties = {}
            for prop_name, prop_schema in list(properties.items()):
                if not isinstance(prop_schema, dict):
                    properties[prop_name] = {"type": "string"}
                prop_schema.pop('title', None)
                if 'description' not in prop_schema:
                    prop_schema['description'] = prop_name.replace('_', ' ')
                if 'type' not in prop_schema:
                    prop_schema['type'] = 'string'
            params['properties'] = properties

            if 'required' not in params and properties:
                params['required'] = list(properties.keys())

            groq_tools.append({
                "type": "function",
                "function": {
                    "name": tool.name,
                    "description": tool.description or "",
                    "parameters": params
                }
            })
        return groq_tools
