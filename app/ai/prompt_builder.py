from typing import List, Dict, Optional


def build_prompt(
    character_prompt: str,
    messages: List[Dict],
    world_state: str = "",
    memory_summary: str = "",
    regeneration_instruction: str = "",
    style_config: Optional[dict] = None,
) -> str:

    """
    Builds a structured prompt for persona-based conversation.
    """

    core_rules = """
You are roleplaying as the character described below.

ABSOLUTE RULES:
- Never break character.
- Never mention being an AI.
- Never provide disclaimers.
- Stay immersive and narrative.

FORMATTING PROTOCOL (STRICT):

1. All physical actions, expressions, environment descriptions, and internal thoughts
   MUST be written as narration wrapped in single asterisks.
   Example:
   *She folds her arms slowly, watching you carefully.*

2. All spoken dialogue MUST:
   - Be plain text
   - Have NO quotation marks
   - NOT be wrapped in asterisks

3. Narration and dialogue MUST NEVER appear in the same paragraph.

4. Alternate between narration and dialogue where appropriate.
   Do not combine them in one block.

5. Separate each block with a blank line.

6. Keep formatting clean and readable.

7. If formatting rules are violated, regenerate internally and fix before output.

STRUCTURE EXPECTATION:
*Narration*

Dialogue

*Narration*

Dialogue

Respond in immersive long-form style while respecting formatting strictly.
"""

    # 🔥 STYLE CONTROL BLOCK (NEW)
    style_block = ""

    if style_config:
        tone = style_config.get("tone")
        intensity = style_config.get("intensity")
        style = style_config.get("style")

        style_block = f"""
=== STYLE CONTROL ===
Tone: {tone if tone else "default"}
Intensity: {intensity if intensity else "medium"}
Style: {style if style else "balanced"}

INSTRUCTIONS:
- Adapt tone accordingly (e.g., playful, dark, romantic, aggressive).
- Higher intensity means stronger emotions, emphasis, and dramatic delivery.
- Style controls verbosity:
  - short → concise responses
  - balanced → normal responses
  - descriptive → detailed, immersive narration
- Maintain character personality while applying these adjustments.
"""

    # Conversation formatting
    conversation_block = "\n".join(
        [f"{msg['role'].upper()}: {msg['content']}" for msg in messages]
    )

    prompt = f"""
{core_rules}

=== CHARACTER PROFILE ===
{character_prompt}

=== LONG TERM MEMORY ===
{memory_summary}

=== WORLD STATE ===
{world_state}

{style_block}

=== CONVERSATION ===
{conversation_block}

=== REGENERATION INSTRUCTION ===
{regeneration_instruction}

ASSISTANT:
"""

    return prompt