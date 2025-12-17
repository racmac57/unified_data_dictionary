# 🕒 2025-12-17-19-38-00
# unified_data_dictionary/src/cli.py
# Author: R. A. Carucci
# Purpose: Command-line interface for unified data dictionary operations including extract, build, excel, and validate commands

import click
import logging
from pathlib import Path
from .extract_from_repos import RepoSchemaExtractor
from .build_dictionary import DictionaryBuilder
from .generate_excel_output import ExcelDictionaryGenerator

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)


@click.group()
@click.version_option(version='1.0.0')
def cli():
    """Unified Data Dictionary CLI - CAD/RMS/DV schema management."""
    pass


@cli.command()
@click.option(
    '--repos',
    '-r',
    multiple=True,
    help='Repository names to extract (default: all configured)'
)
@click.option(
    '--output-dir',
    '-o',
    type=click.Path(),
    default='schemas',
    help='Output directory for extracted schemas'
)
def extract(repos, output_dir):
    """Extract schemas from Git repositories."""
    click.echo("🔍 Extracting schemas from repositories...")
    
    output_path = Path(output_dir)
    extractor = RepoSchemaExtractor(output_dir=output_path)
    
    repo_list = list(repos) if repos else None
    extractor.extract_all(repo_names=repo_list)
    extractor.save_extracted_schemas()
    
    summary = extractor.generate_summary()
    
    click.echo(f"\n✅ Extraction complete!")
    click.echo(f"   Repositories: {summary['repositories_processed']}")
    click.echo(f"   Total schemas: {summary['total_schemas']}")
    

@cli.command()
@click.option(
    '--schemas-dir',
    '-s',
    type=click.Path(exists=True),
    default='schemas',
    help='Directory containing extracted schemas'
)
@click.option(
    '--output',
    '-o',
    type=click.Path(),
    default='output/unified_data_dictionary.json',
    help='Output path for dictionary JSON'
)
def build(schemas_dir, output):
    """Build unified canonical dictionary."""
    click.echo("🔨 Building unified data dictionary...")
    
    builder = DictionaryBuilder(schemas_dir=Path(schemas_dir))
    dictionary = builder.build_canonical_dictionary()
    builder.save_dictionary(dictionary, Path(output))
    
    stats = builder.generate_statistics(dictionary)
    
    click.echo(f"\n✅ Dictionary built successfully!")
    click.echo(f"   Total fields: {stats['total_fields']}")
    click.echo(f"   Required fields: {stats['required_fields']}")
    click.echo(f"   PII fields: {stats['pii_fields']}")
    

@cli.command()
@click.option(
    '--input',
    '-i',
    type=click.Path(exists=True),
    default='output/unified_data_dictionary.json',
    help='Input JSON dictionary file'
)
@click.option(
    '--output',
    '-o',
    type=click.Path(),
    default='output/unified_data_dictionary.xlsx',
    help='Output Excel file'
)
def excel(input, output):
    """Generate Excel documentation from dictionary."""
    click.echo("📊 Generating Excel documentation...")
    
    generator = ExcelDictionaryGenerator()
    generator.generate(Path(input), Path(output))
    
    click.echo(f"\n✅ Excel file generated: {output}")
    

@cli.command()
@click.option(
    '--input',
    '-i',
    type=click.Path(exists=True),
    default='output/unified_data_dictionary.json',
    help='Dictionary JSON file to validate'
)
@click.option(
    '--strict',
    is_flag=True,
    help='Enable strict validation mode'
)
def validate(input, strict):
    """Validate dictionary mappings and consistency."""
    click.echo("🔍 Validating dictionary...")
    
    import json
    
    with open(input, 'r') as f:
        dictionary = json.load(f)
        
    issues = []
    
    # Check for duplicate field names
    field_names = list(dictionary['fields'].keys())
    if len(field_names) != len(set(field_names)):
        issues.append("❌ Duplicate field names detected")
        
    # Check for missing required attributes
    for field_name, field_def in dictionary['fields'].items():
        if not field_def.get('data_type'):
            issues.append(f"❌ {field_name}: Missing data_type")
        if not field_def.get('description') and strict:
            issues.append(f"⚠️  {field_name}: Missing description")
            
    # Check for unresolved conflicts
    if dictionary.get('conflicts'):
        issues.append(f"⚠️  {len(dictionary['conflicts'])} conflicts detected")
        
    if issues:
        click.echo("\n⚠️  Validation issues found:")
        for issue in issues:
            click.echo(f"   {issue}")
        if strict:
            raise click.ClickException("Validation failed in strict mode")
    else:
        click.echo("\n✅ Dictionary validation passed!")
        

@cli.command()
@click.option(
    '--repos',
    '-r',
    multiple=True,
    help='Repositories to process'
)
@click.option(
    '--output-dir',
    '-o',
    type=click.Path(),
    default='output',
    help='Output directory'
)
def all(repos, output_dir):
    """Run complete pipeline: extract → build → excel."""
    click.echo("🚀 Running full dictionary pipeline...\n")
    
    # Extract
    click.echo("Step 1/3: Extracting schemas")
    ctx = click.get_current_context()
    ctx.invoke(extract, repos=repos, output_dir='schemas')
    
    # Build
    click.echo("\nStep 2/3: Building dictionary")
    output_json = Path(output_dir) / 'unified_data_dictionary.json'
    ctx.invoke(build, schemas_dir='schemas', output=str(output_json))
    
    # Excel
    click.echo("\nStep 3/3: Generating Excel")
    output_excel = Path(output_dir) / 'unified_data_dictionary.xlsx'
    ctx.invoke(excel, input=str(output_json), output=str(output_excel))
    
    click.echo("\n🎉 Full pipeline complete!")
    

@cli.command()
def info():
    """Display dictionary statistics and metadata."""
    dict_path = Path('output/unified_data_dictionary.json')
    
    if not dict_path.exists():
        click.echo("❌ Dictionary not found. Run 'build' first.")
        return
        
    import json
    with open(dict_path, 'r') as f:
        dictionary = json.load(f)
        
    metadata = dictionary['metadata']
    
    click.echo("\n📊 Dictionary Information")
    click.echo("=" * 50)
    click.echo(f"Version:        {metadata['version']}")
    click.echo(f"Generated:      {metadata['generated_at']}")
    click.echo(f"Total Fields:   {metadata['total_fields']}")
    click.echo(f"Source Systems: {', '.join(metadata['source_systems'])}")
    click.echo(f"Conflicts:      {metadata['conflicts_resolved']}")
    

if __name__ == '__main__':
    cli()
