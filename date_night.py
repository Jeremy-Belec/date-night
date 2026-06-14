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
# Load song.mp3 as base64
song_b64 = ""
song_path = "static/music/song.mp3"
if os.path.exists(song_path):
    with open(song_path, "rb") as f:
        song_b64 = base64.b64encode(f.read()).decode()

components.html(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Lora:wght@400&display=swap');
    .music-bar {{
        text-align: center;
        margin-bottom: 0.5rem;
    }}
    .music-btn {{
        background: linear-gradient(135deg, #fce4ec, #ede7f6);
        border: 1.5px solid #f48fb1;
        border-radius: 20px;
        padding: 0.5rem 1.5rem;
        font-family: 'Lora', serif;
        font-size: 0.9rem;
        color: #880e4f;
        cursor: pointer;
        transition: opacity 0.3s;
    }}
    .music-btn:hover {{ opacity: 0.8; }}
    .music-label {{
        font-family: 'Lora', serif;
        color: #a07090;
        font-size: 0.8rem;
        margin-top: 0.3rem;
    }}
</style>

<div class="music-bar">
    <button class="music-btn" onclick="startMusic()" id="playBtn">
        🎵 Play our song
    </button>
    <div class="music-label">Je te laisserai des mots — Patrick Watson</div>
</div>

<audio id="player" loop>
    <source src="data:audio/mp3;base64,{song_b64}" type="audio/mp3">
</audio>

<script>
    function startMusic() {{
        const player = document.getElementById('player');
        player.play();
        document.getElementById('playBtn').textContent = '🎵 Playing…';
        document.getElementById('playBtn').disabled = true;
        document.getElementById('playBtn').style.opacity = '0.6';
    }}
</script>
""", height=80)

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
        .slide img {{
            width: 100%;
            height: auto;
            border-radius: 16px;
            object-fit: contain;
            display: block;
        }}
        .slide.active {{ display: block; animation: fadein 2.0s ease; }}
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

        // Auto-resize the iframe height to fit the image naturally
        function resizeToImage() {{
            const img = container.querySelector('.slide.active img');
            if (img && img.complete) {{
                const ratio = img.naturalHeight / img.naturalWidth;
                const width = container.offsetWidth;
                window.frameElement.style.height = Math.round(width * ratio) + 'px';
            }}
        }}

        // Resize on each slide change
        const originalNext = nextSlide;
        function nextSlideWithResize() {{
            originalNext();
            setTimeout(resizeToImage, 100);
        }}
        setInterval(nextSlideWithResize, 4000);

        // Resize on first load
        window.addEventListener('load', () => setTimeout(resizeToImage, 200));
    </script>
    """, height=500)
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

            const colors = ['#f48fb1','#b39ddb','#ff8fab','#c77dff','#ffccd5','#ffd6e0','#ffffff'];
            const rockets    = [];
            const particles  = [];

            // Rocket that flies up then explodes
            function spawnRocket() {
                rockets.push({
                    x: 100 + Math.random() * (canvas.width - 200),
                    y: canvas.height,
                    vy: -(9 + Math.random() * 6),
                    color: colors[Math.floor(Math.random() * colors.length)],
                    targetY: 60 + Math.random() * (canvas.height * 0.45)
                });
            }

            // Explosion: mix of circle sparks and hearts
            function explode(x, y, color) {
                for (let i = 0; i < 120; i++) {
                    const angle = Math.random() * Math.PI * 2;
                    const speed = 1.5 + Math.random() * 7;
                    const isHeart = Math.random() < 0.35; // 35% hearts, 65% sparks
                    particles.push({
                        x, y,
                        vx: Math.cos(angle) * speed,
                        vy: Math.sin(angle) * speed,
                        alpha: 1,
                        color,
                        radius: isHeart ? 6 + Math.random() * 6 : 3 + Math.random() * 4,
                        isHeart
                    });
                }
            }

            function drawHeart(x, y, size) {
                ctx.save();
                ctx.translate(x, y);
                ctx.beginPath();
                ctx.moveTo(0, -size * 0.5);
                ctx.bezierCurveTo( size,  -size * 1.2,  size * 1.8,  size * 0.5, 0,  size * 1.2);
                ctx.bezierCurveTo(-size * 1.8,  size * 0.5, -size, -size * 1.2, 0, -size * 0.5);
                ctx.fill();
                ctx.restore();
            }

            function animate() {
                ctx.clearRect(0, 0, canvas.width, canvas.height);

                // Draw rockets
                for (let i = rockets.length - 1; i >= 0; i--) {
                    const r = rockets[i];
                    r.y += r.vy;
                    // Rocket trail
                    ctx.globalAlpha = 0.9;
                    ctx.fillStyle = r.color;
                    ctx.beginPath();
                    ctx.arc(r.x, r.y, 3, 0, Math.PI * 2);
                    ctx.fill();
                    // Explode when reaching target
                    if (r.y <= r.targetY) {
                        explode(r.x, r.y, r.color);
                        rockets.splice(i, 1);
                    }
                }

                // Draw particles
                for (let i = particles.length - 1; i >= 0; i--) {
                    const p = particles[i];
                    p.x += p.vx;
                    p.y += p.vy;
                    p.vy += 0.07;
                    p.alpha -= 0.013;
                    if (p.alpha <= 0) { particles.splice(i, 1); continue; }
                    ctx.globalAlpha = p.alpha;
                    ctx.fillStyle   = p.color;
                    if (p.isHeart) {
                        drawHeart(p.x, p.y, p.radius);
                    } else {
                        ctx.beginPath();
                        ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
                        ctx.fill();
                    }
                }

                ctx.globalAlpha = 1;
                requestAnimationFrame(animate);
            }

            // Launch rockets one by one
            let launched = 0;
            function launchNext() {
                if (launched >= 12) return;
                spawnRocket();
                launched++;
                setTimeout(launchNext, 400);
            }

            launchNext();
            animate();
        </script>
        """, height=220)

        col_l, col_img, col_r = st.columns([1, 2, 1])
        with col_img:
            st.image("static/photos/family_picture.jpg", use_container_width=True)

        st.markdown("""
        <div style="text-align:center; margin-top:1rem; padding: 0 1rem;">
            <a href="https://www.instagram.com/jay.belec/" target="_blank"
               style="display:block;
                      background: linear-gradient(135deg, #f48fb1, #b39ddb);
                      color: white;
                      text-decoration: none;
                      padding: 1rem 1.5rem;
                      border-radius: 14px;
                      font-family: 'Lora', serif;
                      font-size: 1rem;
                      line-height: 1.6;
                      text-align: center;">
                Press here to let me know<br>what you picked Laurinka 💕
            </a>
        </div>
        """, unsafe_allow_html=True)

st.markdown('<div class="footer">💕 Vyrobeno s vášní, jen pro vás 💕<br>
 PS: ma mère nous a cuisiné une surprise </div>', unsafe_allow_html=True)
