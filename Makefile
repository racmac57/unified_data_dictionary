# Unified Dictionary Framework - Makefile
# Author: R. A. Carucci
# Purpose: Build automation for unified data dictionary

.PHONY: all clean build extract validate benchmark test lint typecheck help

# Default target
all: build

help:
	@echo "Unified Dictionary Framework - Available Targets:"
	@echo ""
	@echo "  make build         - Generate unified dictionary from schema"
	@echo "  make extract       - Extract rules from CAD/RMS repositories"
	@echo "  make validate      - Run validation checks"
	@echo "  make benchmark     - Run validation performance benchmarks"
	@echo "  make test          - Run unit tests"
	@echo "  make lint          - Run code linting (ruff)"
	@echo "  make typecheck     - Run type checking (mypy)"
	@echo "  make clean         - Remove generated files"
	@echo "  make all           - Run full build pipeline"
	@echo ""

# Install dependencies
install:
	pip install -r requirements.txt

# Generate unified dictionary
build:
	@echo "Building unified data dictionary..."
	python unified_dictionary_builder/build_dictionary.py \
		--schema docs/schema/canonical_schema.json \
		--output docs/data_dictionary/

# Extract rules from repositories
extract:
	@echo "Extracting rules from repositories..."
	python unified_dictionary_builder/extract_rules_from_repo.py \
		--cad-repo ../CAD_Data_Cleaning_Engine \
		--rms-repo ../dv_doj \
		--output docs/extracted_rules.json

# Validate data dictionary
validate:
	@echo "Validating data dictionary..."
	python unified_dictionary_builder/build_dictionary.py --validate

# Run validation benchmarks
benchmark:
	@echo "Running validation benchmarks..."
	python unified_dictionary_builder/run_validation_benchmarks.py \
		--engine pandas_parallel \
		--workers 4 \
		--chunk-size 10000 \
		--dataset-size 100000

# Run unit tests
test:
	@echo "Running unit tests..."
	pytest __tests__/ -v --tb=short

# Run code linting
lint:
	@echo "Running code linting..."
	ruff check unified_dictionary_builder/ __tests__/

# Run type checking
typecheck:
	@echo "Running type checking..."
	mypy unified_dictionary_builder/ --ignore-missing-imports

# Clean generated files
clean:
	@echo "Cleaning generated files..."
	rm -rf docs/data_dictionary/*.csv
	rm -rf docs/data_dictionary/*.xlsx
	rm -rf docs/data_dictionary/*.json
	rm -rf docs/benchmarks/*.json
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

# Full pipeline
pipeline: clean extract build test benchmark
	@echo "Full pipeline complete!"

# Quick quality check
qa: lint typecheck test
	@echo "Quality assurance checks complete!"
