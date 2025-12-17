# // 2025-12-17-19-30-00
# // unified_dictionary_builder/run_validation_benchmarks.py
# // Author: R. A. Carucci
# // Purpose: Benchmark validation performance with different parallelization strategies

"""
Run Validation Benchmarks

Tests validation performance using different engines and parallelization strategies.

Usage:
    python run_validation_benchmarks.py --engine pandas --workers 4 --chunk-size 10000
    python run_validation_benchmarks.py --engine polars --workers 8
"""

import time
import json
import pandas as pd
import numpy as np
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor
from datetime import datetime
from typing import Dict, List
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def generate_test_data(n_records: int = 100000) -> pd.DataFrame:
    """
    Generate synthetic test data for benchmarking.
    
    Args:
        n_records: Number of test records to generate
        
    Returns:
        Test DataFrame
    """
    logger.info(f"Generating {n_records:,} test records")
    
    np.random.seed(42)
    
    data = {
        'ReportNumberNew': [f"{np.random.randint(19, 26):02d}-{np.random.randint(1, 999999):06d}" 
                           for _ in range(n_records)],
        'Incident': np.random.choice(['ASSAULT', 'BURGLARY', 'MVA', 'THEFT'], n_records),
        'FullAddress2': [f"{np.random.randint(1, 999)} MAIN STREET" for _ in range(n_records)],
        'TimeOfCall': pd.date_range('2024-01-01', periods=n_records, freq='5min'),
        'TimeDispatched': pd.date_range('2024-01-01 00:02:00', periods=n_records, freq='5min'),
        'HowReported': np.random.choice(['9-1-1', 'Phone', 'Walk-in'], n_records),
        'Disposition': np.random.choice(['Report Taken', 'GOA', 'Arrest Made'], n_records),
        'PDZone': np.random.choice(['Z1', 'Z2', 'Z3', 'Z4'], n_records)
    }
    
    df = pd.DataFrame(data)
    logger.info("Test data generated")
    
    return df


def validate_chunk_pandas(chunk: pd.DataFrame) -> Dict:
    """
    Validate a chunk of data using pandas operations.
    
    Args:
        chunk: DataFrame chunk to validate
        
    Returns:
        Validation results dictionary
    """
    errors = []
    
    # Case number format
    invalid_case = ~chunk['ReportNumberNew'].str.match(r'^\d{2}-\d{6}$', na=False)
    errors.extend([('case_number_format', i) for i in chunk[invalid_case].index])
    
    # Time sequence
    invalid_time = chunk['TimeDispatched'] < chunk['TimeOfCall']
    errors.extend([('time_sequence', i) for i in chunk[invalid_time].index])
    
    # Address completeness
    invalid_addr = chunk['FullAddress2'].str.len() < 5
    errors.extend([('address_incomplete', i) for i in chunk[invalid_addr].index])
    
    # Controlled vocabulary
    valid_zones = ['Z1', 'Z2', 'Z3', 'Z4', 'UNK']
    invalid_zone = ~chunk['PDZone'].isin(valid_zones)
    errors.extend([('invalid_zone', i) for i in chunk[invalid_zone].index])
    
    return {
        'total_records': len(chunk),
        'error_count': len(errors),
        'errors': errors
    }


def validate_vectorized_pandas(df: pd.DataFrame) -> Dict:
    """
    Validate entire DataFrame using vectorized pandas operations.
    
    Args:
        df: DataFrame to validate
        
    Returns:
        Validation results dictionary
    """
    start_time = time.time()
    
    # Vectorized validations
    errors = {}
    
    # Case number format
    invalid_case = ~df['ReportNumberNew'].str.match(r'^\d{2}-\d{6}$', na=False)
    errors['case_number_format'] = df[invalid_case].index.tolist()
    
    # Time sequence
    invalid_time = df['TimeDispatched'] < df['TimeOfCall']
    errors['time_sequence'] = df[invalid_time].index.tolist()
    
    # Address completeness
    invalid_addr = df['FullAddress2'].str.len() < 5
    errors['address_incomplete'] = df[invalid_addr].index.tolist()
    
    # Controlled vocabulary
    valid_zones = ['Z1', 'Z2', 'Z3', 'Z4', 'UNK']
    invalid_zone = ~df['PDZone'].isin(valid_zones)
    errors['invalid_zone'] = df[invalid_zone].index.tolist()
    
    elapsed = time.time() - start_time
    
    total_errors = sum(len(v) for v in errors.values())
    
    return {
        'total_records': len(df),
        'error_count': total_errors,
        'errors_by_type': {k: len(v) for k, v in errors.items()},
        'elapsed_seconds': elapsed
    }


