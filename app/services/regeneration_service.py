from app.ai.gemini_client import client, MODEL_NAME


async def regenerate_response(
    character_prompt: str,
    memory_summary: str,
    conversation: str,
    last_assistant_reply: str,
    tone_instruction: str = "",
) -> str:

    rewrite_prompt = f"""
You are rewriting the LAST assistant response in a roleplay conversation.

DO NOT change story facts.
DO NOT contradict memory.
Preserve continuity.

If tone instruction is provided, apply it.
Otherwise generate a natural alternative variation.

=== CHARACTER PROFILE ===
{character_prompt}

=== LONG TERM MEMORY ===
{memory_summary}

=== FULL CONVERSATION ===
{conversation}

=== LAST ASSISTANT RESPONSE TO REWRITE ===
{last_assistant_reply}

=== TONE / SCENARIO INSTRUCTION ===
{tone_instruction}

Rewrite the last assistant response only.
Follow formatting protocol strictly.
Return only the rewritten response.
"""

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=rewrite_prompt,
    )

    return response.text
