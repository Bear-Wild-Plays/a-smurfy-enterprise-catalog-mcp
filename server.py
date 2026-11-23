import json
from pathlib import Path
from typing import Optional
from pydantic import BaseModel, Field
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Enterprise Catalog MCP Server (Smurf Village ERP Edition)")

CATALOG_PATH = Path(__file__).parent / "data" / "smurf_village_bom_catalog.json"


def _load_catalog() -> list[dict]:
    with open(CATALOG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


class NormalizedCatalogQuery(BaseModel):
    """Strict enterprise schema mapping colloquial villager descriptions to ERP attributes."""
    raw_villager_phrase: str = Field(..., description="Original colloquial query from a villager")
    resolved_sku_id: Optional[str] = Field(None, description="Matched Oracle ERP SKU ID")
    canonical_item_name: Optional[str] = Field(None, description="Official standardized item name")
    category: Optional[str] = Field(None, description="Normalized ERP product category")
    lifecycle_status: Optional[str] = Field(None, description="Current PLM lifecycle state")
    match_confidence: str = Field(..., description="EXACT_ALIAS_MATCH, PARTIAL_KEYWORD_MATCH, or UNRESOLVED")


@mcp.tool()
def normalize_catalog_query(villager_description: str) -> dict:
    """
    Translates messy, colloquial villager descriptions (e.g., 'that sweet red berry paste
    from two summers ago') into a strict, machine-readable ERP catalog schema.
    """
    catalog = _load_catalog()
    query_lower = villager_description.strip().lower()

    for item in catalog:
        aliases = [a.lower() for a in item.get("colloquial_aliases", [])]
        if query_lower in aliases or any(query_lower in a or a in query_lower for a in aliases):
            result = NormalizedCatalogQuery(
                raw_villager_phrase=villager_description,
                resolved_sku_id=item["sku_id"],
                canonical_item_name=item["item_name"],
                category=item["category"],
                lifecycle_status=item["lifecycle_status"],
                match_confidence="EXACT_ALIAS_MATCH",
            )
            return result.model_dump()

    for item in catalog:
        searchable = f"{item['item_name']} {item['category']} {' '.join(item.get('colloquial_aliases', []))}".lower()
        if any(word in searchable for word in query_lower.split() if len(word) > 3):
            result = NormalizedCatalogQuery(
                raw_villager_phrase=villager_description,
                resolved_sku_id=item["sku_id"],
                canonical_item_name=item["item_name"],
                category=item["category"],
                lifecycle_status=item["lifecycle_status"],
                match_confidence="PARTIAL_KEYWORD_MATCH",
            )
            return result.model_dump()

    return NormalizedCatalogQuery(
        raw_villager_phrase=villager_description,
        match_confidence="UNRESOLVED",
    ).model_dump()


@mcp.tool()
def get_sku_bom_details(sku_id: str) -> dict:
    """
    Retrieves the complete multi-layered Bill of Materials (BOM), component thicknesses,
    and ERP lifecycle metadata for a standardized SKU ID.
    """
    catalog = _load_catalog()
    for item in catalog:
        if item["sku_id"].upper() == sku_id.strip().upper():
            return item
    return {"error": f"SKU '{sku_id}' not found in Smurf Village ERP Catalog."}


@mcp.tool()
def validate_bom_configuration(sku_id: str) -> dict:
    """
    Deterministic engineering QA tool: sums multi-layer component thicknesses (mm)
    and validates whether the assembly complies with maximum manufacturing tolerances.
    """
    catalog = _load_catalog()
    for item in catalog:
        if item["sku_id"].upper() == sku_id.strip().upper():
            layers = item.get("bom_layers", [])
            total_thickness = round(sum(layer["thickness_mm"] for layer in layers), 2)
            max_allowed = item["max_assembly_thickness_mm"]
            variance = round(total_thickness - max_allowed, 2)
            passed = total_thickness <= max_allowed

            return {
                "sku_id": item["sku_id"],
                "item_name": item["item_name"],
                "erp_source": item["erp_source"],
                "layer_count": len(layers),
                "calculated_total_thickness_mm": total_thickness,
                "max_allowed_thickness_mm": max_allowed,
                "tolerance_variance_mm": variance,
                "qa_status": "PASS_RELEASE_TO_PRODUCTION" if passed else "FAIL_QA_HOLD_EXCEEDS_TOLERANCE",
            }

    return {"error": f"SKU '{sku_id}' not found for BOM validation."}


if __name__ == "__main__":
    mcp.run()
