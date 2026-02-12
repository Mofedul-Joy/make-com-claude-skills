# Build with Make.com — Skills

A workspace for designing, building, and managing Make.com scenarios using Claude Code with Make.com MCP server and Skills integration.

This project provides **7 complementary Claude Skills** that teach Claude how to build production-ready Make.com scenarios, similar to the [n8n-skills](https://github.com/czlonkowski/n8n-skills) project.

## Make.com Skills Overview

The following skills are included in this workspace:

| Skill | Description |
|-------|-------------|
| **make-scenario-builder** | Core skill for building scenarios, modules, routers, filters, and scheduling configurations |
| **make-mcp-tools-expert** | Expert guidance on selecting the right MCP server tools and formatting parameters correctly |
| **make-blueprint-syntax** | Deep dive into Make.com's Blueprint JSON structure and manipulation techniques |
| **make-module-configuration** | App-specific module setup and parameter configuration patterns |
| **make-error-handling** | Error handler patterns (Resume, Commit, Rollback, Ignore, Break) and retry strategies |
| **make-validation-expert** | Debugging, troubleshooting, and scenario validation techniques |
| **make-functions-javascript** | Custom JavaScript function development for Make.com scenarios |

Each skill includes comprehensive documentation, code examples, and reference materials to guide Claude in building robust Make.com automations.

## Workflow

1. **Build** — Design and construct Make.com scenarios locally using Claude Code with Make.com Skills and MCP tools
2. **Upload** — Push completed scenarios to your Make.com account via the API
3. **Debug** — Test, troubleshoot, and iterate on scenarios until they are production-ready
4. **Manage** — Remotely create, edit, activate, deactivate, or delete scenarios through the API

## Prerequisites

- A [Make.com](https://www.make.com/) account
- A Make.com API key (generate one from your Make.com account under **Profile > API**)
- Claude Code with MCP server support
- Make.com MCP server package installed and configured
- Make.com Skills installed in Claude Code

## Setup

### 1. Make.com API Key

Store your API key so it can be used by the MCP server and Skills:

```
MAKE_API_KEY=<YOUR_MAKE_API_KEY>
MAKE_TEAM_ID=<YOUR_TEAM_ID>
MAKE_ORGANIZATION_ID=<YOUR_ORGANIZATION_ID>
```

> Keep your API key secure. Never commit it to version control.

### 2. MCP Server Configuration

Add the Make.com MCP server to your Claude Code MCP configuration. Create or update the `.mcp.json` file in this workspace:

```json
{
  "mcpServers": {
    "make": {
      "command": "npx",
      "args": ["-y", "@makehq/mcp-server"],
      "env": {
        "MAKE_API_KEY": "${MAKE_API_KEY}",
        "MAKE_ZONE": "us1",
        "MAKE_TEAM_ID": "${MAKE_TEAM_ID}"
      }
    }
  }
}
```

**Environment Variables:**
- `MAKE_API_KEY` (required): Your Make.com API key
- `MAKE_ZONE` (optional): Region zone (us1, us2, eu1, eu2, etc.)
- `MAKE_TEAM_ID` (optional): Team ID for organization features

The server provides 130+ API operations including scenarios, connections, webhooks, data stores, templates, custom functions, and more.

### 3. Make.com Skills Installation

The skills are located in the `skills/` directory of this workspace. Claude Code automatically detects skills in this location.

**Skills Directory Structure:**
```
skills/
├── make-scenario-builder/
├── make-mcp-tools-expert/
├── make-blueprint-syntax/
├── make-module-configuration/
├── make-error-handling/
├── make-validation-expert/
└── make-functions-javascript/
```

**Verification:**
Ask Claude: "What Make.com skills do you have?" to verify all 7 skills are loaded.

**Usage:**
Simply describe what you want to build, and Claude will automatically leverage the appropriate skills to construct your Make.com scenarios using MCP server tools.

## Usage

Once set up, you can interact with Make.com directly through Claude Code:

### Building Scenarios

- Describe the automation you want and Claude will construct the scenario structure
- Define triggers, actions, filters, routers, and error handlers
- Configure module parameters, mappings, and data transformations

### Uploading and Deploying

- Push locally built scenarios to Make.com via the API
- Clone or duplicate existing scenarios for iteration
- Update live scenarios with new configurations

### Debugging

- Inspect scenario execution logs and error details
- Identify and fix module misconfigurations
- Test individual modules or full scenario runs
- Iterate until the scenario runs cleanly in production

### Remote API Capabilities

With a configured API key, you can:

| Action | Description |
|--------|-------------|
| **Create** | Build new scenarios from scratch |
| **Read** | List and inspect existing scenarios, modules, and connections |
| **Update** | Modify scenario structure, module settings, and scheduling |
| **Delete** | Remove scenarios that are no longer needed |
| **Activate / Deactivate** | Toggle scenarios on or off |
| **Run** | Trigger immediate scenario execution |
| **Clone** | Duplicate scenarios for testing or templating |

## Project Structure

```
.
├── README.md              # This file
├── .mcp.json              # MCP server configuration
├── scripts/               # Skill management utilities
│   ├── init_skill.py      # Initialize new skills
│   ├── package_skill.py   # Package skills as .skill files
│   └── quick_validate.py  # Validate skill structure
├── skills/                # Make.com Claude Skills
│   ├── make-scenario-builder/
│   ├── make-mcp-tools-expert/
│   ├── make-blueprint-syntax/
│   ├── make-module-configuration/
│   ├── make-error-handling/
│   ├── make-validation-expert/
│   └── make-functions-javascript/
├── dist/                  # Packaged skills for distribution
└── scenarios/             # Local scenario definitions (create as needed)
```

## Notes

- Always test scenarios in a development environment before activating in production
- Use Make.com's built-in versioning and execution history for rollback if needed
- Refer to the [Make.com API documentation](https://www.make.com/en/api-documentation) for detailed endpoint references
