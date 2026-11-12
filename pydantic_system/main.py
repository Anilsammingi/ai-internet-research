
import asyncio

from pydantic_system.research_agent import research_agent


async def main():
    print("\n======================================")
    print("   PYDANTICAI INTERNET RESEARCH AGENT")
    print("======================================\n")

    query = input("Enter your research question: ").strip()

    if not query:
        print("Please enter a valid research question.")
        return

    print("\nResearching the internet... Please wait.\n")

    try:
        result = await research_agent.run(query)

        print("\n========== RESEARCH SUMMARY ==========\n")
        print(result.output)
        print("\n======================================\n")

    except Exception as error:
        print(f"\nResearch failed: {error}")


if __name__ == "__main__":
    asyncio.run(main())
