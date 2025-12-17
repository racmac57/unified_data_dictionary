# 🕒 2025-12-17-19-32-00
# unified_data_dictionary/src/extract_from_repos.py
# Author: R. A. Carucci
# Purpose: Extract schema definitions, field mappings, and validation rules from existing CAD/RMS/DV repositories for dictionary consolidation

import json
import logging
from pathlib import Path
from typing import Dict, List, Any
import subprocess
import tempfile
import shutil

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RepoSchemaExtractor:
    """Extract schemas and mappings from existing Git repositories."""
    
    REPO_CONFIGS = {
        'dv_doj': {
            'url': 'https://github.com/racmac57/dv_doj.git',
            'schema_paths': [
                'data_dictionary.md',
                'docs/PII_POLICY.md',
                'processed_data/*.json'
            ],
            'field_prefix': 'DV_'
        },
        'CAD_Data_Cleaning_Engine': {
            'url': 'https://github.com/racmac57/CAD_Data_Cleaning_Engine.git',
            'schema_paths': [
                'cad_field_map.json',
                'rms_field_map.json',
                'cad_fields_schema.json',
                'rms_fields_schema.json',
                'cad_to_rms_field_map.json',
                'rms_to_cad_field_map.json'
            ],
            'field_prefix': 'CAD_'
        }
    }
    
    def __init__(self, output_dir: Path = Path("schemas")):
        """Initialize extractor with output directory."""
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.extracted_schemas = {}
        
    def clone_repo(self, repo_name: str, temp_dir: Path) -> Path:
        """Clone repository to temporary directory."""
        config = self.REPO_CONFIGS.get(repo_name)
        if not config:
            raise ValueError(f"Unknown repository: {repo_name}")
            
        repo_url = config['url']
        target_path = temp_dir / repo_name
        
        logger.info(f"Cloning {repo_name} from {repo_url}")
        
        try:
            subprocess.run(
                ['git', 'clone', '--depth', '1', repo_url, str(target_path)],
                check=True,
                capture_output=True,
                text=True
            )
            logger.info(f"Successfully cloned {repo_name}")
            return target_path
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to clone {repo_name}: {e.stderr}")
            raise
            
    def extract_json_schemas(self, repo_path: Path, schema_paths: List[str]) -> Dict[str, Any]:
        """Extract JSON schema files from repository."""
        schemas = {}
        
        for pattern in schema_paths:
            if pattern.endswith('.json'):
                # Direct JSON files
                json_files = list(repo_path.glob(pattern))
                for json_file in json_files:
                    try:
                        with open(json_file, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                            schemas[json_file.name] = data
                            logger.info(f"Extracted {json_file.name}")
                    except Exception as e:
                        logger.warning(f"Failed to parse {json_file}: {e}")
                        
        return schemas
        
    def extract_markdown_tables(self, repo_path: Path, md_paths: List[str]) -> Dict[str, List[Dict]]:
        """Extract field definitions from markdown tables."""
        md_schemas = {}
        
        for pattern in md_paths:
            if pattern.endswith('.md'):
                md_files = list(repo_path.glob(pattern))
                for md_file in md_files:
                    try:
                        fields = self._parse_markdown_table(md_file)
                        if fields:
                            md_schemas[md_file.name] = fields
                            logger.info(f"Extracted {len(fields)} fields from {md_file.name}")
                    except Exception as e:
                        logger.warning(f"Failed to parse {md_file}: {e}")
                        
        return md_schemas
        
    def _parse_markdown_table(self, md_file: Path) -> List[Dict]:
        """Parse markdown table into structured field definitions."""
        fields = []
        
        with open(md_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
        in_table = False
        headers = []
        
        for line in lines:
            line = line.strip()
            
            # Detect table start
            if '|' in line and not in_table:
                headers = [h.strip() for h in line.split('|') if h.strip()]
                in_table = True
                continue
                
            # Skip separator row
            if in_table and set(line.replace(' ', '')) <= {'|', '-'}:
                continue
                
            # Parse table rows
            if in_table and '|' in line:
                values = [v.strip() for v in line.split('|') if v.strip()]
                
                if len(values) >= len(headers):
                    field_dict = dict(zip(headers, values))
                    fields.append(field_dict)
                    
            # End of table
            elif in_table and '|' not in line:
                in_table = False
                headers = []
                
        return fields
        
    def normalize_schema(self, raw_schema: Dict, field_prefix: str) -> Dict[str, Dict]:
        """Normalize extracted schema to canonical format."""
        normalized = {}
        
        for field_name, field_info in raw_schema.items():
            if isinstance(field_info, dict):
                canonical_name = f"{field_prefix}{field_name}"
                
                normalized[canonical_name] = {
                    'source_name': field_name,
                    'data_type': field_info.get('type', 'string'),
                    'description': field_info.get('description', ''),
                    'required': field_info.get('required', False),
                    'example': field_info.get('example'),
                    'constraints': field_info.get('constraints', {}),
                    'source_system': field_prefix.rstrip('_')
                }
                
        return normalized
        
    def extract_from_repo(self, repo_name: str) -> Dict[str, Any]:
        """Extract all schemas from a repository."""
        config = self.REPO_CONFIGS[repo_name]
        
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            # Clone repository
            repo_path = self.clone_repo(repo_name, temp_path)
            
            # Extract JSON schemas
            json_schemas = self.extract_json_schemas(repo_path, config['schema_paths'])
            
            # Extract markdown tables
            md_schemas = self.extract_markdown_tables(repo_path, config['schema_paths'])
            
            # Combine and normalize
            all_schemas = {**json_schemas, **md_schemas}
            
            self.extracted_schemas[repo_name] = all_schemas
            
        return all_schemas
        
    def extract_all(self, repo_names: List[str] = None) -> Dict[str, Dict]:
        """Extract schemas from all configured repositories."""
        if repo_names is None:
            repo_names = list(self.REPO_CONFIGS.keys())
            
        logger.info(f"Extracting schemas from {len(repo_names)} repositories")
        
        for repo_name in repo_names:
            try:
                schemas = self.extract_from_repo(repo_name)
                logger.info(f"Extracted {len(schemas)} schemas from {repo_name}")
            except Exception as e:
                logger.error(f"Failed to extract from {repo_name}: {e}")
                
        return self.extracted_schemas
        
    def save_extracted_schemas(self):
        """Save extracted schemas to output directory."""
        for repo_name, schemas in self.extracted_schemas.items():
            output_file = self.output_dir / f"{repo_name}_extracted.json"
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(schemas, f, indent=2, ensure_ascii=False)
                
            logger.info(f"Saved {repo_name} schemas to {output_file}")
            
    def generate_summary(self) -> Dict[str, Any]:
        """Generate summary statistics of extraction."""
        summary = {
            'repositories_processed': len(self.extracted_schemas),
            'total_schemas': sum(len(s) for s in self.extracted_schemas.values()),
            'by_repository': {}
        }
        
        for repo_name, schemas in self.extracted_schemas.items():
            summary['by_repository'][repo_name] = {
                'schema_count': len(schemas),
                'schema_files': list(schemas.keys())
            }
            
        return summary


def main():
    """Main extraction workflow."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Extract schemas from Git repositories")
    parser.add_argument(
        '--repos',
        nargs='+',
        default=None,
        help='Repository names to extract (default: all)'
    )
    parser.add_argument(
        '--output-dir',
        type=Path,
        default=Path('schemas'),
        help='Output directory for extracted schemas'
    )
    
    args = parser.parse_args()
    
    # Run extraction
    extractor = RepoSchemaExtractor(output_dir=args.output_dir)
    extractor.extract_all(repo_names=args.repos)
    extractor.save_extracted_schemas()
    
    # Generate summary
    summary = extractor.generate_summary()
    
    summary_file = args.output_dir / 'extraction_summary.json'
    with open(summary_file, 'w') as f:
        json.dump(summary, f, indent=2)
        
    logger.info(f"Extraction complete. Summary: {summary}")
    logger.info(f"Total schemas extracted: {summary['total_schemas']}")
    

if __name__ == '__main__':
    main()
