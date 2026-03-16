import pandas as pd
import json
from pathlib import Path
import re
from typing import Dict, Any, List, Optional, cast

# Constants
DESIGN_DOC_PATH = Path("docs/content_design/characters/THEORIST_SIMPLIFIED_DESIGN.md")
CARDS_JSON_PATH = Path("data/cards.json")

def load_design_doc(path: Path) -> Optional[pd.DataFrame]:
    """Loads all markdown tables from the design document into a single DataFrame."""
    print(f"--- 1. Loading Design Document: {path} ---")
    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        
        tables = re.findall(r"(\|.*->\n\|-.*->\n(->:\|.*->\n)+)", content)
        if not tables:
            print("  [Error] No markdown tables found in the document.")
            return None
        
        all_dfs = []
        for i, table_str in enumerate(tables):
            lines = table_str.strip().split('\n')
            header = [h.strip() for h in lines[0].strip('|').split('|')]
            rows = []
            for line in lines[2:]:
                rows.append([r.strip() for r in line.strip('|').split('|')])
            
            df = pd.DataFrame(rows, columns=header)
            if "中文名称" in df.columns and "卡牌名称 (英文)" in df.columns:
                df["中文名称"] = df["中文名称"].str.replace(r"\*\*", "", regex=True)
                all_dfs.append(df)
        
        if not all_dfs:
            print("  [Error] No valid card tables found (missing '中文名称' or '卡牌名称 (英文)' columns).")
            return None
            
        full_design_df = pd.concat(all_dfs, ignore_index=True)
        print(f"  [Success] Loaded {len(full_design_df)} card designs from {len(all_dfs)} tables.")
        return full_design_df

    except Exception as e:
        print(f"  [Error] Failed to load or parse design document: {e}")
        return None

def validate_design_doc_schema(df: pd.DataFrame) -> bool:
    """Step 1: Validates the schema of the design document DataFrame."""
    print("\n--- 2. Validating Design Document Schema ---")
    required_columns = ["中文名称", "卡牌名称 (英文)", "类型", "费用", "效果描述 (中文)"]
    missing_columns = [col for col in required_columns if col not in df.columns]
    
    if missing_columns:
        print(f"  [Error] Design document is missing required columns: {', '.join(missing_columns)}")
        return False
        
    print("  [Success] Design document schema is valid.")
    return True

def analyze_effects_from_description(description: str) -> List[Dict[str, Any]]:
    """Analyzes a card's description text and returns a list of expected effects."""
    EFFECT_KEYWORD_MAP: Dict[str, Dict[str, Any] | str] = {
        r"造成 (->P<base_damage>\d+) 点伤害.*->严谨度对此牌效果翻 (->P<multiplier>\d+) 倍": "heavy_blade_special",
        r"造成 (->P<value>\d+) 点伤害": {"type": "damage"},
        r"获得 (->P<value>\d+) 点自信": {"type": "block"},
        r"获得 (->P<value>\d+) 点格挡": {"type": "block"},
        r"抽 (->P<value>\d+) 张牌": {"type": "draw"},
        r"获得 (->P<value>\d+) 点严谨度": {"type": "rigor"},
        r"施加 (->P<value>\d+) 层破防": {"type": "status", "status_type": "Vulnerable"},
    }
    
    expected_effects = []
    
    for pattern, effect_template in EFFECT_KEYWORD_MAP.items():
        match = re.search(pattern, description)
        if match:
            if effect_template == "heavy_blade_special":
                base_damage = int(match.groupdict()['base_damage'])
                multiplier = int(match.groupdict()['multiplier'])
                expected_effects.append({
                    "type": "damage", 
                    "value": base_damage, 
                    "rigor_multiplier": multiplier
                })
                continue

            found_effect = dict(cast(Dict[str, Any], effect_template))
            # Use a generic 'value' key in the regex if possible to simplify this
            if 'value' in match.groupdict() and match.groupdict()['value']:
                value = int(match.groupdict()['value'])
                if found_effect.get("type") == "status":
                    found_effect["duration"] = value
                else:
                    found_effect["value"] = value
            expected_effects.append(found_effect)

    # Implicit consume rigor for any attack or skill card that isn't a power
    # This is a broad assumption based on the design doc's core mechanic
    if any(e['type'] in ['damage', 'block'] for e in expected_effects):
        if not any(e['type'] == 'rigor' for e in expected_effects): # Powers that grant rigor shouldn't consume it
             expected_effects.append({'type': 'consume_rigor'})
            
    return expected_effects

