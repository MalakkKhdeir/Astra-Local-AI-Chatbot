from pathlib import Path



import streamlit as st



from chatbot import ask_ai

from session_manager import (

    create_chat,

    list_chats,

    load_chat,

    save_chat,

    update_chat_title,

)



# ---------------------------------------------------------

# Astra configuration

# ---------------------------------------------------------

BASE_DIR = Path(__file__).parent
ASSETS_DIR = BASE_DIR / "assets"

LOGO_PATH = ASSETS_DIR / "astra_logo_transparent.png"
APP_ICON = ASSETS_DIR / "astra_app_icon_transparent.png"



st.set_page_config(

    page_title="Astra | Your AI, Your Space",

    page_icon=str(APP_ICON) if APP_ICON.exists() else "✨",

    layout="wide",

    initial_sidebar_state="expanded",

)



# ---------------------------------------------------------

# Language

# ---------------------------------------------------------

if "language" not in st.session_state:

    st.session_state.language = "English"



LANGUAGE_OPTIONS = ["English", "العربية"]

language = st.session_state.language

is_arabic = language == "العربية"

direction = "rtl" if is_arabic else "ltr"

align = "right" if is_arabic else "left"



T = {

    "new_chat": "محادثة جديدة" if is_arabic else "New Chat",

    "chats": "المحادثات" if is_arabic else "Chats",

    "conversations": "محادثاتك" if is_arabic else "Your Conversations",

    "search": "ابحث في محادثاتك..." if is_arabic else "Search conversations...",

    "welcome": "أهلًا، أنا أسترا" if is_arabic else "Hello, I'm Astra",

    "tagline": "مساعدك الذكي، مساحتك الخاصة." if is_arabic else "Your AI, your space.",

    "local_private": "محلي وخاص" if is_arabic else "Local & Private",

    "local_desc": "يعمل على جهازك باستخدام Ollama" if is_arabic else "Runs on your device with Ollama",

    "languages": "العربية والإنجليزية" if is_arabic else "Arabic & English",

    "languages_desc": "تحدّث باللغة التي تفضّلها" if is_arabic else "Chat naturally in both languages",

    "saved": "محادثات محفوظة" if is_arabic else "Saved Conversations",

    "saved_desc": "احتفظ بأفكارك منظمة" if is_arabic else "Keep your ideas organized",

    "your_space": "مساحتك الخاصة" if is_arabic else "Your Space",

    "space_desc": "تجربة محادثة هادئة وجميلة" if is_arabic else "A calm and beautiful chat experience",

    "empty_title": "بماذا يمكنني مساعدتك اليوم؟" if is_arabic else "What can I help you with today?",

    "empty_desc": "اكتب رسالتك بالأسفل ولنبدأ." if is_arabic else "Type your message below and let's get started.",

    "input": "اكتب رسالتك هنا..." if is_arabic else "Type your message...",

    "thinking": "أسترا تفكّر..." if is_arabic else "Astra is thinking...",

    "connection_error": "تعذّر الاتصال بـ Ollama. تأكد من تشغيله ثم حاول مجددًا." if is_arabic else "Couldn't connect to Ollama. Make sure it's running, then try again.",

    "empty_response": "وصل رد فارغ من النموذج. جرّب مرة أخرى." if is_arabic else "The model returned an empty response. Please try again.",

    "model": "Qwen3:0.6b",

    "connected_label": "نموذج محلي" if is_arabic else "Local model",

    "settings": "الإعدادات" if is_arabic else "Settings",

    "online": "Ollama متصل" if is_arabic else "Ollama Connected",

    "offline": "Ollama غير متصل" if is_arabic else "Ollama Offline",

    "language_label": "اللغة" if is_arabic else "Language",

}





@st.cache_data(ttl=10)

def ollama_online() -> bool:

    """Check whether the local Ollama server is reachable."""

    try:

        import ollama



        ollama.list()

        return True

    except Exception:

        return False





# ---------------------------------------------------------

# Visual design

# ---------------------------------------------------------

