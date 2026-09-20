
import random
import json
from datetime import datetime

import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Phật Giáo & Lời Phật Dạy",
    page_icon="🪷",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------- STYLE ----------------
st.markdown("""
<style>
.stApp { background:#0d1117; color:#f5f1e8; }
.block-container {
    max-width: 1320px;
    padding-top: 1.1rem;
    padding-bottom: 2rem;
}
h1 { font-size:2.55rem !important; color:#f0d993 !important; }
h2 { font-size:1.75rem !important; color:#f0d993 !important; }
h3 { font-size:1.22rem !important; color:#ffffff !important; }
p, label, .stMarkdown, .stRadio, .stSelectbox { font-size:1.02rem !important; }

[data-testid="stSidebar"] {
    background:#151922;
    border-right:1px solid #2a303b;
    min-width: 290px;
}
[data-testid="stSidebar"] .block-container {
    padding-top: 1rem;
    padding-left: 1rem;
    padding-right: 1rem;
}

.hero {
    padding:22px 26px;
    border-radius:18px;
    background:linear-gradient(135deg,#171b22,#272214);
    border:1px solid #5a4a25;
    margin-bottom:16px;
}
.hero p { color:#ddd4c2; margin-bottom:0; }

.tip {
    padding:12px 14px;
    border-radius:12px;
    background:#141a22;
    border-left:4px solid #d7b35a;
    color:#d7d0c4;
}

.result-card {
    padding:16px 18px;
    border-radius:16px;
    background:#141922;
    border:1px solid #5d4c27;
    margin-top:12px;
    margin-bottom:8px;
}

[data-testid="stButton"] button {
    min-height:44px;
    border-radius:10px;
    font-weight:650;
    font-size:0.98rem;
}
[data-testid="stFileUploader"] {
    border-radius:12px;
}
.small-note {
    color:#aaa398;
    font-size:0.9rem;
}
</style>
""", unsafe_allow_html=True)

# ---------------- DATA ----------------
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

STYLES = [
    "Cinematic realism",
    "Thiền tĩnh, tối giản",
    "Trang nghiêm Phật giáo",
    "Tự nhiên, ấm áp",
    "Poetic cinematic",
]

NEGATIVE_PRESETS = {
    "Chuẩn an toàn":
        "No quick cuts, no random scene changes, no dramatic action, no distorted architecture, "
        "no extra limbs, no warped faces, no unwanted text, no oversaturated colors.",
    "Giữ kiến trúc":
        "Do not alter temple architecture, gates, statues, signs, roof details, colors, or spatial layout. "
        "No random objects or people.",
    "Giữ nhân vật":
        "Preserve the same person, face, clothing, age, proportions, and identity. "
        "No face changes, no costume changes, no duplicate person.",
    "Tối giản":
        "No quick cuts, no random changes, no unwanted text, no distortion.",
}

# ---------------- HELPERS ----------------
def reroll_different(current, values):
    candidates = [v for v in values if v != current]
    return random.choice(candidates) if candidates else current

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
        c1, c2 = st.columns([5.4, 1.5])
        with c1:
            st.info(st.session_state[key])
        with c2:
            if st.button("🔄 Đổi", key=f"{key}_reroll", use_container_width=True):
                st.session_state[key] = reroll_different(st.session_state[key], values)
                st.rerun()
        return st.session_state[key]

    return st.text_input(
        "Nhập nội dung",
        key=f"{key}_custom",
        placeholder="Nhập nội dung của bạn..."
    )

def copy_button(text):
    payload = json.dumps(text)
    components.html(
        f"""
        <button id="copyBtn" style="
          width:100%;padding:11px 14px;border-radius:10px;
          border:1px solid #6b582c;background:#d7b35a;color:#111;
          font-weight:700;cursor:pointer;">
          📋 Sao chép Prompt
        </button>
        <script>
        const btn = document.getElementById("copyBtn");
        const txt = {payload};
        btn.onclick = async () => {{
          try {{
            await navigator.clipboard.writeText(txt);
            btn.innerText = "✅ Đã sao chép";
            setTimeout(() => btn.innerText = "📋 Sao chép Prompt", 1500);
          }} catch (e) {{
            btn.innerText = "⚠️ Trình duyệt chặn Clipboard";
          }}
        }};
        </script>
        """,
        height=56,
    )

def reset_app():
    preserved = {"history"}
    for key in list(st.session_state.keys()):
        if key not in preserved:
            del st.session_state[key]

def get_custom_value(key):
    return str(st.session_state.get(f"{key}_custom", "")).strip()

def validate_inputs(use_ref):
    missing = []

    pairs = [
        ("theme", "Chủ đề / Thông điệp"),
        ("camera", "Chuyển động Camera"),
        ("angle", "Góc máy"),
        ("sound", "Âm thanh"),
        ("message", "Câu chữ / Lời dạy"),
    ]
    if use_ref == "Không":
        pairs.append(("scene", "Bối cảnh"))

    for key, label in pairs:
        if st.session_state.get(f"{key}_mode") == "Tự tạo" and not get_custom_value(key):
            missing.append(label)

    return missing

