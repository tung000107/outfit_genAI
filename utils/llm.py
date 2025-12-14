"""LLM integration for outfit text generation."""
import base64
from openai import OpenAI


def encode_image_to_base64(image_bytes: bytes) -> str:
    """Encode image bytes to base64 string."""
    return base64.b64encode(image_bytes).decode("utf-8")


def generate_outfit_recommendation(
    client: OpenAI,
    user_prompt: str,
    season: str,
    occasion: str,
    color_tone: str,
    image_bytes: bytes | None = None,
) -> dict:
    """
    Generate outfit recommendation using GPT-4o.

    Returns a dict with 'recommendation' (text) and 'image_prompt' (for DALL-E).
    """
    system_prompt = """你是一位專業的時尚穿搭顧問 AI。根據使用者提供的資訊，生成詳細的穿搭建議。

你的回覆必須包含以下格式：

## 穿搭建議

### 整體風格
[描述整體穿搭風格和氛圍]

### 單品清單
- **上衣**: [具體描述]
- **下身**: [具體描述]
- **外套**: [如需要，具體描述]
- **鞋款**: [具體描述]
- **配件**: [具體描述]

### 穿搭理由
[解釋為何這套穿搭適合使用者的需求，包含季節性、場合適合度、配色協調性]

---
IMAGE_PROMPT_START
[用英文寫一段適合 DALL-E 生成穿搭示意圖的 prompt，描述一個時尚插畫風格的全身穿搭圖，不要包含真實人臉，使用 fashion illustration style]
IMAGE_PROMPT_END
"""

    user_message_content = []

    # Add image if provided
    if image_bytes:
        base64_image = encode_image_to_base64(image_bytes)
        user_message_content.append({
            "type": "image_url",
            "image_url": {
                "url": f"data:image/jpeg;base64,{base64_image}",
                "detail": "low"
            }
        })
        image_context = "請參考上傳的照片來判斷適合的風格和色彩。"
    else:
        image_context = ""

    user_text = f"""
{image_context}

使用者風格需求: {user_prompt}
季節: {season}
場合: {occasion}
色調偏好: {color_tone}

請根據以上資訊生成穿搭建議。
"""
    user_message_content.append({"type": "text", "text": user_text})

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message_content}
        ],
        max_tokens=1500,
        temperature=0.7
    )

    full_response = response.choices[0].message.content

    # Extract image prompt
    image_prompt = ""
    if "IMAGE_PROMPT_START" in full_response and "IMAGE_PROMPT_END" in full_response:
        start = full_response.find("IMAGE_PROMPT_START") + len("IMAGE_PROMPT_START")
        end = full_response.find("IMAGE_PROMPT_END")
        image_prompt = full_response[start:end].strip()
        # Remove the image prompt section from the recommendation text
        recommendation = full_response[:full_response.find("---\nIMAGE_PROMPT_START")].strip()
    else:
        recommendation = full_response
        # Generate a default image prompt
        image_prompt = f"Fashion illustration of a stylish outfit for {season} {occasion}, {color_tone} color palette, full body fashion sketch style, no face details, elegant and modern, white background"

    return {
        "recommendation": recommendation,
        "image_prompt": image_prompt
    }
