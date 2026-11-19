# 🗂️ Enterprise Catalog MCP Server (`enterprise-catalog-mcp`)

**A Python Model Context Protocol (MCP) server enabling AI agents to query, audit, and validate structured enterprise product catalogs and multi-layer Bill of Materials (BOM) schemas.**

![Python](https://shields.io)
![MCP](https://shields.io)
![Database](https://shields.io)
![Client](https://shields.io)

---

## 🎯 Project Overview

Enterprise ERP systems (such as Oracle Fusion and Oracle EBS) store critical SKU lifecycles, component thicknesses, and multi-layered Bill of Materials (BOM) specifications inside rigid relational schemas. When teams rely on manual lookups or static exports, product configuration errors and QA holds slow down production.

**Enterprise Catalog MCP Server** bridges structured enterprise catalog data with agentic AI workflows. Built on Anthropic's open **Model Context Protocol (MCP)** using `MCPServer`, it exposes deterministic query and engineering validation tools so **Claude Desktop** (or any MCP-compliant agent framework, including Cursor, VS Code Copilot, Gemini, or OpenAI Agents) can inspect SKU data and enforce manufacturing tolerances autonomously.

---

## 🏗️ System Architecture

```text
User Prompt in Claude Desktop / MCP Client
  │  (e.g., "Audit SKU-1004 and check if its layer thickness passes QA tolerances")
  ▼
┌──────────────────────────────────────────────────────────────┐
│  LLM Agent Orchestration (Claude / MCP Host)                 │
│  • Selects & chains appropriate MCP tools via JSON-RPC       │
└──────────────────────────────────────────────────────────────┘
  │
  ▼  [stdio Transport]
┌──────────────────────────────────────────────────────────────┐
│  Enterprise Catalog MCP Server (server.py / MCPServer)       │
│                                                              │
│  ├── Tool 1: search_catalog()                                │
│  │     Filters SKUs by category, lifecycle status, or layers │
│  ├── Tool 2: get_sku_bom_details()                           │
│  │     Retrieves full component & print spec metadata        │
│  └── Tool 3: validate_bom_configuration()                    │
│        Enforces engineering rules & packaging thickness gates│
└──────────────────────────────────────────────────────────────┘
  │
  ▼
┌──────────────────────────────────────────────────────────────┐
│  Self-Seeding Relational Store (SQLite / catalog.db)         │
│  • Auto-initializes sample multi-layer ERP SKU records       │
└──────────────────────────────────────────────────────────────┘
```

---

## 🛠️ Exposed MCP Tools

| Tool Name | Parameters | Purpose |
| :--- | :--- | :--- |
| **`search_catalog`** | `category`, `status`, `max_layers` *(all optional)* | Queries the enterprise SKU catalog using dynamic filters (e.g., finding all `Active` or `QA Hold` items under a specific layer count). |
| **`get_sku_bom_details`** | `sku` *(required)* | Retrieves the complete Bill of Materials record—including layer count, finish specification, point (`pt`) thickness, lifecycle status, and unit cost. |
| **`validate_bom_configuration`** | `layer_count`, `thickness_pt` *(required)* | Acts as an automated **Quality Assurance gate**, evaluating proposed multi-layer configurations against manufacturing tolerances (1–8 layers, max 150pt packaging threshold, and structural thickness minimums). |

---

## 🚀 Quickstart & Local Setup

### 1. Clone the Repository
```bash
git clone https://github.com
cd enterprise-catalog-mcp
```

### 2. Create a Virtual Environment & Install Dependencies
```bash
python -m venv .venv

# Windows:
.venv\Scripts\activate

# macOS / Linux:
source .venv/bin/activate

pip install -r requirements.txt
```
*(Note: No separate database installation is required. Running the server automatically initializes and seeds `catalog.db` via Python's built-in `sqlite3` library.)*

### 3. Test with the Interactive MCP Inspector
Launch the built-in MCP developer inspector in your browser to test tool schemas and outputs directly:
```bash
mcp dev server.py
```

---

## 🔌 Connecting to Claude Desktop

1. Open your Claude Desktop configuration file:
   * **macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
   * **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

2. Add the `enterprise-catalog` server entry (replace `/FULL/PATH/TO/` with your local directory path):
```json
{
  "mcpServers": {
    "enterprise-catalog": {
      "command": "python",
      "args": [
        "/FULL/PATH/TO/enterprise-catalog-mcp/server.py"
      ]
    }
  }
}
```

3. Restart **Claude Desktop**. Look for the hammer/tools icon in the chat input bar to confirm the three catalog tools are active.

---

## 💬 Example Agent Prompts

Once connected to Claude Desktop, try asking:
* *"Show me all products in the catalog that are currently on QA Hold."*
* *"Look up the BOM specifications for SKU-1004 and run a validation check to tell me why it might be flagged."*
* *"We are designing a new 7-layer collectible card with a 65pt thickness. Check if that configuration passes our engineering tolerances."*
* *"Compare the unit costs and finish specs across all Active items with 4 or fewer layers."*

---

## 🗺️ Roadmap & Future Extensions
* [ ] **CSV / ERP Flat-File Ingestion:** Add an MCP resource loader to ingest raw Oracle Fusion / EBS item export CSVs directly into SQLite.
* [ ] **Hybrid Vector Search:** Integrate embedding-based semantic search alongside SQL filtering for natural-language finish and material discovery.
* [ ] **Automated Evaluation Suite:** Add `pytest` golden-dataset test cases to benchmark LLM tool-selection accuracy.

---

## 👤 Author
**Sean David Wilda** — AI Solutions Builder & Oracle ERP Systems Specialist  
* [GitHub](https://github.com)
* [LinkedIn](https://linkedin.com)
## 📸 Live Demo
<img width="3840" height="2160" alt="image" src="https://github.com/user-attachments/assets/9eedf04b-300c-4aeb-bf01-1a63ff139c7b" />
