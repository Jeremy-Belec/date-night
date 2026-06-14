import streamlit as st
import streamlit.components.v1 as components
import base64
import os

# ── Page config MUST be first ─────────────────────────────────────────────────
st.set_page_config(page_title="A question for you 💕", page_icon="💕", layout="centered")

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Lora:ital,wght@0,400;0,600;1,400&display=swap');

html, body, [data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #fff0f5 0%, #fce4ec 50%, #ede7f6 100%) !important;
}

[data-testid="stAppViewContainer"] > .main > div {
    padding-top: 3rem;
}

h1 {
    font-family: 'Lora', serif !important;
    color: #5c3357 !important;
    text-align: center;
}

.subtitle {
    text-align: center;
    color: #a07090;
    font-style: italic;
    font-size: 1.05rem;
    line-height: 1.6;
    margin-bottom: 1.5rem;
}

.hearts {
    text-align: center;
    font-size: 1.8rem;
    letter-spacing: 8px;
    margin-bottom: 1rem;
}

.response-box {
    background: linear-gradient(135deg, #fce4ec, #ede7f6);
    border-radius: 16px;
    padding: 1.2rem 1.5rem;
    text-align: center;
    font-family: 'Lora', serif;
    font-size: 1.05rem;
    color: #5c3357;
    margin-top: 1rem;
    margin-bottom: 1rem;
}

.footer {
    text-align: center;
    color: #c9a0b8;
    font-size: 0.8rem;
    margin-top: 2rem;
}

div[data-testid="column"]:first-child button {
    background-color: #fce4ec !important;
    color: #880e4f !important;
    border: 1.5px solid #f48fb1 !important;
    border-radius: 14px !important;
    font-size: 1rem !important;
    width: 100%;
}

div[data-testid="column"]:last-child button {
    background-color: #ede7f6 !important;
    color: #4527a0 !important;
    border: 1.5px solid #b39ddb !important;
    border-radius: 14px !important;
    font-size: 1rem !important;
    width: 100%;
}
</style>
""", unsafe_allow_html=True)

# ── Background music (YouTube embed, no file needed) ──────────────────────────
components.html("""
<iframe
    src="https://www.youtube.com/embed/HgzGwKwLmgM?autoplay=1&loop=1&playlist=HgzGwKwLmgM&controls=0&mute=0"
    allow="autoplay"
    style="width:1px;height:1px;position:fixed;top:-100px;left:-100px;border:none;">
</iframe>
<div style="text-align:center; font-family:serif; color:#a07090; font-size:0.85rem;">
    🎵 Je te laisserai des mots — Patrick Watson
</div>
""", height=40)

# ── Session state init ────────────────────────────────────────────────────────
for key in ["choice", "suboption", "verdict_clicked"]:
    if key not in st.session_state:
        st.session_state[key] = None
if "verdict_clicked" not in st.session_state:
    st.session_state.verdict_clicked = False

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown('<div class="hearts">♥ ♥ ♥</div>', unsafe_allow_html=True)
st.title("Kočičko, mám na tebe důležitou otázku…")
st.markdown("""
<p class="subtitle">
Raději bys šel/šla ven, <br>
nebo bys udělal/a něco útulného? (V obou případech budeme do půlnoci v posteli)
</p>
""", unsafe_allow_html=True)

# ── Slideshow ─────────────────────────────────────────────────────────────────
def img_to_b64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

# List your photos — make sure these filenames match exactly on GitHub
slideshow_photos = [
    "static/photos/picture_window.jpg",
    "static/photos/picture_red_dress_back.jpg",
    "static/photos/picture_selfie1.jpg",
    "static/photos/picture_smile.jpg",
    "static/photos/picture_selfie2.jpg",
]

# Only load photos that actually exist — prevents crash if one is missing
existing_photos = [p for p in slideshow_photos if os.path.exists(p)]

if existing_photos:
    slides_b64 = [img_to_b64(p) for p in existing_photos]
    slides_json = str(slides_b64).replace("'", '"')

    col_l, col_img, col_r = st.columns([1, 2, 1])
    with col_img:
        components.html(f"""
        <style>
            .slideshow-container {{ position: relative; width: 100%; border-radius: 16px; overflow: hidden; }}
            .slide {{ display: none; width: 100%; }}
            .slide img {{ width: 100%; border-radius: 16px; object-fit: cover; }}
            .slide.active {{ display: block; animation: fadein 1.2s ease; }}
            @keyframes fadein {{ from {{ opacity: 0; }} to {{ opacity: 1; }} }}
        </style>
        <div class="slideshow-container" id="slideshow"></div>
        <script>
            const photos = {slides_json};
            const container = document.getElementById('slideshow');
            photos.forEach((b64, i) => {{
                const div = document.createElement('div');
                div.className = 'slide' + (i === 0 ? ' active' : '');
                div.innerHTML = '<img src="data:image/jpeg;base64,' + b64 + '" />';
                container.appendChild(div);
            }});
            let current = 0;
            function nextSlide() {{
                const slides = document.querySelectorAll('.slide');
                slides[current].classList.remove('active');
                current = (current + 1) % slides.length;
                slides[current].classList.add('active');
            }}
            setInterval(nextSlide, 2000);
        </script>
        """, height=350)
else:
    st.markdown("""
    <div style="text-align:center; color:#c9a0b8; font-size:0.85rem; margin-bottom:1rem;">
        📷 Photos loading…
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Level 1: main choice ──────────────────────────────────────────────────────
col1, col2 = st.columns(2)

with col1:
    if st.button("🛋 Cozy night in", use_container_width=True):
        st.session_state.choice = "cozy"
        st.session_state.suboption = None
        st.session_state.verdict_clicked = False

with col2:
    if st.button("🍸 Night out", use_container_width=True):
        st.session_state.choice = "out"
        st.session_state.suboption = None
        st.session_state.verdict_clicked = False

# ── Level 2: suboptions ───────────────────────────────────────────────────────
if st.session_state.choice == "cozy":

    col_l, col_img, col_r = st.columns([1, 2, 1])
    with col_img:
        st.image("static/photos/picture_shy.jpg", use_container_width=True)

    st.markdown("""
    <div class="response-box">
        OH YEAHHH! 🛋️ Blankets, snacks, and a movie it is — now pick the vibe:
    </div>
    """, unsafe_allow_html=True)

    col3, col4 = st.columns(2)
    with col3:
        if st.button("✨ Option A — Light\n\n1981, games & cuddles", use_container_width=True):
            st.session_state.suboption = "cozy_a"
    with col4:
        if st.button("🥃 Option B — Deep\n\nOppenheimer + vodka & the presentation", use_container_width=True):
            st.session_state.suboption = "cozy_b"

elif st.session_state.choice == "out":

    col_l, col_img, col_r = st.columns([1, 2, 1])
    with col_img:
        st.image("static/photos/picture_red_dress_front.jpg", use_container_width=True)

    st.markdown("""
    <div class="response-box">
        Love it! 🍸 Let's go out — now pick the vibe:
    </div>
    """, unsafe_allow_html=True)

    col3, col4 = st.columns(2)
    with col3:
        if st.button("🍕 Option A — Cute\n\nRemake of our first date: Bar Mal Nécessaire, discussions & chicken pizza", use_container_width=True):
            st.session_state.suboption = "out_a"
    with col4:
        if st.button("🎤 Option B — Fun\n\nKaraoke with drinks and your amazing voice", use_container_width=True):
            st.session_state.suboption = "out_b"

# ── Level 3: final response + fireworks ───────────────────────────────────────
final_messages = {
    "cozy_a": "🎮 Games, cuddles and 1981 — the most perfect soft evening. I'm already excited 🥰",
    "cozy_b": "🎬 Oppenheimer, vodka, and the presentation… a whole experience. Let's do it 🥃",
    "out_a":  "🍕 Back to where it all started — Mal Nécessaire, chicken pizza and us. I love this 💕",
    "out_b":  "🎤 Karaoke it is! Can't wait to hear you sing your heart out 🎶✨",
}

if st.session_state.suboption:
    st.markdown(f"""
    <div class="response-box">{final_messages[st.session_state.suboption]}</div>
    """, unsafe_allow_html=True)

    col_l, col_btn, col_r = st.columns([1, 2, 1])
    with col_btn:
        if st.button("Click here for a little surprise 🎁", use_container_width=True):
            st.session_state.verdict_clicked = True

    if st.session_state.verdict_clicked:
        components.html("""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Lora:wght@400;600&display=swap');
            body { margin: 0; background: transparent; }
            canvas { position: fixed; top: 0; left: 0; width: 100%; height: 100%;
                     pointer-events: none; z-index: 9999; }
            .finale-message {
                animation: pop 0.6s ease forwards;
                background: linear-gradient(135deg, #fce4ec, #ede7f6);
                border-radius: 20px;
                padding: 1.5rem;
                text-align: center;
                font-family: 'Lora', serif;
                font-size: 1.3rem;
                color: #5c3357;
                margin-top: 1rem;
            }
            @keyframes pop {
                0%   { transform: scale(0.5); opacity: 0; }
                70%  { transform: scale(1.1); opacity: 1; }
                100% { transform: scale(1);   opacity: 1; }
            }
        </style>
        <canvas id="fireworks-canvas"></canvas>
        <div class="finale-message">
            I can't wait to see you 🥰✨<br>
            Madame Majestueuse, Formidable, Gracieuse
        </div>
        <script>
            const canvas = document.getElementById('fireworks-canvas');
            const ctx    = canvas.getContext('2d');
            canvas.width  = window.innerWidth;
            canvas.height = window.innerHeight;
            const colors = ['#f48fb1','#b39ddb','#fce4ec','#ff8fab','#c77dff','#ffccd5','#ffd6e0'];
            const particles = [];
            function spawnBurst(x, y) {
                for (let i = 0; i < 80; i++) {
                    const angle = Math.random() * Math.PI * 2;
                    const speed = 2 + Math.random() * 5;
                    particles.push({ x, y,
                        vx: Math.cos(angle) * speed,
                        vy: Math.sin(angle) * speed,
                        alpha: 1,
                        color: colors[Math.floor(Math.random() * colors.length)],
                        radius: 3 + Math.random() * 3
                    });
                }
            }
            let bursts = 0;
            function launchRandom() {
                if (bursts >= 14) return;
                spawnBurst(
                    100 + Math.random() * (canvas.width - 200),
                    50  + Math.random() * (canvas.height * 0.6)
                );
                bursts++;
                setTimeout(launchRandom, 300);
            }
            function animate() {
                ctx.clearRect(0, 0, canvas.width, canvas.height);
                for (let i = particles.length - 1; i >= 0; i--) {
                    const p = particles[i];
                    p.x += p.vx; p.y += p.vy; p.vy += 0.08; p.alpha -= 0.016;
                    if (p.alpha <= 0) { particles.splice(i, 1); continue; }
                    ctx.globalAlpha = p.alpha;
                    ctx.fillStyle   = p.color;
                    ctx.beginPath();
                    ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
                    ctx.fill();
                }
                ctx.globalAlpha = 1;
                requestAnimationFrame(animate);
            }
            launchRandom();
            animate();
        </script>
        """, height=220)

        col_l, col_img, col_r = st.columns([1, 2, 1])
        with col_img:
            st.image("static/photos/family_picture.jpg", use_container_width=True)

        col_l, col_btn, col_r = st.columns([1, 2, 1])
        with col_btn:
            if st.button("Press here to let me know\nwhat you picked Laurinka 💕", use_container_width=True):
                st.markdown("""
                <meta http-equiv="refresh" content="0; url=https://www.instagram.com/jay.belec/" />
                """, unsafe_allow_html=True)

st.markdown('<div class="footer">Vyrobeno s vášní, jen pro vás 💕</div>', unsafe_allow_html=True)
