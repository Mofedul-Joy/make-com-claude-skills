# Make.com Skills Distribution

This directory contains packaged Make.com Claude Skills ready for distribution.

## Available Packages

### Individual Skills

Each skill is packaged as a `.skill` file (ZIP archive):

1. **make-scenario-builder.skill** - Core scenario building with modules, routers, filters, and scheduling
2. **make-mcp-tools-expert.skill** - MCP server tools and parameter formatting guidance
3. **make-blueprint-syntax.skill** - Blueprint JSON structure and manipulation
4. **make-module-configuration.skill** - App-specific module configuration patterns
5. **make-error-handling.skill** - Error handlers, retry strategies, and DLQ management
6. **make-validation-expert.skill** - Debugging and troubleshooting scenarios
7. **make-functions-javascript.skill** - Custom JavaScript functions

### Complete Bundle

**make-skills-bundle.skill** - All 7 skills in one package for easy installation

## Installation

### Installing Individual Skills

1. Download the desired `.skill` file
2. Extract the ZIP archive
3. Copy the extracted folder to your Claude Code skills directory:
   - **Local workspace**: `<workspace>/skills/`
   - **Global**: `~/.claude/skills/`
4. Restart Claude Code or reload skills

### Installing the Complete Bundle

1. Download `make-skills-bundle.skill`
2. Extract the bundle (contains 7 individual `.skill` files)
3. Extract each individual skill file
4. Copy all 7 skill folders to your skills directory
5. Restart Claude Code or reload skills

## Quick Start

After installation:

1. **Set up MCP server**: Configure `.mcp.json` with Make.com credentials
2. **Ask Claude**: "What Make.com skills do you have?"
3. **Start building**: Describe your automation and Claude will use the appropriate skills

Example prompts:
- "Create a Make.com scenario that sends Slack notifications when a webhook receives data"
- "Build a scenario that syncs Airtable records to a database every 15 minutes"
- "Help me debug this failed scenario execution"

## Package Generation

To regenerate packages from source:

```bash
# From workspace root
python scripts/package_skill.py skills/* --bundle
```

This will create:
- Individual `.skill` files in `dist/`
- Complete bundle as `make-skills-bundle.skill`

## Validation

All packaged skills have been validated for:
- ✅ Valid YAML frontmatter (name, description)
- ✅ Kebab-case naming convention
- ✅ SKILL.md content completeness
- ✅ Reference file integrity

To re-validate:

```bash
python scripts/quick_validate.py skills/*
```

## Requirements

- Claude Code with MCP support
- Make.com account and API key
- Node.js (for running MCP server via npx)

## Support

For issues, questions, or contributions, refer to the main workspace README.

## License

These skills are provided as-is for educational and productivity purposes.
