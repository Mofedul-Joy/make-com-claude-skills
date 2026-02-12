# Make.com MCP Server Installation for Antigravity

## Issue: MCP Server Not Appearing

The `.mcp.json` file in your workspace is **not** the configuration file that Antigravity uses. 

## Solution

Antigravity uses a **global MCP configuration file** that needs to be edited manually.

### Steps to Install Make.com MCP Server

#### 1. Locate Your Antigravity MCP Config File

The configuration file is typically located at one of these paths:
- `~/Library/Application Support/Antigravity/mcp.json`
- `~/.config/antigravity/mcp.json`
- Check Antigravity settings for the exact location

#### 2. Add Make.com Server Configuration

Open the MCP configuration file and add the Make.com server:

```json
{
  "mcpServers": {
    "make": {
      "command": "npx",
      "args": [
        "-y",
        "mcp-remote",
        "https://mcp.make.com/sse"
      ]
    }
  }
}
```

**If you already have other MCP servers**, just add the `"make"` entry:

```json
{
  "mcpServers": {
    "existing-server": {
      ...
    },
    "make": {
      "command": "npx",
      "args": [
        "-y",
        "mcp-remote",
        "https://mcp.make.com/sse"
      ]
    }
  }
}
```

#### 3. Restart Antigravity

- Quit Antigravity completely
- Relaunch Antigravity
- Go to "Manage MCP Servers" to verify Make appears

#### 4. Authorize Make.com

Once the server appears:
1. Click on the Make server in "Manage MCP Servers"
2. Click "Authorize" or "Connect"
3. Sign in to your Make.com account in the browser
4. Grant the requested permissions
5. Return to Antigravity

## Alternative: Find Config File via Antigravity Settings

1. Open Antigravity Settings/Preferences
2. Look for "MCP Servers" or "Model Context Protocol" section
3. There should be an option to "Edit Configuration" or "Open Config File"
4. This will show you the exact file location and let you edit it

## Verify Installation

After restarting, the Make server should appear in:
- **Settings → Manage MCP Servers** (or similar)
- Server name: `make`
- Status: Should show as "Connected" or "Ready to authorize"

## Need Help?

If you can't find the config file location, please:
1. Go to Antigravity Settings/Preferences
2. Look for MCP-related settings
3. Share a screenshot or the path shown there
4. I can then provide the exact configuration to add

## Configuration Details

**Connection Type**: OAuth (browser-based authorization)  
**Transport**: Server-Sent Events (SSE) via mcp-remote proxy  
**Endpoint**: `https://mcp.make.com/sse`  

**What this enables:**
- Run Make.com scenarios from Antigravity
- Create and modify scenarios
- Manage connections, webhooks, data stores
- Use scenarios as callable AI tools
