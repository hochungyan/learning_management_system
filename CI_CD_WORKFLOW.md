CI/CD Workflow
Overview
This project employs a comprehensive CI/CD pipeline using GitHub Actions. The pipeline includes the following stages:
Setup

Checkout code
Set up Python environment
Install dependencies

Code Quality

Run linters with flake8
Execute pre-commit hooks
Perform Sourcery code quality check

Testing

Run tests with pytest
Generate coverage report with coverage.py
Upload coverage to Codecov

Security Analysis

Perform CodeQL analysis for security vulnerabilities

Deployment

Deploy to production on successful builds from the main branch

Workflow File
yamlCopyname: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]
  schedule:
    - cron: '0 1 * * 3'  # Every Wednesday at 1:00 AM

permissions:
  contents: write
  security-events: write

jobs:
  setup:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install -r backend/requirements.txt
          pip install flake8 pre-commit coverage pytest pytest-django pytest-cov sourcery-cli

  code_quality:
    runs-on: ubuntu-latest
    needs: setup
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'

      - name: Run linters
        run: flake8 .

      - name: Run pre-commit hooks
        run: pre-commit run --all-files

      - name: Run Sourcery
        env:
          SOURCERY_TOKEN: ${{ secrets.SOURCERY_TOKEN }}
        run: |
          sourcery login --token $SOURCERY_TOKEN
          if [ "${{ github.event_name }}" == "pull_request" ]; then
            sourcery review --check --diff "origin/${{ github.base_ref }}..HEAD" .
          else
            sourcery review --check .
          fi

  tests:
    runs-on: ubuntu-latest
    needs: setup
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'

      - name: Run tests with coverage
        run: |
          coverage run -m pytest
          coverage xml

      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v3
        with:
          file: coverage.xml

  codeql_analysis:
    runs-on: ubuntu-latest
    needs: setup
    steps:
      - name: Checkout repository
        uses: actions/checkout@v3

      - name: Initialize CodeQL
        uses: github/codeql-action/init@v2
        with:
          languages: python

      - name: Autobuild
        uses: github/codeql-action/autobuild@v2

      - name: Perform CodeQL Analysis
        uses: github/codeql-action/analyze@v2

  deploy:
    runs-on: ubuntu-latest
    needs: [tests, code_quality, codeql_analysis]
    if: github.ref == 'refs/heads/main'
    steps:
      - name: Deploy to Production
        run: echo "Deploying to production..."
        # Add your deployment steps here
