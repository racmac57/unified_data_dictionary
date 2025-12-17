# // 2025-12-17-19-30-00
# // unified_dictionary_builder/extract_rules_from_repo.py
# // Author: R. A. Carucci
# // Purpose: Extract field validation rules, mappings, and vocab lists from CAD/RMS repos

"""
Extract Rules from Repository

Scans CAD and RMS repository codebases to extract:
- Field validation logic
- Controlled vocabulary lists
- Transformation patterns
- Data quality rules

Usage:
    python extract_rules_from_repo.py --cad-repo ../CAD_Data_Cleaning_Engine --rms-repo ../dv_doj
"""

import os
import re
import json
from pathlib import Path
from typing import Dict, List, Set
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class RuleExtractor:
    """Extract validation rules and patterns from repository code"""
    
    def __init__(self, repo_path: str):
        self.repo_path = Path(repo_path)
        self.rules = {
            'validation_patterns': [],
            'controlled_vocabularies': {},
            'field_mappings': {},
            'transformation_logic': []
        }
    
    def scan_python_files(self) -> List[Path]:
        """Find all Python files in repository"""
        logger.info(f"Scanning Python files in {self.repo_path}")
        
        py_files = list(self.repo_path.rglob('*.py'))
        logger.info(f"Found {len(py_files)} Python files")
        
        return py_files
    
    def extract_validation_patterns(self, file_path: Path):
        """Extract validation regex patterns from Python code"""
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Look for regex patterns
            regex_patterns = re.findall(r'r[\'"](.+?)[\'"]', content)
            
            for pattern in regex_patterns:
                if any(indicator in pattern for indicator in ['\\d', '\\w', '[', '^', '$']):
                    self.rules['validation_patterns'].append({
                        'pattern': pattern,
                        'source_file': str(file_path.relative_to(self.repo_path))
                    })
        
        except Exception as e:
            logger.warning(f"Error reading {file_path}: {e}")
    
    def extract_controlled_vocabularies(self, file_path: Path):
        """Extract lists of allowed values from code"""
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Look for list definitions that might be vocabularies
            list_patterns = [
                r'(\w+)\s*=\s*\[([\'\"].+?[\'\"],?\s*)+\]',  # Simple lists
                r'allowed_values\s*=\s*\{(.+?)\}',  # Dictionary of allowed values
            ]
            
            for pattern in list_patterns:
                matches = re.findall(pattern, content, re.MULTILINE | re.DOTALL)
                
                for match in matches:
                    # TODO: Parse and store vocabulary lists
                    pass
        
        except Exception as e:
            logger.warning(f"Error reading {file_path}: {e}")
    
    def extract_field_mappings(self, file_path: Path):
        """Extract field mapping dictionaries from code"""
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Look for dictionary definitions with field mappings
            mapping_pattern = r'(\w+_map|field_map)\s*=\s*\{(.+?)\}'
            
            matches = re.findall(mapping_pattern, content, re.MULTILINE | re.DOTALL)
            
            for var_name, mapping_content in matches:
                self.rules['field_mappings'][var_name] = {
                    'content': mapping_content[:200],  # Truncate for storage
                    'source_file': str(file_path.relative_to(self.repo_path))
                }
        
        except Exception as e:
            logger.warning(f"Error reading {file_path}: {e}")
    
    def extract_from_json_configs(self):
        """Extract rules from JSON configuration files"""
        
        json_files = list(self.repo_path.rglob('*.json'))
        logger.info(f"Found {len(json_files)} JSON files")
        
        for json_file in json_files:
            try:
                with open(json_file, 'r') as f:
                    config = json.load(f)
                
                # Check if it's a field map or schema
                if isinstance(config, dict):
                    if 'fields' in config or 'field_map' in config:
                        self.rules['field_mappings'][json_file.name] = config
            
            except Exception as e:
                logger.warning(f"Error reading {json_file}: {e}")
    
    def extract_from_csv_references(self):
        """Find CSV files that contain reference data"""
        
        csv_files = list(self.repo_path.rglob('*.csv'))
        logger.info(f"Found {len(csv_files)} CSV files")
        
        for csv_file in csv_files:
            # Check if it looks like a vocabulary or mapping file
            file_name = csv_file.name.lower()
            
            if any(keyword in file_name for keyword in ['vocab', 'values', 'types', 'codes', 'mapping']):
                self.rules['controlled_vocabularies'][csv_file.name] = {
                    'path': str(csv_file.relative_to(self.repo_path)),
                    'type': 'reference_csv'
                }
    
    def run_extraction(self):
        """Run all extraction methods"""
        
        logger.info(f"Starting rule extraction from {self.repo_path}")
        
        # Scan Python files
        py_files = self.scan_python_files()
        
        for py_file in py_files:
            self.extract_validation_patterns(py_file)
            self.extract_controlled_vocabularies(py_file)
            self.extract_field_mappings(py_file)
        
        # Scan JSON configs
        self.extract_from_json_configs()
        
        # Find reference CSVs
        self.extract_from_csv_references()
        
        logger.info("Extraction complete")
        
        return self.rules


def merge_extracted_rules(cad_rules: Dict, rms_rules: Dict) -> Dict:
    """
    Merge rules extracted from CAD and RMS repositories.
    
    Args:
        cad_rules: Rules from CAD repo
        rms_rules: Rules from RMS repo
        
    Returns:
        Merged rules dictionary
    """
    logger.info("Merging extracted rules")
    
    merged = {
        'cad': cad_rules,
        'rms': rms_rules,
        'statistics': {
            'cad_validation_patterns': len(cad_rules['validation_patterns']),
            'rms_validation_patterns': len(rms_rules['validation_patterns']),
            'cad_vocabularies': len(cad_rules['controlled_vocabularies']),
            'rms_vocabularies': len(rms_rules['controlled_vocabularies']),
            'cad_field_mappings': len(cad_rules['field_mappings']),
            'rms_field_mappings': len(rms_rules['field_mappings'])
        }
    }
    
    return merged


def main():
    """Main execution function"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Extract rules from repositories')
    parser.add_argument('--cad-repo', required=True,
                       help='Path to CAD repository')
    parser.add_argument('--rms-repo', required=True,
                       help='Path to RMS/DV repository')
    parser.add_argument('--output', default='docs/extracted_rules.json',
                       help='Output JSON file')
    
    args = parser.parse_args()
    
    # Extract from CAD repo
    cad_extractor = RuleExtractor(args.cad_repo)
    cad_rules = cad_extractor.run_extraction()
    
    # Extract from RMS repo
    rms_extractor = RuleExtractor(args.rms_repo)
    rms_rules = rms_extractor.run_extraction()
    
    # Merge results
    merged = merge_extracted_rules(cad_rules, rms_rules)
    
    # Write output
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w') as f:
        json.dump(merged, f, indent=2)
    
    logger.info(f"Extracted rules written to: {output_path}")
    logger.info(f"Statistics: {merged['statistics']}")


if __name__ == "__main__":
    main()
