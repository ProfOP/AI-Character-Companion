from app.ai.gemini_client import client, MODEL_NAME


async def update_memory_summary(
    previous_summary: str,
    conversation: str,
) -> str:
    """
    Updates structured long-term memory using Gemini.
    """

    memory_prompt = f"""
You are maintaining a structured story memory.

Update the memory summary below based on the new conversation.

Keep it concise but information-dense.
Preserve:
- Key events
- Character relationships
- Emotional shifts
- Goals
- World state changes

=== PREVIOUS MEMORY ===
{previous_summary}

=== NEW CONVERSATION ===
{conversation}

Return ONLY the updated memory summary.
"""

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=memory_prompt,
    )

    return response.text
