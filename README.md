# ScanSwarm

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Swarms](https://img.shields.io/badge/Swarms-Framework-orange.svg)](https://github.com/kyegomez/swarms)
[![Status: Alpha](https://img.shields.io/badge/Status-Alpha-red.svg)]()

A token analysis system built on the [Swarms Framework](https://github.com/kyegomez/swarms), utilizing multi-agent architecture for automated crypto token screening.

## Framework Integration
ScanSwarm leverages the Swarms Framework for:
- 🤖 Multi-Agent Orchestration
- 🔄 Sequential Workflows
- 📊 Distributed Analysis
- 🧠 Agent Communication

## Agent Architecture
Built using Swarms' agent patterns:
\\\python
from swarms import Agent, SequentialWorkflow

class NavigatorAgent(Agent):
    def __init__(self):
        super().__init__(
            agent_name="Navigator",
            system_prompt="Specialized navigation agent for token analysis",
            model_name="gpt-4"
        )
\\\

## Swarms Integration
- Uses Swarms' SequentialWorkflow for agent coordination
- Implements Swarms' Agent class for each specialized component
- Follows Swarms' communication patterns
- Leverages Swarms' error handling

## 📊 Implementation Status

### Core Components
\\\
NavigatorAgent    [███████░░░] 70%  ⚠️ Geo-restriction pending
ChartAnalyzer    [████░░░░░░] 40%  🔄 In Development
DataCollector    [░░░░░░░░░░] 0%   📝 Planned
RiskAssessor     [░░░░░░░░░░] 0%   📝 Planned
\\\

### Infrastructure
\\\
Project Structure    [██████████] 100%
Git Repository      [██████████] 100%
Configuration       [██████████] 100%
Test Framework      [██████████] 100%
Browser Automation  [██████████] 100%
\\\

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Git
- Playwright

### Installation
\\\ash
# Clone the repository
git clone https://github.com/Josiah-O/ScanSwarm.git

# Navigate to project directory
cd ScanSwarm

# Install dependencies
pip install -r requirements.txt

# Install playwright browsers
playwright install
\\\

### Configuration
1. Copy environment example:
\\\ash
cp .env.example .env
\\\

2. Update configuration in \.env\:
\\\env
OPENAI_API_KEY=your_key_here
SWARMS_API_KEY=your_key_here
\\\

## 💻 Usage
Basic implementation example:

\\\python
from src.orchestrator import ScanOrchestrator
from src.utils.browser import BrowserManager

async def analyze_token(token_address: str):
    # Initialize browser
    browser_manager = BrowserManager(headless=False)
    await browser_manager.initialize()

    # Create orchestrator
    orchestrator = ScanOrchestrator(browser_manager)

    # Analyze token
    result = await orchestrator.execute(token_address)
    return result
\\\

## 🤝 Contributing
We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

## 📜 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔗 Links
- [Swarms Framework](https://github.com/kyegomez/swarms)
- [Documentation](https://github.com/Josiah-O/ScanSwarm/wiki)
- [Issue Tracker](https://github.com/Josiah-O/ScanSwarm/issues)

---
<p align="center">
  Made with ❤️ by the ScanSwarm Team
</p>
