
import random
from datetime import datetime
import streamlit as st

st.set_page_config(
    page_title="Phật Giáo & Lời Phật Dạy",
    page_icon="🪷",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
.stApp { background: #0d1117; color: #f5f1e8; }
.block-container { max-width: 1180px; padding-top: 1.25rem; }
h1, h2, h3 { color: #f3dfaa; }
[data-testid="stSidebar"] { background: #171b22; }
.hero {
    padding:18px 20px; border-radius:18px;
    background: linear-gradient(135deg,#171b22,#242014);
    border:1px solid #4b4127; margin-bottom:18px;
}
</style>
""", unsafe_allow_html=True)

THEMES = [
    "Bình an trong tâm",
    "Buông xả nhẹ lòng",
    "Chánh niệm trong từng hơi thở",
    "Biết đủ là hạnh phúc",
    "Từ bi và yêu thương",
    "Nhân quả trong đời sống",
    "Vô thường – trân quý hiện tại",
    "Tha thứ để lòng nhẹ hơn",
]
SCENES = [
    "Chùa Việt Nam lúc bình minh, sương mỏng, nắng xuyên tán cây",
    "Hồ sen buổi sớm, mặt nước yên, ánh nắng mềm",
    "Sân chùa thanh tịnh sau cơn mưa, nền đá phản chiếu ánh sáng",
    "Lối đá dẫn vào chùa, hàng cây xanh, chim bay xa",
    "Không gian thiền tĩnh lặng với tượng Phật và ánh nến ấm",
]
CAMERAS = [
    "Slow push-in tiến chậm về chủ thể",
    "Slow dolly-in, chuyển động rất mượt",
    "Static cinematic shot, chỉ có chuyển động môi trường tự nhiên",
    "Gentle side tracking shot",
    "Very slow tilt-up từ sân lên mái chùa",
]
ANGLES = [
    "Góc ngang tầm mắt",
    "Góc rộng chính diện",
    "Góc 3/4 nhẹ",
    "Góc thấp nhẹ hướng lên mái chùa",
    "Góc cận vừa với chiều sâu điện ảnh",
]
SOUNDS = [
    "Một tiếng chuông chùa nhẹ, chim hót xa, ambience tự nhiên",
    "Nhạc thiền rất nhẹ, tiếng gió và lá cây",
    "Không nhạc, chỉ âm thanh môi trường thanh tịnh",
    "Chuông gió nhẹ và tiếng chim buổi sớm",
]
MESSAGES = [
    "Buông được một niệm, lòng nhẹ thêm một phần.",
    "Bình an bắt đầu từ một tâm biết dừng.",
    "Biết đủ là một dạng giàu có trong tâm.",
    "Mỗi hơi thở tỉnh thức là một bước trở về.",
    "Điều gì đến rồi cũng sẽ đi; hãy sống trọn với hiện tại.",
]

def ensure_choice(key, values):
    if key not in st.session_state:
        st.session_state[key] = random.choice(values)

def choose_block(title, key, values):
    ensure_choice(key, values)
    st.markdown(f"### {title}")
    mode = st.radio(
        f"{title}-mode",
        ["Bạn đề xuất", "Tự tạo"],
        horizontal=True,
        key=f"{key}_mode",
        label_visibility="collapsed",
    )
    if mode == "Bạn đề xuất":
        c1, c2 = st.columns([4, 1])
        with c1:
            st.info(st.session_state[key])
        with c2:
            if st.button("Đổi đề xuất", key=f"{key}_reroll", use_container_width=True):
                st.session_state[key] = random.choice(values)
                st.rerun()
        return st.session_state[key]
    return st.text_input("Nhập nội dung", key=f"{key}_custom")

st.markdown("""
<div class="hero">
<h1>🪷 PHẬT GIÁO & LỜI PHẬT DẠY</h1>
<p>Web app Streamlit tạo Prompt Google Flow AI cho video Phật giáo, thiền, bình an và lời dạy ý nghĩa.</p>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.header("⚙️ Cấu hình")
    duration = st.selectbox("Thời lượng", ["8 giây", "10 giây", "15 giây"], index=1)
    ratio = st.selectbox("Tỉ lệ", ["9:16", "16:9", "1:1"], index=0)
    language = st.selectbox("Ngôn ngữ Prompt", ["English", "Tiếng Việt"], index=0)
    voiceover = st.toggle("Có Voiceover", value=True)
    text_overlay = st.toggle("Có chữ trên màn hình", value=True)
    st.markdown("---")
    st.caption("v1.0 chạy được mà không cần API. Có thể nâng cấp Gemini API sau.")

tab_create, tab_templates, tab_history = st.tabs(
    ["🎬 Tạo Prompt", "📚 Mẫu nhanh", "🕘 Lịch sử"]
)

with tab_create:
    left, right = st.columns(2)
    with left:
        theme = choose_block("1. Chủ đề / Thông điệp", "theme", THEMES)
        scene = choose_block("2. Bối cảnh", "scene", SCENES)
        camera = choose_block("3. Chuyển động Camera", "camera", CAMERAS)
    with right:
        angle = choose_block("4. Góc máy", "angle", ANGLES)
        sound = choose_block("5. Âm thanh", "sound", SOUNDS)
        message = choose_block("6. Câu chữ / Lời dạy", "message", MESSAGES)

    st.markdown("---")
    st.markdown("### 7. Ảnh tham chiếu")
    use_ref = st.radio("Có dùng ảnh tham chiếu?", ["Không", "Có"], horizontal=True)
    ref_instruction = ""
    if use_ref == "Có":
        ref_file = st.file_uploader("Tải ảnh tham chiếu", type=["png", "jpg", "jpeg", "webp"])
        if ref_file is not None:
            st.image(ref_file, caption="Ảnh tham chiếu", width=280)
            ref_instruction = (
                "Use the uploaded reference image as the exact visual reference. "
                "Preserve the architecture, composition, clothing, colors, and important details."
            )
        else:
            ref_instruction = (
                "A reference image will be provided. Preserve its important visual details."
            )

    st.markdown("---")
    if st.button("✨ TẠO PROMPT GOOGLE FLOW AI", type="primary", use_container_width=True):
        if language == "English":
            prompt = f"""Create a {duration} cinematic video in {ratio}.

Theme: {theme}
Scene: {scene}
Camera movement: {camera}
Camera angle: {angle}
Mood: peaceful, respectful, warm, meditative, natural, cinematic realism.

{ref_instruction}

On-screen text: {"Show this message with a soft fade-in: " + message if text_overlay else "No on-screen text."}
Voiceover: {"Vietnamese voiceover, calm and natural, synchronized with the message: " + message if voiceover else "No voiceover."}
Sound: {sound}

Keep one cohesive visual style and a calm pace. Use slow, smooth motion.
No quick cuts, no random scene changes, no dramatic action, no distorted architecture, no unwanted extra text.
"""
        else:
            prompt = f"""Tạo video điện ảnh thời lượng {duration}, tỉ lệ {ratio}.

Chủ đề: {theme}
Bối cảnh: {scene}
Chuyển động camera: {camera}
Góc máy: {angle}
Không khí: bình an, trang nghiêm, ấm áp, thiền tĩnh, chân thực điện ảnh.

{ref_instruction}

Chữ trên màn hình: {"Hiển thị nhẹ nhàng, fade-in: " + message if text_overlay else "Không hiển thị chữ."}
Voiceover: {"Giọng Việt nhẹ, tự nhiên, đồng bộ với câu: " + message if voiceover else "Không voiceover."}
Âm thanh: {sound}

Giữ phong cách nhất quán, chuyển động chậm và mượt.
Không cắt nhanh, không đổi cảnh ngẫu nhiên, không hành động kịch tính, không làm méo kiến trúc, không thêm chữ ngoài yêu cầu.
"""
        st.session_state["last_prompt"] = prompt
        hist = st.session_state.get("history", [])
        hist.insert(0, {
            "time": datetime.now().strftime("%d/%m/%Y %H:%M"),
            "theme": theme,
            "prompt": prompt
        })
        st.session_state["history"] = hist[:20]

    if st.session_state.get("last_prompt"):
        st.success("Đã tạo Prompt.")
        st.code(st.session_state["last_prompt"], language="text")
        st.download_button(
            "⬇️ Tải Prompt .txt",
            data=st.session_state["last_prompt"],
            file_name="google-flow-ai-prompt.txt",
            mime="text/plain",
            use_container_width=True,
        )

with tab_templates:
    templates = {
        "Chùa buổi sớm": "Bình minh tại chùa Việt Nam, sương mỏng, camera tiến chậm, chuông chùa nhẹ.",
        "Hồ sen bình an": "Hồ sen buổi sớm, mặt nước yên, ánh nắng mềm, nhạc thiền rất nhẹ.",
        "Buông xả": "Khung cảnh thiền tĩnh, thông điệp buông xả nhẹ lòng, không cắt nhanh.",
        "Chánh niệm": "Không gian yên tĩnh, ánh sáng dịu, nhấn mạnh sự tỉnh thức trong hiện tại.",
    }
    for name, desc in templates.items():
        with st.expander(name):
            st.write(desc)

with tab_history:
    history = st.session_state.get("history", [])
    if not history:
        st.info("Chưa có Prompt nào trong phiên này.")
    else:
        for item in history:
            with st.expander(f"{item['time']} — {item['theme']}"):
                st.code(item["prompt"], language="text")

st.markdown("---")
st.caption("Phật Giáo & Lời Phật Dạy – Streamlit v1.0")
