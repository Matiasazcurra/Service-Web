import base64
import html
from pathlib import Path
from urllib.parse import quote

import streamlit as st
import streamlit.components.v1 as components

# ==========================================================
# CONFIGURACIÓN
# ==========================================================
st.set_page_config(
    page_title="Maxi Service",
    page_icon="🔌",
    layout="wide",
    initial_sidebar_state="collapsed",
)

APP_DIR = Path(__file__).resolve().parent
LOGO_PATH = APP_DIR / "Logo.png"


def _logo_data_uri(path: Path) -> str | None:
    """Devuelve una data-URI base64 para incrustar el logo dentro de HTML (opcional)."""
    try:
        if not path.exists():
            return None

        data = path.read_bytes()
        b64 = base64.b64encode(data).decode("ascii")

        ext = path.suffix.lower().lstrip(".") or "png"
        if ext == "jpg":
            ext = "jpeg"
        if ext not in {"png", "jpeg", "webp"}:
            ext = "png"

        return f"data:image/{ext};base64,{b64}"
    except Exception:
        return None


LOGO_URI = _logo_data_uri(LOGO_PATH)

# ==========================================================
# ESTILOS (DISEÑO)
# ==========================================================
CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');

:root {
  --bg: #0b1220;
  --surface: rgba(255,255,255,0.055);
  --surface2: rgba(255,255,255,0.075);
  --border: rgba(255,255,255,0.11);
  --text: #f5f7ff;
  --muted: rgba(245,247,255,0.70);
  --accent: #4caf50;
  --accent2: #2196f3;
  --danger: #ff4b4b;
  --shadow: 0 14px 38px rgba(0,0,0,.35);
  --radius: 16px;
}

html, body, [class*="css"] {
  font-family: 'Inter', sans-serif;
}

.stApp {
  background:
    radial-gradient(900px circle at 15% 10%, rgba(33,150,243,0.20), transparent 45%),
    radial-gradient(900px circle at 85% 0%, rgba(76,175,80,0.18), transparent 45%),
    radial-gradient(900px circle at 10% 95%, rgba(255,75,75,0.10), transparent 50%),
    var(--bg);
  color: var(--text);
}

/* BOTÓN FLOTANTE WHATSAPP */
.float-whatsapp {
    position: fixed;
    width: 60px;
    height: 60px;
    bottom: 40px;
    right: 40px;
    background-color: #25d366;
    color: #FFF !important;
    border-radius: 50px;
    text-align: center;
    font-size: 30px;
    box-shadow: 2px 2px 10px rgba(0,0,0,0.5);
    z-index: 1000;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 0.3s ease;
    text-decoration: none !important;
}
.float-whatsapp:hover {
    background-color: #128C7E;
    transform: scale(1.1);
}
.float-whatsapp img {
    width: 35px;
}

/* Espaciado general */
div.block-container {
  padding-top: 1.2rem;
  padding-bottom: 2.5rem;
  max-width: 1200px;
}

/* Ocultar UI default */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* Ajustes tipográficos */
[data-testid="stMarkdownContainer"] p {
  color: rgba(245,247,255,0.90);
}
[data-testid="stMarkdownContainer"] small,
[data-testid="stMarkdownContainer"] .caption {
  color: var(--muted) !important;
}

/* --- BOTONES REDES SOCIALES --- */
.social-btn {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 100%;
    background: rgba(255,255,255,0.05);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 10px 0;
    text-decoration: none !important;
    transition: transform 0.2s, background 0.2s;
    color: white !important;
    font-weight: 600;
}
.social-btn:hover {
    transform: translateY(-2px);
    background: rgba(255,255,255,0.1);
    box-shadow: 0 4px 12px rgba(0,0,0,0.2);
}
.social-btn img {
    width: 24px;
    height: 24px;
    margin-right: 10px;
    display: block;
}

/* Hero */
.hero {
  display: grid;
  grid-template-columns: 140px 1fr 320px;
  gap: 18px;
  padding: 20px;
  border-radius: var(--radius);
  border: 1px solid var(--border);
  background: linear-gradient(135deg, rgba(255,255,255,0.07), rgba(255,255,255,0.03));
  box-shadow: var(--shadow);
  align-items: center;
}

.hero__logo {
  display:flex;
  align-items:center;
  justify-content:center;
}

.hero-logo {
  width: 120px;
  height: 120px;
  border-radius: 18px;
  background: rgba(255,255,255,0.95);
  padding: 10px;
  object-fit: contain;
  border: 1px solid rgba(255,255,255,0.18);
}

