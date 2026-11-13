# AI Internet Research Agent

An AI-powered Internet Research System built with **Python, PydanticAI, CrewAI, and Groq LLMs**.

The project aims to develop an autonomous Agentic AI research assistant capable of planning research, searching the internet, reading webpages, verifying information, analyzing findings, and generating structured research reports.

## Project Overview

The system currently provides two independent AI research implementations:

1. **PydanticAI Research Agent** – A single AI agent that accepts a research question, searches the internet using a custom search tool, and generates a research response.
2. **CrewAI Multi-Agent Research System** – A multi-agent workflow in which a Research Agent gathers information and a Summarizer Agent generates a structured research report.

The long-term goal is to evolve these implementations into a complete Agentic AI Research Platform.

## Architecture

```text
                 User Research Query
                         |
              +----------+----------+
              |                     |
        PydanticAI System       CrewAI System
              |                     |
         Research Agent        Research Agent
              |                     |
        Internet Search       Search & Web Reader
              |                     |
        Research Results      Research Findings
              |                     |
         AI Response          Summarizer Agent
                                    |
                              Research Report
```

## Implemented Features

- AI-powered internet research.
- PydanticAI single-agent implementation.
- CrewAI multi-agent workflow.
- Custom DuckDuckGo search integration using DDGS.
- Webpage content extraction using Trafilatura.
- Groq LLM integration.
- Structured research report generation.
- Source title and URL collection.
- Basic error handling.
- TLS certificate support for corporate network environments.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python 3.13 | Core programming language |
| PydanticAI | Structured AI agent development |
| CrewAI | Multi-agent orchestration |
| Groq | LLM inference |
| DDGS | Internet search |
| Requests | Webpage retrieval |
| Trafilatura | Webpage content extraction |
| Pydantic | Data validation |
| python-dotenv | Environment configuration |
| Pytest | Automated testing |

## Project Structure

```text
ai-internet-research/
│
├── crewai_system/
│   ├── agents.py
│   ├── crew.py
│   ├── main.py
│   ├── tasks.py
│   └── tools.py
│
├── pydantic_system/
│   ├── main.py
│   └── research_agent.py
│
├── tools/
│   ├── web_search_tool.py
│   └── webpage_reader.py
│
├── .env
├── .gitignore
└── README.md
```

## Prerequisites

- Python 3.13 or later.
- Git.
- Groq API key.

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/Anilsammingi/ai-internet-research.git
cd ai-internet-research
```

### 2. Create a virtual environment

```powershell
python -m venv .venv
```

### 3. Activate the virtual environment

```powershell
.venv\Scripts\Activate.ps1
```

### 4. Install dependencies

Install the packages used by the project:

```powershell
python -m pip install crewai pydantic-ai ddgs python-dotenv requests trafilatura beautifulsoup4 truststore
```

### 5. Configure environment variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key
```

Never commit your `.env` file or expose API keys publicly.

## Running the Application

### PydanticAI Research System

```powershell
python -m pydantic_system.main
```

### CrewAI Multi-Agent Research System

```powershell
python -m crewai_system.main
```

Enter a research question when prompted.

Example:

```text
What is Generative AI?
Explain its main applications and risks.
```

The CrewAI workflow will execute its research and summarization tasks and produce a structured report.

## Development Roadmap

The project is being developed incrementally toward a complete Agentic AI Research Platform.

- [x] PydanticAI research agent.
- [x] CrewAI multi-agent workflow.
- [x] Custom internet search tool.
- [x] Webpage content extraction.
- [x] Groq LLM integration.
- [ ] Improve research accuracy and source credibility.
- [ ] Autonomous research planning agent.
- [ ] Advanced multi-agent collaboration.
- [ ] Fact-checking and source verification.
- [ ] PDF and document research tools.
- [ ] Research memory and knowledge base.
- [ ] Autonomous research decisions and retries.
- [ ] Human-in-the-loop approval.
- [ ] PDF, Word and Excel report generation.
- [ ] FastAPI backend.
- [ ] Streamlit web interface.
- [ ] Production deployment and monitoring.

## Future Vision

The completed platform will aim to:

1. Understand complex research requests.
2. Generate autonomous research plans.
3. Delegate tasks to specialized AI agents.
4. Search and analyze multiple internet sources.
5. Verify important claims using supporting evidence.
6. Identify missing information and conduct additional research.
7. Generate detailed research reports with citations.
8. Store previous research for future retrieval.

## Security

- API keys are stored in environment variables.
- `.env` and `.venv` are excluded through `.gitignore`.
- Research sources should be treated as untrusted external content.
- Additional production security controls will be introduced as the platform evolves.

## Author

**Anil Sandy**

GitHub: https://github.com/Anilsammingi

## License

License to be determined.
