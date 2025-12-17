# // 2025-12-17-19-30-00
# // unified_dictionary_builder/build_dictionary.py
# // Author: R. A. Carucci
# // Purpose: Build unified data dictionary from canonical schema and extracted rules

"""
Build Unified Data Dictionary

This script generates the unified data dictionary in CSV, XLSX, and JSON formats
from the canonical schema and extracted field rules.

Usage:
    python build_dictionary.py --schema docs/schema/canonical_schema.json --output docs/data_dictionary/
"""

import json
import pandas as pd
from pathlib import Path
from datetime import datetime
from typing import Dict, List
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def load_canonical_schema(schema_path: str) -> Dict:
    """
    Load the canonical schema from JSON file.
    
    Args:
        schema_path: Path to canonical_schema.json
        
    Returns:
        Dictionary containing schema definition
    """
    logger.info(f"Loading canonical schema from {schema_path}")
    
    with open(schema_path, 'r') as f:
        schema = json.load(f)
    
    logger.info(f"Loaded schema with {len(schema['fields'])} fields")
    return schema


def flatten_field_definitions(schema: Dict) -> List[Dict]:
    """
    Flatten nested field definitions into tabular format.
    
    Args:
        schema: Canonical schema dictionary
        
    Returns:
        List of flattened field dictionaries
    """
    logger.info("Flattening field definitions")
    
    flattened = []
    
    for field_name, field_def in schema['fields'].items():
        row = {
            'field_name': field_name,
            'display_name': field_def.get('display_name'),
            'source_system': field_def.get('source_system'),
            'internal_field_name': field_def.get('internal_field_name'),
            'data_type': field_def.get('data_type'),
            'format': field_def.get('format'),
            'max_length': field_def.get('max_length'),
            'nullable': field_def.get('nullable'),
            'primary_key': field_def.get('primary_key'),
            'examples': ', '.join(map(str, field_def.get('examples', []))),
            'description': field_def.get('description'),
            'validation_rules': ' | '.join(field_def.get('validation_rules', [])),
            'derivation': field_def.get('derivation'),
            'dependencies': ', '.join(field_def.get('dependencies', [])),
            'used_in': ', '.join(field_def.get('used_in', [])),
            'quality_check': field_def.get('quality_check'),
            'controlled_values': str(field_def.get('controlled_values')) if field_def.get('controlled_values') else None
        }
        
        flattened.append(row)
    
    logger.info(f"Flattened {len(flattened)} field definitions")
    return flattened


def build_vocabulary_lists(schema: Dict) -> Dict[str, List]:
    """
    Extract controlled vocabulary lists from schema.
    
    Args:
        schema: Canonical schema dictionary
        
    Returns:
        Dictionary of field_name -> vocabulary list
    """
    logger.info("Building vocabulary lists")
    
    vocabularies = {}
    
    for field_name, field_def in schema['fields'].items():
        if field_def.get('controlled_values'):
            if isinstance(field_def['controlled_values'], list):
                vocabularies[field_name] = field_def['controlled_values']
            else:
                # Reference to external file
                vocabularies[field_name] = f"See: {field_def['controlled_values']}"
    
    logger.info(f"Built {len(vocabularies)} vocabulary lists")
    return vocabularies


def generate_csv(flattened: List[Dict], output_path: str):
    """
    Generate CSV version of data dictionary.
    
    Args:
        flattened: List of flattened field definitions
        output_path: Output file path
    """
    logger.info(f"Generating CSV: {output_path}")
    
    df = pd.DataFrame(flattened)
    df.to_csv(output_path, index=False, encoding='utf-8-sig')
    
    logger.info(f"CSV written successfully: {len(df)} rows")


def generate_excel(flattened: List[Dict], vocabularies: Dict, output_path: str):
    """
    Generate Excel version with multiple sheets.
    
    Args:
        flattened: List of flattened field definitions
        vocabularies: Dictionary of controlled vocabularies
        output_path: Output file path
    """
    logger.info(f"Generating Excel: {output_path}")
    
    with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
        # Main dictionary sheet
        df = pd.DataFrame(flattened)
        df.to_excel(writer, sheet_name='Data Dictionary', index=False)
        
        # Vocabularies sheet
        if vocabularies:
            vocab_df = pd.DataFrame([
                {'Field': k, 'Controlled_Values': str(v)}
                for k, v in vocabularies.items()
            ])
            vocab_df.to_excel(writer, sheet_name='Controlled Vocabularies', index=False)
        
        # Field groups sheet (from schema)
        # TODO: Load from schema and add to workbook
        
    logger.info(f"Excel written successfully")


def generate_json(schema: Dict, flattened: List[Dict], output_path: str):
    """
    Generate JSON version of unified dictionary.
    
    Args:
        schema: Original canonical schema
        flattened: List of flattened field definitions
        output_path: Output file path
    """
    logger.info(f"Generating JSON: {output_path}")
    
    output = {
        'metadata': {
            'generated_at': datetime.now().isoformat(),
            'author': 'R. A. Carucci',
            'schema_version': schema.get('schema_version'),
            'total_fields': len(flattened)
        },
        'fields': flattened
    }
    
    with open(output_path, 'w') as f:
        json.dump(output, f, indent=2)
    
    logger.info(f"JSON written successfully")


def main():
    """Main execution function"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Build unified data dictionary')
    parser.add_argument('--schema', default='docs/schema/canonical_schema.json',
                       help='Path to canonical schema JSON')
    parser.add_argument('--output', default='docs/data_dictionary/',
                       help='Output directory')
    
    args = parser.parse_args()
    
    # Create output directory
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Load schema
    schema = load_canonical_schema(args.schema)
    
    # Flatten definitions
    flattened = flatten_field_definitions(schema)
    
    # Extract vocabularies
    vocabularies = build_vocabulary_lists(schema)
    
    # Generate outputs
    generate_csv(flattened, output_dir / 'unified_dictionary.csv')
    generate_excel(flattened, vocabularies, output_dir / 'unified_dictionary.xlsx')
    generate_json(schema, flattened, output_dir / 'unified_dictionary.json')
    
    logger.info("Dictionary generation complete!")
    logger.info(f"Outputs written to: {output_dir}")


if __name__ == "__main__":
    main()