def compare_design_vs_implementation(design_df: pd.DataFrame, impl_cards: Dict[str, Any]):
    """Step 2 & 3: Compare design to implementation and report findings."""
    print("\n--- 3. Comparing Design vs. Implementation ---")
    
    design_card_names = set(design_df["中文名称"])
    impl_card_names = set(impl_cards.keys())
    
    implemented_cards = design_card_names.intersection(impl_card_names)
    unimplemented_cards = design_card_names.difference(impl_card_names)
    
    total_design_cards = len(design_card_names)
    total_implemented_cards = len(implemented_cards)
    coverage = (total_implemented_cards / total_design_cards) * 100 if total_design_cards > 0 else 0
    
    print("\n--- Coverage Report ---")
    print(f"  - Total cards in design: {total_design_cards}")
    print(f"  - Implemented cards: {total_implemented_cards}")
    print(f"  - Implementation Coverage: {coverage:.2f}%")
    
    if unimplemented_cards:
        print("\n  [Info] Unimplemented Cards:")
        for card_name in sorted(list(unimplemented_cards)):
            print(f"    - {card_name}")
            
    print("\n--- Consistency Report ---")
    all_consistent = True
    for card_name in sorted(list(implemented_cards)):
        design_info = design_df[design_df["中文名称"] == card_name].iloc[0]
        impl_info = impl_cards[card_name]
        
        issues = []
        
        try:
            design_cost_str = str(design_info["费用"]).strip()
            if design_cost_str.isdigit():
                design_cost = int(design_cost_str)
                if design_cost != impl_info.get("cost"):
                    issues.append(f"Cost mismatch: Design='{design_cost}', Impl='{impl_info.get('cost')}'")
        except (ValueError, TypeError):
            pass 
            
        type_mapping = {"能力": "Power", "攻击": "Attack", "技能": "Skill"}
        design_type = design_info["类型"]
        expected_impl_type = type_mapping.get(design_type)
        if expected_impl_type and expected_impl_type != impl_info.get("type"):
            issues.append(f"Type mismatch: Design='{design_type}', Impl='{impl_info.get('type')}'")
            
        design_description = design_info["效果描述 (中文)"]
        expected_effects = analyze_effects_from_description(design_description)
        impl_effects = impl_info.get("effects", [])
        
        for expected in expected_effects:
            is_found = any(all(item in impl.items() for item in expected.items()) for impl in impl_effects)
            if not is_found:
                issues.append(f"Effect not found in implementation: {expected}")

        # Check for unexpected effects in implementation
        for impl in impl_effects:
            is_expected = any(all(item in impl.items() for item in expected.items()) for expected in expected_effects)
            # This logic is complex because of implicit effects like consume_rigor.
            # A more robust check might be needed if false positives appear.
            if not is_expected:
                # Let's only flag effects that are clearly not the implicit 'consume_rigor'
                if impl.get('type') != 'consume_rigor':
                     issues.append(f"Unexpected effect in implementation: {impl}")

        if issues:
            all_consistent = False
            # Ensure card_name is printed only once, outside the loop
            print(f"\n  [Warning] Inconsistencies found for '{card_name}':")
            for issue in issues:
                # Ensure the issue is a string before printing
                print(f"    - {str(issue)}")
        
    if all_consistent:
        print("\n  [Success] All implemented cards are consistent with the design document!")


def main():
    """Main validation function."""
    design_df = load_design_doc(DESIGN_DOC_PATH)
    
    if design_df is None:
        return

    if not validate_design_doc_schema(design_df):
        return
        
    try:
        with open(CARDS_JSON_PATH, "r", encoding="utf-8") as f:
            impl_data = json.load(f)
        
        impl_cards_map = {
            card['name_key']: card 
            for card in impl_data['cards'] 
            if not card['card_id'].endswith("_upgraded")
        }
    except Exception as e:
        print(f"\n[Error] Failed to load or parse implementation file '{CARDS_JSON_PATH}': {e}")
        return

    compare_design_vs_implementation(design_df, impl_cards_map)

if __name__ == "__main__":
    main() 