# ---------------- HEADER ----------------
st.markdown("""
<div class="hero">
<h1>🪷 PHẬT GIÁO & LỜI PHẬT DẠY</h1>
<p>Web app Streamlit tạo Prompt Google Flow AI cho video Phật giáo, thiền, bình an và lời dạy ý nghĩa.</p>
</div>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.header("⚙️ Cấu hình nhanh")

    preset = st.radio(
        "Preset video",
        ["8 giây", "10 giây", "Tùy chọn"],
        index=1
    )

    if preset == "Tùy chọn":
        duration = st.selectbox(
            "Thời lượng",
            ["6 giây", "8 giây", "10 giây", "12 giây", "15 giây"],
            index=2
        )
    else:
        duration = preset

    ratio = st.selectbox("Tỉ lệ", ["9:16", "16:9", "1:1"], index=0)
    language = st.selectbox("Ngôn ngữ Prompt", ["English", "Tiếng Việt"], index=0)
    style = st.selectbox("Phong cách video", STYLES, index=0)

    st.markdown("---")
    voiceover = st.toggle("Có Voiceover", value=True)
    text_overlay = st.toggle("Có chữ trên màn hình", value=True)

    st.markdown("---")
    neg_name = st.selectbox("Negative Prompt", list(NEGATIVE_PRESETS.keys()), index=0)
    custom_negative = st.toggle("Tự chỉnh Negative Prompt", value=False)

    if custom_negative:
        negative_prompt = st.text_area(
            "Negative Prompt tùy chỉnh",
            value=NEGATIVE_PRESETS[neg_name],
            height=130
        )
    else:
        negative_prompt = NEGATIVE_PRESETS[neg_name]

    st.markdown("---")
    if st.button("♻️ Reset phiên làm việc", use_container_width=True):
        reset_app()
        st.rerun()

    st.markdown("---")
    st.caption("v1.2 • Polish & Reliability • Không cần API cho chức năng cốt lõi.")

# ---------------- TABS ----------------
tab_create, tab_templates, tab_history = st.tabs(
    ["🎬 Tạo Prompt", "📚 Mẫu nhanh", "🕘 Lịch sử"]
)

# ---------------- CREATE TAB ----------------
with tab_create:
    st.markdown(
        '<div class="tip">💡 Khi dùng ảnh tham chiếu, app ưu tiên ảnh đó làm nguồn hình ảnh chính và giảm vai trò của Bối cảnh.</div>',
        unsafe_allow_html=True
    )
    st.markdown("")

    use_ref = st.radio(
        "Bạn có dùng ảnh tham chiếu không?",
        ["Không", "Có"],
        horizontal=True
    )

    left, right = st.columns(2, gap="large")

    with left:
        theme = choose_block("1. Chủ đề / Thông điệp", "theme", THEMES)

        if use_ref == "Không":
            scene = choose_block("2. Bối cảnh", "scene", SCENES)
        else:
            scene = "Use the uploaded reference image as the primary scene reference."
            st.markdown("### 2. Bối cảnh")
            st.info("Đã dùng ảnh tham chiếu → bối cảnh chính lấy từ ảnh.")

        camera = choose_block("3. Chuyển động Camera", "camera", CAMERAS)

    with right:
        angle = choose_block("4. Góc máy", "angle", ANGLES)
        sound = choose_block("5. Âm thanh", "sound", SOUNDS)
        message = choose_block("6. Câu chữ / Lời dạy", "message", MESSAGES)

    st.markdown("---")
    st.markdown("### 7. Ảnh tham chiếu")

    ref_instruction = ""
    ref_file = None

    if use_ref == "Có":
        ref_file = st.file_uploader(
            "Tải ảnh tham chiếu",
            type=["png", "jpg", "jpeg", "webp"]
        )
        if ref_file is not None:
            st.image(ref_file, caption="Ảnh tham chiếu", width=340)
            ref_instruction = (
                "Use the uploaded reference image as the exact visual reference. "
                "Preserve architecture, composition, clothing, colors, facial identity, "
                "and important visual details. Do not invent a new location unless required."
            )
        else:
            st.warning("Bạn đã chọn dùng ảnh tham chiếu nhưng chưa tải ảnh.")
            ref_instruction = (
                "A reference image will be provided. Use it as the primary visual source "
                "and preserve all key details."
            )
    else:
        st.caption("Không dùng ảnh tham chiếu.")

    st.markdown("---")

    if st.button(
        "✨ TẠO PROMPT GOOGLE FLOW AI",
        type="primary",
        use_container_width=True
    ):
        missing = validate_inputs(use_ref)

        if missing:
            st.error(
                "Vui lòng nhập nội dung cho các mục đang ở chế độ Tự tạo: "
                + ", ".join(missing)
            )
        elif use_ref == "Có" and ref_file is None:
            st.error("Vui lòng tải ảnh tham chiếu trước khi tạo Prompt.")
        else:
            if language == "English":
                prompt = f"""Create a {duration} cinematic video in {ratio}.

Theme: {theme}
Visual style: {style}
Scene: {scene}
Camera movement: {camera}
Camera angle: {angle}
Mood: peaceful, respectful, warm, meditative, natural, cinematic realism.

{ref_instruction}

On-screen text: {"Show this message with a soft fade-in, synchronized naturally: " + message if text_overlay else "No on-screen text."}
Voiceover: {"Vietnamese voiceover, calm and natural, synchronized with the message: " + message if voiceover else "No voiceover."}
Sound: {sound}

Continuity:
Keep one cohesive visual style and a calm pace. Use slow, smooth motion.
Preserve scene continuity and avoid sudden changes.

Negative prompt:
{negative_prompt}
"""
            else:
                prompt = f"""Tạo video điện ảnh thời lượng {duration}, tỉ lệ {ratio}.

Chủ đề: {theme}
Phong cách hình ảnh: {style}
Bối cảnh: {scene}
Chuyển động camera: {camera}
Góc máy: {angle}
Không khí: bình an, trang nghiêm, ấm áp, thiền tĩnh, chân thực điện ảnh.

{ref_instruction}

Chữ trên màn hình: {"Hiển thị nhẹ nhàng, fade-in, đồng bộ tự nhiên: " + message if text_overlay else "Không hiển thị chữ."}
Voiceover: {"Giọng Việt nhẹ, tự nhiên, đồng bộ với câu: " + message if voiceover else "Không voiceover."}
Âm thanh: {sound}

Tính liên tục:
Giữ một phong cách hình ảnh thống nhất, chuyển động chậm và mượt.
Không thay đổi cảnh đột ngột.

Negative Prompt:
{negative_prompt}
"""

            st.session_state["last_prompt"] = prompt

            history = st.session_state.get("history", [])
            history.insert(0, {
                "time": datetime.now().strftime("%d/%m/%Y %H:%M"),
                "theme": theme,
                "duration": duration,
                "ratio": ratio,
                "prompt": prompt,
            })
            st.session_state["history"] = history[:30]

    if st.session_state.get("last_prompt"):
        st.markdown(
            '<div class="result-card"><h3>✅ Prompt hoàn chỉnh</h3><div class="small-note">Có thể sao chép hoặc tải xuống ngay.</div></div>',
            unsafe_allow_html=True
        )

        st.text_area(
            "Kết quả Prompt",
            st.session_state["last_prompt"],
            height=360,
            label_visibility="collapsed"
        )

        c1, c2 = st.columns(2)
        with c1:
            copy_button(st.session_state["last_prompt"])
        with c2:
            st.download_button(
                "⬇️ Tải Prompt .txt",
                data=st.session_state["last_prompt"],
                file_name="google-flow-ai-prompt.txt",
                mime="text/plain",
                use_container_width=True
            )

# ---------------- TEMPLATES TAB ----------------
with tab_templates:
    st.subheader("📚 Mẫu nhanh")

    templates = {
        "Chùa buổi sớm":
            "Bình minh tại chùa Việt Nam, sương mỏng, camera tiến chậm, chuông chùa nhẹ.",
        "Hồ sen bình an":
            "Hồ sen buổi sớm, mặt nước yên, ánh nắng mềm, nhạc thiền rất nhẹ.",
        "Buông xả":
            "Khung cảnh thiền tĩnh, thông điệp buông xả nhẹ lòng, không cắt nhanh.",
        "Chánh niệm":
            "Không gian yên tĩnh, ánh sáng dịu, nhấn mạnh sự tỉnh thức trong hiện tại.",
        "Lời Phật dạy":
            "Cảnh chùa trang nghiêm, lời dạy ngắn gọn, giọng đọc chậm và ấm.",
    }

    for name, desc in templates.items():
        with st.expander(name):
            st.write(desc)

# ---------------- HISTORY TAB ----------------
with tab_history:
    st.subheader("🕘 Lịch sử trong phiên")

    history = st.session_state.get("history", [])

    if not history:
        st.info("Chưa có Prompt nào trong phiên này.")
    else:
        history_text = []
        for item in history:
            with st.expander(
                f"{item['time']} — {item['theme']} — {item['duration']} — {item['ratio']}"
            ):
                st.code(item["prompt"], language="text")

            history_text.append(
                f"{item['time']} | {item['theme']} | {item['duration']} | {item['ratio']}\n"
                f"{item['prompt']}\n\n{'='*80}\n\n"
            )

        st.download_button(
            "⬇️ Tải toàn bộ lịch sử .txt",
            data="".join(history_text),
            file_name="lich-su-prompt.txt",
            mime="text/plain",
            use_container_width=True
        )

st.markdown("---")
st.caption("Phật Giáo & Lời Phật Dạy – Streamlit v1.2")