.hero-logo--placeholder {
  display:flex;
  align-items:center;
  justify-content:center;
  font-size: 52px;
  color: var(--text);
  background: rgba(255,255,255,0.08);
}

.hero__title {
  font-size: 2.35rem;
  font-weight: 900;
  letter-spacing: 0.8px;
  line-height: 1.05;
  margin-bottom: 6px;
  background: linear-gradient(to right, #ff4b4b, #ffa500, #4caf50, #2196f3, #9c27b0);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.hero__subtitle {
  font-size: 1.05rem;
  color: var(--muted);
  font-weight: 700;
  margin-bottom: 10px;
}

.hero__text {
  font-size: 0.98rem;
  color: rgba(245,247,255,0.82);
  line-height: 1.45;
}

.hero__badges {
  margin-top: 12px;
  display:flex;
  flex-wrap:wrap;
  gap: 8px;
}

.ms-badge {
  display:inline-flex;
  align-items:center;
  gap: 6px;
  padding: 5px 10px;
  border-radius: 999px;
  border: 1px solid rgba(255,255,255,0.14);
  background: rgba(0,0,0,0.18);
  color: rgba(245,247,255,0.86);
  font-size: 0.85rem;
  font-weight: 700;
}

.hero__info {
  display:flex;
  justify-content:flex-end;
}

/* Info card */
.info-card {
  width: 100%;
  border-radius: 14px;
  border: 1px solid rgba(255,255,255,0.10);
  background: rgba(0,0,0,0.22);
  padding: 14px;
}

.info-card__title {
  font-weight: 900;
  margin-bottom: 10px;
}

.info-row {
  display:flex;
  gap: 10px;
  margin: 7px 0;
  color: rgba(245,247,255,0.82);
}

.info-ico {
  width: 18px;
  opacity: 0.9;
}

/* Títulos de sección */
.section-title {
  font-weight: 900;
  font-size: 1.25rem;
  margin: 0.2rem 0 0.8rem 0;
}

.section-spacer { height: 10px; }

/* Cards */
.ms-card {
  border-radius: var(--radius);
  border: 1px solid var(--border);
  background: linear-gradient(180deg, rgba(255,255,255,0.06), rgba(255,255,255,0.03));
  box-shadow: 0 10px 26px rgba(0,0,0,0.28);
  overflow: hidden;
  transition: transform .16s ease, border-color .16s ease, box-shadow .16s ease;
  margin-bottom: 18px;
}

.ms-card:hover {
  transform: translateY(-3px);
  border-color: rgba(33,150,243,0.55);
  box-shadow: 0 16px 34px rgba(0,0,0,0.36);
}

.ms-card__media {
  height: 210px;
  background: rgba(255,255,255,0.08);
}

.ms-card__media img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.ms-card__body {
  padding: 14px 16px 16px 16px;
}

.ms-card__title {
  font-weight: 900;
  font-size: 1.05rem;
  margin-bottom: 8px;
}

.ms-card__desc {
  color: rgba(245,247,255,0.80);
  line-height: 1.45;
  font-size: 0.93rem;
}

/* Variante: service */
.ms-card--service .ms-card__media {
  height: 96px;
  display:flex;
  align-items:center;
  justify-content:center;
}

/* Añadir cursor pointer para servicios clicables */
.ms-card--service {
    cursor: pointer;
}

.ms-icon {
  font-size: 44px;
  filter: drop-shadow(0 12px 18px rgba(0,0,0,0.35));
}

/* Form */
div[data-testid="stForm"] {
  border: 1px solid rgba(255,255,255,0.10);
  border-radius: var(--radius);
  padding: 16px 16px 6px 16px;
  background: rgba(0,0,0,0.20);
}

/* Responsive */
@media (max-width: 1100px) {
  .hero { grid-template-columns: 120px 1fr; }
  .hero__info { grid-column: 1 / -1; }
}
@media (max-width: 650px) {
  div.block-container { padding-left: 0.9rem; padding-right: 0.9rem; }
  .hero { grid-template-columns: 1fr; }
  .hero__logo { justify-content:flex-start; }
  .hero-logo { width: 96px; height: 96px; }
}
</style>
"""

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# HTML del Botón Flotante
st.markdown("""
<a href="https://wa.me/595961843932" class="float-whatsapp" target="_blank">
    <img src="https://upload.wikimedia.org/wikipedia/commons/6/6b/WhatsApp.svg" alt="WhatsApp">
</a>
""", unsafe_allow_html=True)


def _badge(text: str) -> str:
    return f"<span class='ms-badge'>{html.escape(text)}</span>"


def render_hero() -> None:
    if LOGO_URI:
        logo_html = f"<img class='hero-logo' src='{LOGO_URI}' alt='Maxi Service'/>"
    else:
        logo_html = "<div class='hero-logo hero-logo--placeholder'>🔌</div>"

    st.markdown(
        f"""
        <div class="hero">
          <div class="hero__logo">{logo_html}</div>
          <div class="hero__content">
            <div class="hero__title">MAXI SERVICE</div>
            <div class="hero__subtitle">🛠️ Soluciones electrónicas profesionales</div>
            <div class="hero__text">
              Especialistas en reparación de televisores, monitores y consolas.<br/>
              Reballing, micro-soldadura y diagnóstico con equipamiento de precisión.
            </div>
            <div class="hero__badges">
              {_badge('Reballing')}
              {_badge('Micro-soldadura')}
              {_badge('Consolas')}
              {_badge('Monitores')}
              {_badge('Asunción')}
            </div>
          </div>
          <div class="hero__info">
            <div class="info-card">
              <div class="info-card__title">📍 Contacto</div>
              <div class="info-row"><span class="info-ico">🏢</span><span>Dr. Emiliano Paiva 2056, Asunción</span></div>
              <div class="info-row"><span class="info-ico">📞</span><span>+595 0961 843932</span></div>
              <div class="info-row"><span class="info-ico">⏰</span><span>Lun a Vie 08:30 – 19:00</span></div>
            </div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_card(title: str, desc: str, img_url: str, variant: str = "") -> None:
    safe_title = html.escape(title)
    safe_desc = html.escape(desc)
    safe_img = html.escape(img_url, quote=True)

    st.markdown(
        f"""
        <div class="ms-card {variant}">
          <div class="ms-card__media">
            <img src="{safe_img}" alt="{safe_title}" loading="lazy"/>
          </div>
          <div class="ms-card__body">
            <div class="ms-card__title">{safe_title}</div>
            <div class="ms-card__desc">{safe_desc}</div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_service_card(icon: str, title: str, desc: str, link: str = None) -> None:
    safe_title = html.escape(title)
    safe_desc = html.escape(desc)

    card_html = f"""
        <div class="ms-card ms-card--service">
          <div class="ms-card__media"><div class="ms-icon">{html.escape(icon)}</div></div>
          <div class="ms-card__body">
            <div class="ms-card__title">{safe_title}</div>
            <div class="ms-card__desc">{safe_desc}</div>
          </div>
        </div>
    """

    if link:
        st.markdown(f'<a href="{link}" target="_blank" style="text-decoration: none; color: inherit;">{card_html}</a>', unsafe_allow_html=True)
    else:
        st.markdown(card_html, unsafe_allow_html=True)


# ==========================================================
# UI
# ==========================================================
render_hero()

st.markdown("<div class='section-spacer'></div>", unsafe_allow_html=True)
st.markdown("<div class='section-title'>📱 Contacto directo</div>", unsafe_allow_html=True)

c1, c2 = st.columns(2, gap="small")

with c1:
    st.markdown("""
    <a href="https://wa.me/595961843932" target="_blank" class="social-btn">
        <img src="https://upload.wikimedia.org/wikipedia/commons/6/6b/WhatsApp.svg" alt="WhatsApp">
        WhatsApp
    </a>
    """, unsafe_allow_html=True)

with c2:
    st.markdown("""
    <a href="https://www.google.com/maps/search/?api=1&query=Dr.%20Emiliano%20Paiva%202056%2C%20Asunci%C3%B3n" target="_blank" class="social-btn">
        <img src="https://upload.wikimedia.org/wikipedia/commons/a/aa/Google_Maps_icon_%282020%29.svg" alt="Maps">
        Ubicación en Mapa
    </a>
    """, unsafe_allow_html=True)

st.divider()

# Navegación por secciones
TAB_INICIO, TAB_SERV, TAB_PORT = st.tabs(["🏠 Inicio", "🧰 Servicios", "🔧 Portafolio"])

with TAB_INICIO:
    st.markdown("<div class='section-title'>¿Qué hacemos?</div>", unsafe_allow_html=True)
    st.write(
        "Reparación electrónica orientada a resultados: diagnóstico, reparación y prueba. "
        "Priorizamos calidad, trazabilidad del trabajo y comunicación clara con el cliente."
    )

    a, b, c = st.columns(3, gap="large")
    with a:
        render_service_card("⚡", "Diagnóstico preciso", "Evaluación técnica y propuesta de solución con claridad.")
    with b:
        render_service_card("🔬", "Micro-soldadura", "Reparación de placas, conectoras y componentes SMD.")
    with c:
        render_service_card("🧩", "Reballing", "Reparación avanzada en equipos que lo requieren (según caso).")

with TAB_SERV:
    st.markdown("<div class='section-title'>Servicios</div>", unsafe_allow_html=True)
    
    wa_direct = "https://wa.me/595961843932"

    s1, s2, s3 = st.columns(3, gap="large")
    with s1:
        render_service_card("📺", "TV y monitores", "Backlight, fuentes, mainboard...", link=wa_direct)
    with s2:
        render_service_card("🎮", "Consolas", "Reparación HDMI, puertos, limpieza...", link=wa_direct)
    with s3:
        render_service_card("💻", "Equipos electrónicos", "Mantenimiento y reparación de placas...", link=wa_direct)

    st.info("💡 Consejo: al hacer clic en un servicio, podrás consultarnos directamente por WhatsApp.")

with TAB_PORT:
    st.markdown("<div class='section-title'>Portafolio de reparaciones</div>", unsafe_allow_html=True)
    
    trabajos = [
        {"titulo": "Samsung 4K", "desc": "Cambio de backlight.", "img": "https://images.unsplash.com/photo-1593359677879-a4bb92f829d1?auto=format&fit=crop&q=80&w=1200"},
        {"titulo": "Mantenimiento PC", "desc": "Limpieza y pasta térmica.", "img": "https://images.unsplash.com/photo-1587202372775-e229f172b9d7?auto=format&fit=crop&q=80&w=1200"},
        {"titulo": "iPhone", "desc": "Micro-soldadura de carga.", "img": "https://images.unsplash.com/photo-1511385348-a52b4a160dc2?auto=format&fit=crop&q=80&w=1200"},
        {"titulo": "PS5", "desc": "Puerto HDMI nuevo.", "img": "https://images.unsplash.com/photo-1605901309584-818e25960b8f?auto=format&fit=crop&q=80&w=1200"},
    ]

    cols = st.columns(2, gap="large")
    for idx, t in enumerate(trabajos):
        with cols[idx % 2]:
            render_card(t["titulo"], t["desc"], t["img"])

# ==========================================================
# CONTACTO SIEMPRE VISIBLE (AL FINAL)
# ==========================================================
st.divider()
st.markdown("<div class='section-title'>📞 Contacto</div>", unsafe_allow_html=True)

c_left, c_right = st.columns([1.1, 1], gap="large")

with c_left:
    st.markdown("#### 📩 Enviar consulta por WhatsApp")
    with st.form("contact_form", clear_on_submit=False):
        nombre = st.text_input("Nombre")
        equipo = st.text_input("Equipo / Modelo")
        problema = st.text_area("Describe el problema", height=120)
        submit = st.form_submit_button("Generar mensaje")

    if submit:
        msg = f"¡Hola! Soy {nombre or '(sin nombre)'}, soporte para: {equipo or '(sin equipo)'}. Problema: {problema or '(sin descripción)'}"
        wa_url = f"https://wa.me/+595961843932?text={quote(msg)}"
        st.success("Mensaje preparado.")
        st.link_button("💬 Abrir WhatsApp", wa_url, use_container_width=True)

with c_right:
    st.markdown("#### 📍 Ubicación y Datos")
    components.iframe("https://www.google.com/maps?q=Dr.%20Emiliano%20Paiva%202056%2C%20Asunci%C3%B3n&output=embed", height=280)
    
    st.markdown(f"""
    <div class="info-card">
        <div class="info-row"><span class="info-ico">🏢</span><span>Dr. Emiliano Paiva 2056, Asunción</span></div>
        <div class="info-row"><span class="info-ico">📞</span><span>+595 0961 843932</span></div>
        <div class="info-row"><span class="info-ico">⏰</span><span>Lun a Vie 08:30 – 19:00</span></div>
    </div>
    """, unsafe_allow_html=True)

st.divider()
st.markdown("<div style='text-align: center; color: rgba(245,247,255,0.65); padding: 14px 0;'><small>Todos los derechos reservados © 2026 Maxi Service Paraguay</small></div>", unsafe_allow_html=True)
