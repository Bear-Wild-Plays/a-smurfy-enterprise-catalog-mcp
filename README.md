# 🗂️ Enterprise Catalog MCP Server (`enterprise-catalog-mcp`)

**A Smurf Village Edition of a Python Model Context Protocol (MCP) server enabling AI agents to query, audit, and validate structured enterprise product catalogs and multi-layer Bill of Materials (BOM) schemas to assist Brainy and Handy Smurf locate items for the Smurf Village.**

![Python](https://shields.io)
![MCP](https://shields.io)
![Database](https://shields.io)
![Client](https://shields.io)

---

#### 🎯 Project Overview

Enterprise ERP systems (such as **Oracle Fusion** and **Oracle EBS**) store critical SKU lifecycles, component thicknesses, and multi-layered Bill of Materials (BOM) specifications inside rigid relational schemas. When teams rely on manual lookups or static exports, product configuration errors and QA holds slow down production. 

**Enterprise Catalog MCP Server** bridges structured enterprise catalog data with agentic AI workflows. Built on Anthropic's open **Model Context Protocol (MCP)** using MCPServer, it exposes deterministic query and engineering validation tools so **Claude Desktop** (or any MCP-compliant agent framework, including **Cursor, VS Code Copilot, Gemini, or OpenAI Agents**) can inspect SKU data and enforce manufacturing tolerances autonomously. 

#### 🍄 The "Brainy-to-Handy" Fuzzy-to-Structured Schema Normalizer

In **Smurf Village**, villagers rarely speak in Oracle SKU numbers—Greedy Smurf asks for *"that sweet red berry paste from two summers ago,"* while Clumsy Smurf describes *"that shiny round thing that wobbles."* 

This server solves the real-world Content Engineering and PLM problem of **messy-input-to-strict-schema normalization**: mapping colloquial natural language into validated **Pydantic / JSON Schemas**, resolving multi-layer BOM hierarchies, and running automated thickness tolerance checks before production release. 

#### 🛠 Exposed MCP Tools

Tool NamePurposeDeterministic Guardrail
**normalize_catalog_query**
Translates ambiguous villager phrasing into canonical Oracle ERP SKU IDs, categories, and lifecycle states.Enforces strict NormalizedCatalogQuery Pydantic JSON schema & match confidence tiers.
**get_sku_bom_details**
Retrieves full parent-child multi-layer BOM structures, materials, and individual layer thicknesses (mm).Read-only deterministic lookup against structured catalog records.
**validate_bom_configuration**
Sums component layer thicknesses across an assembly and compares against max_assembly_thickness_mm.Flags PASS_RELEASE_TO_PRODUCTION vs. FAIL_QA_HOLD_EXCEEDS_TOLERANCE with exact millimeter variance.

#### 🧪 Example Agent Workflow

1. **Villager Prompt:** *"Can you check if 'that sweet red berry paste from two summers ago' passes manufacturing thickness tolerances?"*
2. **Step 1 (normalize_catalog_query):** Resolves colloquial alias → SMF-BRY-PST-256 (*Reserve Smurfberry Festival Glaze & Paste*).
3. **Step 2 (get_sku_bom_details):** Inspects 3-layer BOM (Clay Vessel 5.50mm + Berry Paste 4.20mm + Beeswax Seal 1.80mm).
4. **Step 3 (validate_bom_configuration):** Computes 11.50mm <= 12.00mm max tolerance → returns **PASS_RELEASE_TO_PRODUCTION**.

*(Try querying "the smoky blue bottle that hisses" -> SMF-PAP-GRD-999 to see the MCP server catch a 0.90mm over-tolerance defect and trigger an automated FAIL_QA_HOLD_EXCEEDS_TOLERANCE alert!)* 

#### 🚀 Quickstart

bash

# 1. Install MCP & Pydantic dependencies
pip install -r requirements.txt

# 2. Run the MCP server (or test interactively with MCP Inspector)
mcp dev server.py

Use code with caution.

Copy code text to clipboard.

#### 👤 Author

**Sean David Wilda** — Content Engineer | Supply Chain & Product Lifecycle Specialist | AI Product Quality
[LinkedIn](https://www.linkedin.com/in/sean-wilda-196a2713/) · [Portfolio](https://www.bearwildplays.com)
## 📸 Live Demo
<img width="3840" height="2160" alt="image" src="https://github.com/user-attachments/assets/9eedf04b-300c-4aeb-bf01-1a63ff139c7b" />
