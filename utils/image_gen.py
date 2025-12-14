"""Image generation using DALL-E 3."""
import requests
from openai import OpenAI


def generate_outfit_image(client: OpenAI, prompt: str) -> str | None:
    """
    Generate outfit visualization image using DALL-E 3.

    Returns the URL of the generated image, or None if failed.
    """
    # Enhance prompt for fashion illustration style
    enhanced_prompt = f"""Fashion illustration style, {prompt}.
    The image should be a stylish fashion sketch or illustration showing the complete outfit.
    Do NOT include realistic human faces - use a fashion illustration style with minimal or stylized facial features.
    Clean white or soft gradient background. Professional fashion magazine quality."""

    try:
        response = client.images.generate(
            model="dall-e-3",
            prompt=enhanced_prompt,
            size="1024x1024",
            quality="standard",
            n=1,
        )
        return response.data[0].url
    except Exception as e:
        print(f"Image generation error: {e}")
        return None


def download_image(url: str) -> bytes | None:
    """Download image from URL and return bytes."""
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        return response.content
    except Exception as e:
        print(f"Image download error: {e}")
        return None