st.markdown(

    f"""

    <style>

    :root {{

        color-scheme: light;

        --astra-bg: #F5F7FF;

        --astra-ink: #171A49;

        --astra-muted: #6F79A8;

        --astra-purple: #744BFF;

        --astra-blue: #347BFF;

        --astra-cyan: #06BFD5;

        --astra-border: #E0E7FF;

    }}



    html, body, .stApp,

    [data-testid="stAppViewContainer"],

    [data-testid="stMain"],

    [data-testid="stMainBlockContainer"],

    [data-testid="stBottom"],

    [data-testid="stBottomBlockContainer"] {{

        background: var(--astra-bg) !important;

        color: var(--astra-ink) !important;

    }}



    [data-testid="stAppViewContainer"] {{

        background:

            radial-gradient(ellipse at 82% 12%, rgba(95, 194, 255, .17), transparent 32%),

            radial-gradient(ellipse at 42% 0%, rgba(156, 122, 255, .14), transparent 34%),

            linear-gradient(145deg, #FAFBFF 0%, #F2F5FF 58%, #F0FAFF 100%) !important;

    }}



    [data-testid="stHeader"] {{

        background: rgba(247,249,255,.88) !important;

    }}



    /* Fixed sidebar width: 300px */

    section[data-testid="stSidebar"] {{

        width: 300px !important;

        min-width: 300px !important;

        max-width: 300px !important;

        flex: 0 0 300px !important;

        background: linear-gradient(180deg, #F8F9FF 0%, #EEF1FF 62%, #EAF9FF 100%) !important;

        border-right: 1px solid #E1E7FA;

    }}

    [data-testid="stSidebar"] > div:first-child {{

        box-sizing: border-box !important;

        width: 100% !important;

        min-width: 0 !important;

        height: 100vh !important;

        background: transparent !important;

        padding: 1rem .95rem;

        overflow-y: auto !important;

        overflow-x: hidden !important;

        overscroll-behavior: contain;

    }}

    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"],

    [data-testid="stSidebar"] button {{

        min-width: 0 !important;

        overflow-wrap: anywhere !important;

    }}



    .astra-symbol {{

        width: 45px;

        height: 45px;

        margin: 0 auto;

        border-radius: 15px;

        display: flex;

        align-items: center;

        justify-content: center;

        color: white;

        font-size: 1.55rem;

        font-weight: 900;

        background: linear-gradient(135deg, #8247FF, #477BFF 62%, #05C6D7);

        box-shadow: 0 8px 20px rgba(104, 91, 255, .23);

    }}

    .astra-wordmark {{

        margin: .3rem 0 0;

        text-align: center;

        font-size: 2rem;

        line-height: 1.05;

        font-weight: 850;

        letter-spacing: -.06em;

        color: #211B62;

    }}

    .astra-tagline {{

        margin: .4rem 0 1rem;

        color: #727AA7;

        font-size: .63rem;

        letter-spacing: .13em;

        text-align: center;

    }}



    /* ---------- Top bar ---------- */

    .astra-topbar {{

        display: flex;

        align-items: center;

        justify-content: space-between;

        gap: 1rem;

        padding: .7rem 1.1rem;

        margin: 0 0 .8rem;

        border: 1px solid rgba(255,255,255,.95);

        border-radius: 22px;

        background: rgba(255,255,255,.72);

        box-shadow: 0 7px 24px rgba(65,90,170,.06);

        direction: {direction};

    }}

    .astra-top-brand {{

        color: #211B62;

        font-weight: 800;

        font-size: 1.15rem;

    }}

    .astra-top-sub {{

        color: #7A83AA;

        font-size: .66rem;

        letter-spacing: .1em;

    }}

    .astra-status {{

        display: inline-flex;

        align-items: center;

        gap: .55rem;

        padding: .55rem .9rem;

        border-radius: 18px;

        background: #EDF8F5;

        border: 1px solid #D7F2E9;

        color: #246C5B;

        font-size: .78rem;

        font-weight: 750;

        white-space: nowrap;

    }}

    .astra-status-dot {{

        width: 9px;

        height: 9px;

        border-radius: 50%;

        background: #21B889;

        box-shadow: 0 0 0 4px rgba(33,184,137,.12);

    }}

    .astra-status.off {{

        background: #FDEEEE;

        border-color: #F7D3D3;

        color: #9A3030;

    }}

    .astra-status.off .astra-status-dot {{

        background: #E24B4B;

        box-shadow: 0 0 0 4px rgba(226,75,75,.12);

    }}



    /* ---------- Hero ---------- */

    .astra-hero {{

        position: relative;

        overflow: hidden;

        margin: 0 0 .8rem;

        padding: 1.35rem 1.2rem 1.25rem;

        border: 1px solid rgba(255,255,255,.95);

        border-radius: 25px;

        text-align: center;

        background:

            radial-gradient(circle at 7% 30%, rgba(158,123,255,.19), transparent 28%),

            radial-gradient(circle at 95% 25%, rgba(6,191,213,.17), transparent 30%),

            linear-gradient(120deg, #FFFFFF 0%, #F0F2FF 52%, #E8FBFF 100%);

        box-shadow: 0 10px 30px rgba(75,101,190,.07);

    }}

    .astra-eyebrow {{

        color: #6B5CFF;

        font-size: .68rem;

        font-weight: 850;

        letter-spacing: .2em;

        margin-bottom: .35rem;

    }}

    .astra-hero h1 {{

        margin: 0;

        padding: 0;

        font-size: clamp(1.8rem, 3vw, 2.5rem);

        line-height: 1.3;

        font-weight: 850;

        background: linear-gradient(90deg, #744BFF 0%, #3979F6 56%, #04AFC7 100%);

        -webkit-background-clip: text;

        background-clip: text;

        -webkit-text-fill-color: transparent;

    }}

    .astra-hero p {{

        margin: .35rem 0 0;

        color: #68739F;

        font-size: .94rem;

    }}



    .astra-features {{

        display: grid;

        grid-template-columns: repeat(4, minmax(0, 1fr));

        gap: .65rem;

        margin: 1rem 0 0;

        direction: {direction};

    }}

    .astra-feature {{

        min-height: 108px;

        padding: .85rem .5rem;

        text-align: center;

        border: 1px solid rgba(255,255,255,.95);

        border-radius: 19px;

        background: rgba(255,255,255,.76);

        box-shadow: 0 7px 20px rgba(75,101,190,.05);

    }}

    .astra-feature-icon {{

        font-size: 1.55rem;

        margin-bottom: .3rem;

        color: #6B5CFF;

    }}

    .astra-feature-title {{ color: #202452; font-size: .83rem; font-weight: 800; }}

    .astra-feature-desc {{ color: #737CA8; font-size: .73rem; margin-top: .25rem; line-height: 1.45; }}



    /* ---------- Buttons / inputs ---------- */

    .stButton > button {{

        min-height: 2.5rem;

        border: 1px solid #DFE6FF;

        border-radius: 13px;

        background: rgba(255,255,255,.88);

        color: #25285C;

        transition: all .18s ease;

    }}

    .stButton > button:hover {{

        border-color: #9D7BFF;

        color: #6046E8;

        box-shadow: 0 5px 15px rgba(107,92,255,.12);

        transform: translateY(-1px);

    }}

    [data-testid="stSidebar"] .stButton > button {{

        text-align: {align};

        font-size: .85rem;

        min-height: 2.3rem;

    }}

    [data-testid="stSidebar"] button[kind="primary"] {{

        color: white !important;

        border: none !important;

        background: linear-gradient(100deg, #814DFF 0%, #5D70FF 57%, #06BBD2 100%) !important;

        box-shadow: 0 8px 18px rgba(107,92,255,.22);

        font-weight: 750;

    }}



    [data-testid="stSelectbox"] label,

    [data-testid="stTextInput"] label {{

        color: #68739F !important;

        font-size: .78rem;

    }}

    [data-testid="stTextInput"] div[data-baseweb="input"],

    [data-testid="stTextInput"] div[data-baseweb="base-input"],

    [data-testid="stSelectbox"] div[data-baseweb="select"] > div {{

        background: #FFFFFF !important;

        border: 1px solid #DFE6FF !important;

        border-radius: 13px !important;

        color: #202452 !important;

    }}

    [data-testid="stTextInput"] input {{

        background: transparent !important;

        color: #202452 !important;

        -webkit-text-fill-color: #202452 !important;

    }}

    [data-testid="stTextInput"] input::placeholder {{

        color: #929ABF !important;

        -webkit-text-fill-color: #929ABF !important;

    }}

    [data-testid="stSelectbox"] div[data-baseweb="select"] div {{

        color: #202452 !important;

    }}

    [data-testid="stSelectbox"] svg {{

        fill: #6F79A8 !important;

    }}

    [data-baseweb="popover"] [data-baseweb="menu"],

    [data-baseweb="popover"] li {{

        background: #FFFFFF !important;

        color: #202452 !important;

    }}



    /* ---------- Chat messages ---------- */

    [data-testid="stChatMessage"] {{

        background: rgba(255,255,255,.90) !important;

        border: 1px solid #E4E9FB !important;

        border-radius: 18px !important;

        padding: .7rem .9rem !important;

        box-shadow: 0 5px 17px rgba(75,101,190,.045);

        margin-bottom: .55rem;

        width: fit-content;

        min-width: 140px;

        max-width: 78%;

    }}

    [data-testid="stChatMessage"] p,

    [data-testid="stChatMessage"] li {{

        color: #202452 !important;

        line-height: 1.55;

    }}

    /* Each paragraph picks its own direction from its content:

       Arabic text -> RTL / right-aligned, English text -> LTR / left-aligned */

    [data-testid="stChatMessageContent"] p,

    [data-testid="stChatMessageContent"] li,

    [data-testid="stChatMessageContent"] h1,

    [data-testid="stChatMessageContent"] h2,

    [data-testid="stChatMessageContent"] h3 {{

        unicode-bidi: plaintext;

        text-align: start;

    }}



    /* User bubble: purple, aligned to the opposite side */

    [data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]),

    [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {{

        flex-direction: row-reverse;

        margin-left: auto;

        background: linear-gradient(135deg, #7A5CFF, #8F6CFF) !important;

        border: none !important;

    }}

    [data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) p,

    [data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) li,

    [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) p,

    [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) li {{

        color: #FFFFFF !important;

    }}



    /* ---------- User avatar: purple circle + person icon ---------- */

    [data-testid="stChatMessageAvatarUser"],

    [data-testid="chatAvatarIcon-user"] {{

        position: relative;

        background: linear-gradient(135deg, #8A6CFF, #5D70FF) !important;

        border-radius: 50% !important;

    }}

    [data-testid="stChatMessageAvatarUser"] > *,

    [data-testid="chatAvatarIcon-user"] > * {{

        display: none !important;

    }}

    [data-testid="stChatMessageAvatarUser"]::after,

    [data-testid="chatAvatarIcon-user"]::after {{

        content: "";

        position: absolute;

        inset: 0;

        background: url("data:image/svg+xml;utf8,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='white' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Ccircle cx='12' cy='8' r='4'/%3E%3Cpath d='M4 21c0-4 4-7 8-7s8 3 8 7'/%3E%3C/svg%3E") center / 58% no-repeat;

    }}



    /* ---------- Sidebar section title ---------- */

    .astra-section-title {{

        color: #202452;

        font-weight: 800;

        font-size: .95rem;

        margin: .6rem 0 .4rem;

        direction: {direction};

    }}



    [data-testid="stMainBlockContainer"] {{
        padding-top: 2.5rem !important;
        padding-bottom: 6rem !important;
        max-width: 1500px;
        overflow-wrap: anywhere;
    }}

    [data-testid="stMain"] {{
        overflow-x: hidden !important;
    }}

    [data-testid="stChatMessageContent"] {{
        min-width: 0 !important;
        overflow-wrap: anywhere !important;
        word-break: normal !important;
    }}

    [data-testid="stChatMessageContent"] p {{
        white-space: pre-wrap !important;
        overflow-wrap: anywhere !important;
    }}

    /* ---------- Composer ---------- */

    [data-testid="stBottom"] {{

        background: linear-gradient(180deg, rgba(245,247,255,0), #F5F7FF 22%) !important;

    }}

    [data-testid="stBottom"] > div {{

        background: transparent !important;

    }}

    [data-testid="stChatInput"],

    [data-testid="stChatInput"] > div,

    [data-testid="stChatInput"] textarea,

    [data-testid="stChatInput"] textarea:focus {{

        background: #FFFFFF !important;

        color: #171A49 !important;

        border-radius: 18px !important;

    }}

    [data-testid="stChatInput"] > div {{

        border: 1px solid #DCE5FF !important;

        box-shadow: 0 8px 24px rgba(75,101,190,.09) !important;

    }}

    [data-testid="stChatInput"] textarea::placeholder {{

        color: #929ABF !important;

        -webkit-text-fill-color: #929ABF !important;

    }}

    [data-testid="stChatInput"] button {{

        color: white !important;

        background: linear-gradient(135deg, #814DFF, #477BFF, #06BBD2) !important;

        border-radius: 12px !important;

    }}



    .astra-sidebar-note {{

        padding: .7rem .8rem;

        border: 1px solid #E1E8FA;

        border-radius: 15px;

        background: rgba(255,255,255,.72);

        color: #68739F;

        font-size: .77rem;

        direction: {direction};

    }}

    .astra-footer {{

        text-align: center;

        color: #8991B3;

        font-size: .72rem;

        padding: .35rem 0 .6rem;

    }}



    @media (max-width: 1000px) {{

        .astra-features {{ grid-template-columns: repeat(2, minmax(0, 1fr)); }}

    }}

    @media (max-width: 600px) {{

        .astra-hero {{ padding: 1.1rem .7rem; border-radius: 18px; }}

        .astra-status {{ font-size: .68rem; padding: .45rem .6rem; }}

        [data-testid="stChatMessage"] {{ max-width: 94%; }}

    }}

    </style>

    """,

    unsafe_allow_html=True,

)