def validate_parallel_pandas(df: pd.DataFrame, n_workers: int, chunk_size: int) -> Dict:
    """
    Validate DataFrame using parallel processing with ProcessPoolExecutor.
    
    Args:
        df: DataFrame to validate
        n_workers: Number of worker processes
        chunk_size: Size of each chunk
        
    Returns:
        Validation results dictionary
    """
    start_time = time.time()
    
    logger.info(f"Starting parallel validation with {n_workers} workers, chunk size {chunk_size}")
    
    # Split dataframe into chunks
    chunks = [df[i:i+chunk_size] for i in range(0, len(df), chunk_size)]
    logger.info(f"Split data into {len(chunks)} chunks")
    
    # Process chunks in parallel
    all_errors = []
    
    with ProcessPoolExecutor(max_workers=n_workers) as executor:
        results = list(executor.map(validate_chunk_pandas, chunks))
    
    # Merge results
    total_errors = sum(r['error_count'] for r in results)
    
    elapsed = time.time() - start_time
    
    return {
        'total_records': len(df),
        'error_count': total_errors,
        'chunks_processed': len(chunks),
        'elapsed_seconds': elapsed,
        'records_per_second': len(df) / elapsed if elapsed > 0 else 0
    }


def run_benchmark(engine: str, df: pd.DataFrame, workers: int, chunk_size: int) -> Dict:
    """
    Run validation benchmark with specified configuration.
    
    Args:
        engine: Validation engine ('pandas', 'pandas_parallel', 'polars')
        df: Test DataFrame
        workers: Number of parallel workers
        chunk_size: Chunk size for parallel processing
        
    Returns:
        Benchmark results dictionary
    """
    logger.info(f"Running benchmark: engine={engine}, workers={workers}, chunk_size={chunk_size}")
    
    if engine == 'pandas':
        result = validate_vectorized_pandas(df)
    elif engine == 'pandas_parallel':
        result = validate_parallel_pandas(df, workers, chunk_size)
    elif engine == 'polars':
        # TODO: Implement polars validation
        logger.warning("Polars engine not yet implemented")
        result = {'error': 'not_implemented'}
    else:
        raise ValueError(f"Unknown engine: {engine}")
    
    result['engine'] = engine
    result['workers'] = workers
    result['chunk_size'] = chunk_size
    result['dataset_size'] = len(df)
    
    logger.info(f"Benchmark complete: {result.get('records_per_second', 0):.0f} records/sec")
    
    return result


def main():
    """Main execution function"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Run validation benchmarks')
    parser.add_argument('--engine', default='pandas',
                       choices=['pandas', 'pandas_parallel', 'polars'],
                       help='Validation engine to use')
    parser.add_argument('--workers', type=int, default=4,
                       help='Number of parallel workers')
    parser.add_argument('--chunk-size', type=int, default=10000,
                       help='Chunk size for parallel processing')
    parser.add_argument('--dataset-size', type=int, default=100000,
                       help='Number of records to generate for testing')
    parser.add_argument('--output', default='docs/benchmarks/benchmark_results.json',
                       help='Output file for results')
    
    args = parser.parse_args()
    
    # Generate test data
    df = generate_test_data(args.dataset_size)
    
    # Run benchmark
    result = run_benchmark(args.engine, df, args.workers, args.chunk_size)
    
    # Add metadata
    result['timestamp'] = datetime.now().isoformat()
    result['test_configuration'] = {
        'engine': args.engine,
        'workers': args.workers,
        'chunk_size': args.chunk_size,
        'dataset_size': args.dataset_size
    }
    
    # Write results
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w') as f:
        json.dump(result, f, indent=2)
    
    logger.info(f"Results written to: {output_path}")
    
    # Print summary
    print("\n" + "="*60)
    print("BENCHMARK RESULTS")
    print("="*60)
    print(f"Engine: {result['engine']}")
    print(f"Dataset Size: {result['dataset_size']:,} records")
    print(f"Workers: {result['workers']}")
    print(f"Chunk Size: {result['chunk_size']:,}")
    print(f"Elapsed Time: {result['elapsed_seconds']:.2f} seconds")
    print(f"Records/Second: {result.get('records_per_second', 0):,.0f}")
    print(f"Total Errors: {result['error_count']:,}")
    print("="*60)


if __name__ == "__main__":
    main()
