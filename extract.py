"""Demo: extract structured data from sample texts."""
import os
from schemas.common import SentimentResult, EntityList, MeetingNotes

SAMPLES = {
    "sentiment": "The new laptop is absolutely incredible — the battery lasts 18 hours and the display is gorgeous. However, the keyboard feels a bit mushy and it runs hot under load.",
    "entities": "Satya Nadella announced at Microsoft's Build conference in Seattle on May 21 that Azure OpenAI Service now supports GPT-4o and Claude 3.5 Sonnet.",
    "meeting": """Q3 Planning Meeting - Oct 14, 2024. Attendees: Sarah Chen, Marcus Webb, Priya Patel.
Decisions: Launch v2.0 in November. Hire 3 ML engineers. Cut infrastructure costs 20%.
Action items: Sarah to finalize roadmap by Oct 21. Marcus to post job reqs this week.
Open questions: Should we support GCP in addition to Azure?""",
}

def main():
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("Set ANTHROPIC_API_KEY to run live extraction.")
        print("\nSchemas available:")
        for schema in [SentimentResult, EntityList, MeetingNotes]:
            print(f"  {schema.__name__}: {list(schema.model_fields.keys())}")
        return

    from extractors.tool_extractor import extract
    print("Extracting sentiment...")
    sentiment = extract(SAMPLES["sentiment"], SentimentResult)
    print(f"  Label: {sentiment.label} ({sentiment.score:.2f})")
    print(f"  Reasoning: {sentiment.reasoning}")

    print("\nExtracting entities...")
    entities = extract(SAMPLES["entities"], EntityList)
    print(f"  People: {entities.people}")
    print(f"  Orgs: {entities.organizations}")

    print("\nExtracting meeting notes...")
    notes = extract(SAMPLES["meeting"], MeetingNotes)
    print(f"  Decisions: {notes.decisions}")
    print(f"  Action items: {notes.action_items}")

if __name__ == "__main__":
    main()
