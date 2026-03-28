from app.ai.gemini_client import client, MODEL_NAME
from app.ai.prompt_builder import build_prompt
from google.genai.errors import ClientError
import asyncio


async def generate_response(
    character_prompt: str,
    messages: list,
    memory_summary: str = "",
    world_state: str = "",
    regeneration_instruction: str = "",
    style_config: dict = None,
) -> str:

    full_prompt = build_prompt(
        character_prompt=character_prompt,
        messages=messages,
        memory_summary=memory_summary,
        world_state=world_state,
        regeneration_instruction=regeneration_instruction,
        style_config=style_config,
    )

    # 🔁 Try primary model first
    try:
        response = client.models.generate_content(
            model=MODEL_NAME,  # e.g. gemini-2.5-flash
            contents=full_prompt,
        )
        return response.text

    except ClientError as e:
        error_msg = str(e)

        # 🚨 QUOTA / RATE LIMIT HIT
        if "429" in error_msg or "RESOURCE_EXHAUSTED" in error_msg:
            print("⚠️ Primary model quota exceeded. Switching to fallback...")

            try:
                # 🔁 Fallback model
                response = client.models.generate_content(
                    model="gemini-1.5-flash",
                    contents=full_prompt,
                )
                return response.text

            except Exception as fallback_error:
                print("❌ Fallback model also failed:", fallback_error)
                return "⚠️ AI service is currently overloaded. Please try again later."

        # ❌ OTHER ERRORS
        print("❌ Gemini API Error:", error_msg)
        return f"Error: {error_msg}"

    except Exception as e:
        print("❌ Unexpected Error:", str(e))
        return "⚠️ Unexpected server error. Please try again."