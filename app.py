"""
OutfitGenAI - AI 個人化穿搭生成系統
A personalized outfit generation system using LLM and DALL-E 3.
"""
import os
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
from PIL import Image
import io

from utils.llm import generate_outfit_recommendation
from utils.image_gen import generate_outfit_image, download_image

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="OutfitGenAI - AI 穿搭助手",
    page_icon="👔",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        color: #1E3A5F;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.2rem;
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    .stButton > button {
        width: 100%;
    }
    .recommendation-box {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize OpenAI client
@st.cache_resource
def get_openai_client():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return None
    return OpenAI(api_key=api_key)

def main():
    # Header
    st.markdown('<p class="main-header">👔 OutfitGenAI</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">AI 個人化穿搭生成系統 - 輸入你的需求，獲得專屬穿搭建議與示意圖</p>', unsafe_allow_html=True)

    # Check for API key
    client = get_openai_client()

    # Sidebar for API key input if not in environment
    with st.sidebar:
        st.header("⚙️ 設定")
        if not client:
            api_key_input = st.text_input("OpenAI API Key", type="password", help="請輸入你的 OpenAI API Key")
            if api_key_input:
                client = OpenAI(api_key=api_key_input)
                st.success("API Key 已設定!")
        else:
            st.success("✅ API Key 已從環境變數載入")

        st.divider()
        st.markdown("### 關於 OutfitGenAI")
        st.markdown("""
        本系統結合 GPT-4o 與 DALL-E 3，
        根據你的照片、風格需求與偏好，
        生成個人化的穿搭建議與示意圖。
        """)

    if not client:
        st.warning("請在側邊欄輸入 OpenAI API Key 以開始使用")
        return

    # Main content - Two columns
    col1, col2 = st.columns([1, 1])

    with col1:
        st.header("📝 輸入你的需求")

        # Photo upload
        st.subheader("1. 上傳照片（選填）")
        uploaded_file = st.file_uploader(
            "上傳一張照片，系統會分析整體氣質與色彩",
            type=["jpg", "jpeg", "png"],
            help="照片僅用於分析風格，不會直接用於生成圖片"
        )

        if uploaded_file:
            image = Image.open(uploaded_file)
            st.image(image, caption="已上傳的照片", use_column_width=True)

        # Style prompt
        st.subheader("2. 描述你想要的風格")
        style_prompt = st.text_area(
            "輸入你的風格需求",
            placeholder="例如：韓系大學生風、日系簡約、職場正式、約會甜美風...",
            height=100
        )

        # Season selection
        st.subheader("3. 選擇季節")
        season_cols = st.columns(4)
        seasons = ["🌸 春季", "☀️ 夏季", "🍂 秋季", "❄️ 冬季"]
        season_values = ["春季", "夏季", "秋季", "冬季"]
        selected_season = None

        if "selected_season" not in st.session_state:
            st.session_state.selected_season = None

        for i, (col, season, value) in enumerate(zip(season_cols, seasons, season_values)):
            with col:
                if st.button(season, key=f"season_{i}"):
                    st.session_state.selected_season = value

        if st.session_state.selected_season:
            st.info(f"已選擇：{st.session_state.selected_season}")

        # Occasion selection
        st.subheader("4. 選擇場合")
        occasion_cols = st.columns(4)
        occasions = ["💕 約會", "💼 工作", "🎓 校園", "✈️ 旅行"]
        occasion_values = ["約會", "工作", "校園", "旅行"]

        if "selected_occasion" not in st.session_state:
            st.session_state.selected_occasion = None

        for i, (col, occasion, value) in enumerate(zip(occasion_cols, occasions, occasion_values)):
            with col:
                if st.button(occasion, key=f"occasion_{i}"):
                    st.session_state.selected_occasion = value

        if st.session_state.selected_occasion:
            st.info(f"已選擇：{st.session_state.selected_occasion}")

        # Color tone selection
        st.subheader("5. 選擇色調偏好")
        color_cols = st.columns(4)
        colors = ["❄️ 冷色系", "🔥 暖色系", "🌰 大地色", "⬛ 黑白灰"]
        color_values = ["冷色系", "暖色系", "大地色系", "黑白灰"]

        if "selected_color" not in st.session_state:
            st.session_state.selected_color = None

        for i, (col, color, value) in enumerate(zip(color_cols, colors, color_values)):
            with col:
                if st.button(color, key=f"color_{i}"):
                    st.session_state.selected_color = value

        if st.session_state.selected_color:
            st.info(f"已選擇：{st.session_state.selected_color}")

        # Generate button
        st.divider()
        generate_btn = st.button("✨ 生成穿搭建議", type="primary")

    with col2:
        st.header("🎨 生成結果")

        if generate_btn:
            # Validate inputs
            if not style_prompt:
                st.error("請輸入風格需求")
            elif not st.session_state.selected_season:
                st.error("請選擇季節")
            elif not st.session_state.selected_occasion:
                st.error("請選擇場合")
            elif not st.session_state.selected_color:
                st.error("請選擇色調偏好")
            else:
                # Get image bytes if uploaded
                image_bytes = None
                if uploaded_file:
                    uploaded_file.seek(0)
                    image_bytes = uploaded_file.read()

                # Generate recommendation
                with st.spinner("🤔 AI 正在分析你的需求並生成穿搭建議..."):
                    try:
                        result = generate_outfit_recommendation(
                            client=client,
                            user_prompt=style_prompt,
                            season=st.session_state.selected_season,
                            occasion=st.session_state.selected_occasion,
                            color_tone=st.session_state.selected_color,
                            image_bytes=image_bytes
                        )

                        st.session_state.recommendation = result["recommendation"]
                        st.session_state.image_prompt = result["image_prompt"]
                        st.success("穿搭建議生成完成!")
                    except Exception as e:
                        st.error(f"生成建議時發生錯誤: {str(e)}")
                        return

                # Generate image
                with st.spinner("🎨 AI 正在生成穿搭示意圖..."):
                    try:
                        image_url = generate_outfit_image(client, st.session_state.image_prompt)
                        if image_url:
                            st.session_state.generated_image_url = image_url
                            st.success("示意圖生成完成!")
                        else:
                            st.warning("示意圖生成失敗，但文字建議已完成")
                    except Exception as e:
                        st.warning(f"生成示意圖時發生錯誤: {str(e)}")

        # Display results
        if "recommendation" in st.session_state and st.session_state.recommendation:
            st.markdown("### 📋 穿搭建議")
            st.markdown(st.session_state.recommendation)

            # Display generated image
            if "generated_image_url" in st.session_state and st.session_state.generated_image_url:
                st.markdown("### 👗 穿搭示意圖")
                st.image(st.session_state.generated_image_url, use_column_width=True)

                # Download button
                image_data = download_image(st.session_state.generated_image_url)
                if image_data:
                    st.download_button(
                        label="📥 下載示意圖",
                        data=image_data,
                        file_name="outfit_suggestion.png",
                        mime="image/png"
                    )

            # Show the image prompt used (for debugging/transparency)
            with st.expander("🔍 查看圖像生成 Prompt"):
                st.code(st.session_state.get("image_prompt", ""))

            # Regenerate button
            if st.button("🔄 重新生成"):
                st.session_state.recommendation = None
                st.session_state.generated_image_url = None
                st.rerun()

        else:
            st.info("👈 請在左側輸入你的需求，然後點擊「生成穿搭建議」按鈕")

    # Footer
    st.divider()
    st.markdown("""
    <div style='text-align: center; color: #888; padding: 10px;'>
        OutfitGenAI - 陽明交通大學 GenAI 期末專案<br>
        Powered by GPT-4o & DALL-E 3
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