# ---------------------------------------------------------

# Conversation state

# ---------------------------------------------------------

if "current_chat_id" not in st.session_state:

    existing_chats = list_chats()

    if existing_chats:

        st.session_state.current_chat_id = existing_chats[0]["id"]

    else:

        first_chat = create_chat()

        st.session_state.current_chat_id = first_chat["id"]



chat = load_chat(st.session_state.current_chat_id)

if chat is None:

    chat = create_chat()

    st.session_state.current_chat_id = chat["id"]



# ---------------------------------------------------------

# Sidebar

# ---------------------------------------------------------

with st.sidebar:

    if APP_ICON.exists():

        left, mid, right = st.columns([1, 2, 1])

        with mid:

            st.image(str(LOGO_PATH), width=90)

    else:

        st.markdown('<div class="astra-symbol">A✦</div>', unsafe_allow_html=True)

    st.markdown(

        '<div class="astra-wordmark">Astra</div>'

        '<div class="astra-tagline">YOUR AI, YOUR SPACE.</div>',

        unsafe_allow_html=True,

    )



    if st.button(T["new_chat"], use_container_width=True, type="primary"):

        new_chat = create_chat()

        st.session_state.current_chat_id = new_chat["id"]

        st.rerun()



    st.markdown("")



    st.markdown(
    f"""
    <div style="
        padding: 16px;
        border: 1px solid #E1E8FA;
        border-radius: 16px;
        background: rgba(255,255,255,0.85);
        color: #68739F;
        direction: {direction};
    ">
        <div style="font-weight: 700; color: #202452;">
            ◈ &nbsp; {T["connected_label"]}
        </div>
        <div style="font-size: 13px; margin-top: 6px;">
            {T["model"]}
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)



    st.selectbox(

        T["language_label"],

        LANGUAGE_OPTIONS,

        key="language",

    )



    st.markdown(

        f'<div class="astra-section-title">{T["conversations"]}</div>',

        unsafe_allow_html=True,

    )



    search_query = st.text_input(

        T["search"],

        label_visibility="collapsed",

        placeholder=T["search"],

        key="conversation_search",

    )



    all_chats = list_chats()

    filtered_chats = []

    for saved_chat in all_chats:

        title = (saved_chat.get("title") or T["new_chat"]).strip()

        if not search_query or search_query.casefold() in title.casefold():

            filtered_chats.append(saved_chat)



    if not filtered_chats:

        st.caption("No matching conversations." if not is_arabic else "لا توجد محادثات مطابقة.")



    for saved_chat in filtered_chats:

        title = (saved_chat.get("title") or T["new_chat"]).strip()

        title = title if len(title) <= 25 else title[:22] + "..."

        active = saved_chat["id"] == st.session_state.current_chat_id

        label = ("✦  " if active else "▢  ") + title



        if st.button(

            label,

            key=f"open_{saved_chat['id']}",

            use_container_width=True,

            type="primary" if active else "secondary",

        ):

            st.session_state.current_chat_id = saved_chat["id"]

            st.rerun()



    st.markdown("---")

    st.markdown(

        '<div class="astra-footer">Astra · Powered by Ollama</div>',

        unsafe_allow_html=True,

    )



# ---------------------------------------------------------

# Main top bar

# ---------------------------------------------------------

online = ollama_online()

status_class = "astra-status" if online else "astra-status off"

status_text = T["online"] if online else T["offline"]



st.markdown(

    f"""<div class="astra-topbar">

<div><div class="astra-top-brand">✦ Astra</div><div class="astra-top-sub">YOUR AI, YOUR SPACE.</div></div>

<div class="{status_class}"><span class="astra-status-dot"></span>{status_text} · {T["model"]}</div>

</div>""",

    unsafe_allow_html=True,

)



# ---------------------------------------------------------

# Hero panel (feature cards live inside it, only for empty chats)

# ---------------------------------------------------------

cards_html = ""

if not chat.get("messages"):

    cards_html = f"""<div class="astra-features">

<div class="astra-feature"><div class="astra-feature-icon">ϟ</div><div class="astra-feature-title">{T["local_private"]}</div><div class="astra-feature-desc">{T["local_desc"]}</div></div>

<div class="astra-feature"><div class="astra-feature-icon">▢</div><div class="astra-feature-title">{T["languages"]}</div><div class="astra-feature-desc">{T["languages_desc"]}</div></div>

<div class="astra-feature"><div class="astra-feature-icon">▤</div><div class="astra-feature-title">{T["saved"]}</div><div class="astra-feature-desc">{T["saved_desc"]}</div></div>

<div class="astra-feature"><div class="astra-feature-icon">☆</div><div class="astra-feature-title">{T["your_space"]}</div><div class="astra-feature-desc">{T["space_desc"]}</div></div>

</div>"""



st.markdown(

    f"""<div class="astra-hero" style="direction:{direction}">

<div class="astra-eyebrow">✦ YOUR AI, YOUR SPACE ✦</div>

<h1>{T["welcome"]} ✦</h1>

<p>{T["tagline"]}</p>

{cards_html}

</div>""",

    unsafe_allow_html=True,

)



if not chat.get("messages"):

    st.markdown(

        f"""<h3 style="text-align:center;color:#202452;direction:{direction};margin-top:.6rem">{T["empty_title"]}</h3>

<p style="text-align:center;color:#737CA8;direction:{direction};margin-top:-.35rem">{T["empty_desc"]}</p>""",

        unsafe_allow_html=True,

    )



# ---------------------------------------------------------

# Persist errors across reruns

# ---------------------------------------------------------

if st.session_state.get("chat_error"):

    st.error(st.session_state.chat_error)

    st.session_state.chat_error = None



# ---------------------------------------------------------

# Conversation messages

# ---------------------------------------------------------

for message in chat.get("messages", []):

    role = message.get("role", "assistant")

    content = message.get("content", "")

    if role not in ("user", "assistant"):

        continue



    # "user" keeps Streamlit's built-in user avatar, which our CSS targets.

    avatar = "user" if role == "user" else (str(APP_ICON) if APP_ICON.exists() else "✦")

    with st.chat_message(role, avatar=avatar):

        st.markdown(content)



# ---------------------------------------------------------

# Message composer

# ---------------------------------------------------------

prompt = st.chat_input(T["input"])



if prompt and prompt.strip():

    prompt = prompt.strip()

    chat["messages"].append({"role": "user", "content": prompt})

    chat = update_chat_title(chat)

    save_chat(chat)

    history = chat["messages"][:-1]



    try:

        with st.spinner(T["thinking"]):

            answer = ask_ai(prompt, history=history)



        if not answer or not answer.strip():

            st.session_state.chat_error = T["empty_response"]

        else:

            chat["messages"].append({

                "role": "assistant",

                "content": answer.strip(),

            })

            save_chat(chat)

    except Exception as error:

        print(f"AI request failed: {error}")

        st.session_state.chat_error = T["connection_error"]



    st.rerun()



st.markdown(

    '<div class="astra-footer">Astra · Your AI, Your Space · Powered by Ollama</div>',

    unsafe_allow_html=True,

)
