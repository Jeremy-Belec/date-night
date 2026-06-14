import streamlit as st
import streamlit.components.v1 as components
import base64

def autoplay_audio(file_path):
    with open(file_path, "rb") as f:
        data = f.read()
    b64 = base64.b64encode(data).decode()
    st.markdown(f"""
    <audio autoplay loop style="display:none;">
        <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
    </audio>
    """, unsafe_allow_html=True)

autoplay_audio("static/music/song.mp3")

st.set_page_config(page_title="A question for you 💕", page_icon="💕", layout="centered")

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

.option-label {
    text-align: center;
    color: #5c3357;
    font-family: 'Lora', serif;
    font-size: 1.1rem;
    font-weight: 600;
    margin: 1.2rem 0 0.4rem 0;
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

.verdict-btn a {
    display: inline-block;
    background: linear-gradient(135deg, #f48fb1, #b39ddb);
    color: white !important;
    text-decoration: none;
    padding: 0.8rem 2rem;
    border-radius: 14px;
    font-family: 'Lora', serif;
    font-size: 1.05rem;
    margin-top: 1rem;
}

@keyframes pop {
    0%   { transform: scale(0.5); opacity: 0; }
    70%  { transform: scale(1.1); opacity: 1; }
    100% { transform: scale(1);   opacity: 1; }
}

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
</style>

<script>
// Fireworks canvas — injected once into the page
if (!window._fireworksLoaded) {
    window._fireworksLoaded = true;
    const canvas = document.createElement('canvas');
    canvas.id = 'fireworks-canvas';
    canvas.style.cssText = 'position:fixed;top:0;left:0;width:100%;height:100%;pointer-events:none;z-index:9999;';
    document.body.appendChild(canvas);

    const ctx = canvas.getContext('2d');
    canvas.width  = window.innerWidth;
    canvas.height = window.innerHeight;

    const particles = [];
    const colors = ['#f48fb1','#b39ddb','#fce4ec','#ede7f6','#ff8fab','#c77dff','#ffccd5'];

    function spawnBurst(x, y) {
        for (let i = 0; i < 80; i++) {
            const angle = Math.random() * Math.PI * 2;
            const speed = 2 + Math.random() * 5;
            particles.push({
                x, y,
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
        if (bursts >= 12) return;
        spawnBurst(
            Math.random() * canvas.width,
            Math.random() * canvas.height * 0.7
        );
        bursts++;
        setTimeout(launchRandom, 350);
    }

    function animate() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        for (let i = particles.length - 1; i >= 0; i--) {
            const p = particles[i];
            p.x     += p.vx;
            p.y     += p.vy;
            p.vy    += 0.08;
            p.alpha -= 0.018;
            if (p.alpha <= 0) { particles.splice(i, 1); continue; }
            ctx.globalAlpha = p.alpha;
            ctx.fillStyle   = p.color;
            ctx.beginPath();
            ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
            ctx.fill();
        }
        ctx.globalAlpha = 1;
        if (particles.length > 0 || bursts < 12) requestAnimationFrame(animate);
    }

    launchRandom();
    animate();
}
</script>
""", unsafe_allow_html=True)

# ── Session state init ────────────────────────────────────────────────────────
for key in ["choice", "suboption"]:
    if key not in st.session_state:
        st.session_state[key] = None

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown('<div class="hearts">♥ ♥ ♥</div>', unsafe_allow_html=True)
st.title("Kočičko, mám na tebe důležitou otázku…")
st.markdown("""
<p class="subtitle">
Raději bys šel/šla ven, <br>
nebo bys udělal/a něco útulného? (V obou případech budeme do půlnoci v posteli)
</p>
""", unsafe_allow_html=True)

# ── Top photo ─────────────────────────────────────────────────────────────────
col_l, col_img, col_r = st.columns([1, 2, 1])
with col_img:
    st.image("static/photos/picture_window.jpg", use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Level 1: main choice ──────────────────────────────────────────────────────
col1, col2 = st.columns(2)

with col1:
    if st.button("🛋 Cozy night in", use_container_width=True):
        st.session_state.choice = "cozy"
        st.session_state.suboption = None

with col2:
    if st.button("🍸 Night out", use_container_width=True):
        st.session_state.choice = "out"
        st.session_state.suboption = None

# ── Level 2: suboptions ───────────────────────────────────────────────────────
if st.session_state.choice == "cozy":

    # Reaction photo
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

    # Reaction photo
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

# ── Level 3: final response + verdict button ───────────────────────────────────
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

    if "verdict_clicked" not in st.session_state:
        st.session_state.verdict_clicked = False

    col_l, col_btn, col_r = st.columns([1, 2, 1])
    with col_btn:
        if st.button("Click here for a little  surprise", use_container_width=True):
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
        <div class="finale-message">I can't wait to see you 🥰✨ <br>
        Madame Majestueuse, Formidable, Graçieuse </div>

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
                    particles.push({
                        x, y,
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
                    p.x     += p.vx;
                    p.y     += p.vy;
                    p.vy    += 0.08;
                    p.alpha -= 0.016;
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
        """, height=200)

        col_l, col_img, col_r = st.columns([1, 2, 1])
        with col_img:
            st.image("static/photos/family_picture.jpg", use_container_width=True)

        st.markdown("""
        <div style="text-align:center; margin-top:1.5rem; padding: 0 1rem;">
            <a href="https://www.instagram.com/jay.belec/" target="_blank"
               style="display: block;
                      background: linear-gradient(135deg, #f48fb1, #b39ddb);
                      color: white; text-decoration: none;
                      padding: 1rem 1.5rem;
                      border-radius: 14px;
                      font-family: 'Lora', serif;
                      font-size: 1rem;
                      line-height: 1.5;
                      word-wrap: break-word;">
                Press here to let me know what you picked Laurinka 💕
            </a>
        </div>
        """, unsafe_allow_html=True)

st.markdown('<div class="footer">Vyrobeno s vášní, jen pro vás 💕</div>', unsafe_allow_html=True)
