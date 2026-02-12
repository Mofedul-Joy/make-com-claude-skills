# Make.com MCP Server Setup Guide

## ✅ MCP Server Configuration Complete

The `.mcp.json` file has been updated with the official Make.com MCP server configuration using OAuth connection.

## Current Configuration

The MCP server is configured to connect via:
- **Connection URL**: `https://mcp.make.com/sse`
- **Transport Method**: Server-Sent Events (SSE) via Cloudflare `mcp-remote` proxy
- **Authentication**: OAuth (requires browser authorization)

## Next Steps

### 1. Restart Claude Code

For the MCP server configuration to take effect:
1. Exit Claude Code completely
2. Relaunch Claude Code
3. Claude will detect the new MCP server

### 2. Authorize Make.com Connection

When Claude Code starts, it will prompt you to authorize the Make.com connection:
1. Click the authorization link
2. Sign in to your Make.com account
3. Grant the requested permissions (scopes)
4. Return to Claude Code

### 3. Verify Installation

After authorization, test the connection by asking Claude:
- "List my Make.com scenarios"
- "What Make.com tools do you have available?"
- "Show me the connection status for Make"

## Available Scopes

The OAuth connection will request access to:

**Scenario Run Tools** (available to all plans):
- Run active and on-demand scenarios
- View scenario execution results

**Management Tools** (paid plans only):
- View and modify scenarios
- Manage connections, webhooks, data stores
- View and modify teams and organizations

## Alternative: MCP Token Configuration

If you prefer to use an MCP token instead of OAuth:

1. **Generate MCP Token** in your Make profile
2. **Update `.mcp.json`** with:

```json
{
  "mcpServers": {
    "make": {
      "command": "npx",
      "args": [
        "-y",
        "mcp-remote",
        "https://<MAKE_ZONE>/mcp/u/<MCP_TOKEN>/sse"
      ]
    }
  }
}
```

Replace:
- `<MAKE_ZONE>` - Your organization zone (e.g., `eu2.make.com`, `us1.make.com`)
- `<MCP_TOKEN>` - Your generated MCP token

## Timeout Limits

**Scenario Run Tools:**
- OAuth connection: 25 seconds
- MCP token: 40 seconds

**Management Tools:**
- OAuth connection: 30 seconds
- MCP token (SSE): 5 minutes, 20 seconds

**Note**: If a scenario run times out, it continues running in Make (up to 40 minutes). You can retrieve the output using the `executionId` returned in the timeout response.

## Using Scenarios as Tools

To make your scenarios available as AI tools:

1. **Enable scenario inputs/outputs** - Define what data the scenario receives and returns
2. **Add detailed descriptions** - Help AI understand the scenario's purpose
3. **Activate scenarios** - Only active and on-demand scenarios are available as tools

## Troubleshooting

### Connection Issues
- Verify you're signed in to Make.com
- Check your Make.com plan supports the requested scopes
- Try regenerating the OAuth authorization

### Tool Not Found
- Ensure scenarios are activated or set to on-demand
- Check scenario has inputs/outputs defined
- Restart Claude Code after making changes

### Timeout Errors
- For long-running scenarios, retrieve results asynchronously
- Consider using MCP token for longer timeouts
- Optimize scenario execution time

## Resources

- [Make MCP Server Documentation](https://developers.make.com/mcp-server/)
- [Scenario Inputs and Outputs](https://help.make.com/scenario-inputs-and-outputs)
- [MCP Token Access Control](https://developers.make.com/mcp-server/connect-using-mcp-token/scenarios-as-tools-access-control)

## Integration with Make.com Skills

Once the MCP server is connected, you can use the 7 Make.com Skills in this workspace to:
- Build new scenarios using Claude
- Debug existing scenarios
- Configure modules and error handling
- Write custom JavaScript functions

The skills will automatically use the connected MCP server to create, update, and manage your scenarios.
