
import truststore
truststore.inject_into_ssl()

from crewai_system.crew import research_crew


def main():
    print("\n======================================")
    print("     CREWAI INTERNET RESEARCH SYSTEM")
    print("======================================\n")

    topic = input("Enter your research question: ").strip()

    if not topic:
        print("Please enter a valid research question.")
        return

    print("\nResearching the internet... Please wait.\n")

    try:
        result = research_crew.kickoff(
            inputs={"topic": topic}
        )

        print("\n========== FINAL RESEARCH REPORT ==========\n")
        print(result)
        print("\n===========================================\n")

    except Exception as error:
        print(f"\nResearch failed: {error}")


if __name__ == "__main__":
    main()

