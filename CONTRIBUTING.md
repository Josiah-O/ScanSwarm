# Contributing to ScanSwarm

## Development Setup
1. Fork the repository
2. Create a virtual environment:
\\\ash
python -m venv venv
source venv/bin/activate  # Linux/Mac
.\\venv\\Scripts\\activate  # Windows
\\\

3. Install dependencies:
\\\ash
pip install -r requirements.txt
playwright install
\\\

## Current Development Focus
1. NavigatorAgent
   - Implementing geo-restriction bypass
   - Optimizing screenshot capture

2. ChartAnalyzerAgent
   - Pattern detection implementation
   - Volume analysis testing

3. Infrastructure
   - Error handling improvements
   - Logging enhancements

## Running Tests
\\\ash
python -m pytest src/test_scan.py -v -s
\\\

## Pull Request Guidelines
1. Update documentation
2. Add/update tests
3. Follow existing code style
4. Update requirements.txt if needed

## Project Structure
See README.md for current project structure and status
