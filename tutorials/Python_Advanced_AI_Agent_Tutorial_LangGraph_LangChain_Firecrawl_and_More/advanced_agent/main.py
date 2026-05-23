from pathlib import Path

from dotenv import load_dotenv
from src.workflow import Workflow

_AGENT_ROOT = Path(__file__).resolve().parent
_TUTORIAL_ROOT = _AGENT_ROOT.parent


def _load_env() -> None:
    for env_dir in (_AGENT_ROOT, _TUTORIAL_ROOT / "simple-agent"):
        load_dotenv(env_dir / "openai.env")
        load_dotenv(env_dir / "firecrawl.env")


def main():
    _load_env()
    workflow = Workflow()
    print("Developer Tools Research Agent")

    while True:
        try:
            query = input("\nDeveloper Tools Query: ").strip()
        except EOFError:
            break
        if query.lower() in {"quit", "exit"}:
            break

        if query:
            result = workflow.run(query)
            print(f"\nResults for: {query}")
            print("=" * 60)

            for i, company in enumerate(result.companies, 1):
                print(f"\n{i}. {company.name}")
                print(f"   Website: {company.website}")
                print(f"   Pricing: {company.pricing_model}")
                print(f"   Open Source: {company.is_open_source}")

                if company.tech_stack:
                    print(f"   Tech Stack: {', '.join(company.tech_stack[:5])}")

                if company.language_support:
                    print(
                        f"   Language Support: {', '.join(company.language_support[:5])}"
                    )

                if company.api_available is not None:
                    api_status = (
                        "Available" if company.api_available else "Not Available"
                    )
                    print(f"   API: {api_status}")

                if company.integration_capabilities:
                    print(
                        f"   Integrations: {', '.join(company.integration_capabilities[:4])}"
                    )

                if company.description and company.description != "Analysis failed":
                    print(f"   Description: {company.description}")

                print()

            if result.analysis:
                print("Developer Recommendations: ")
                print("-" * 40)
                print(result.analysis)


if __name__ == "__main__":
    main()
