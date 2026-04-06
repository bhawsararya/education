import streamlit as st
from llm import generate_explanation
from image_gen import generate_image

# Initialize session state for interactivity
if 'generated_content' not in st.session_state:
    st.session_state.generated_content = []
if 'current_topic' not in st.session_state:
    st.session_state.current_topic = ""
if 'favorites' not in st.session_state:
    st.session_state.favorites = []

st.set_page_config(
    page_title="Multimodal Education Creator", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for beautiful black theme UI
st.markdown("""
<style>
    /* Dark theme colors */
    :root {
        --primary-color: #8b5cf6;
        --secondary-color: #ec4899;
        --accent-color: #06b6d4;
        --background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 50%, #16213e 100%);
        --card-bg: rgba(30, 30, 46, 0.95);
        --card-hover: rgba(40, 40, 60, 0.95);
        --text-primary: #f8fafc;
        --text-secondary: #cbd5e1;
        --border-color: rgba(139, 92, 246, 0.3);
        --glow-color: rgba(139, 92, 246, 0.5);
    }

    /* Body and container styling */
    .stApp {
        background: var(--background);
        background-attachment: fixed;
        color: var(--text-primary);
    }
    
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
        background: transparent;
    }

    /* Hide default streamlit background */
    .stApp > div {
        background: transparent;
    }

    /* Header styling */
    .title-header {
        text-align: center;
        margin-bottom: 3rem;
        animation: fadeInDown 1s ease-out;
        position: relative;
    }
    
    .title-header h1 {
        font-size: 4rem !important;
        font-weight: 800 !important;
        background: linear-gradient(45deg, var(--primary-color), var(--secondary-color), var(--accent-color));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 0 30px rgba(139, 92, 246, 0.5);
        margin-bottom: 1rem;
        letter-spacing: -0.02em;
        animation: glow 3s ease-in-out infinite alternate;
    }
    
    @keyframes glow {
        from { text-shadow: 0 0 30px rgba(139, 92, 246, 0.5); }
        to { text-shadow: 0 0 40px rgba(236, 72, 153, 0.8), 0 0 50px rgba(6, 182, 212, 0.6); }
    }
    
    .subtitle {
        font-size: 1.3rem !important;
        color: var(--text-secondary) !important;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: 300;
        letter-spacing: 0.05em;
    }

    /* Card styling */
    .card {
        background: var(--card-bg);
        border-radius: 24px;
        padding: 2.5rem;
        box-shadow: 0 25px 50px rgba(0, 0, 0, 0.5), 
                    0 0 0 1px var(--border-color),
                    inset 0 1px 0 rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(20px);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        animation: fadeInUp 1s ease-out;
        position: relative;
        overflow: hidden;
    }
    
    .card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 1px;
        background: linear-gradient(90deg, transparent, var(--primary-color), transparent);
        animation: shimmer 3s infinite;
    }
    
    @keyframes shimmer {
        0% { transform: translateX(-100%); }
        100% { transform: translateX(100%); }
    }
    
    .card:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow: 0 35px 70px rgba(0, 0, 0, 0.7), 
                    0 0 30px var(--glow-color),
                    inset 0 1px 0 rgba(255, 255, 255, 0.2);
        background: var(--card-hover);
    }

    /* Input styling */
    .stTextInput > div > div > input {
        background: rgba(20, 20, 35, 0.8);
        border: 2px solid var(--border-color);
        border-radius: 16px;
        padding: 16px 20px;
        font-size: 16px;
        color: var(--text-primary);
        transition: all 0.3s ease;
        backdrop-filter: blur(10px);
        box-shadow: inset 0 2px 10px rgba(0, 0, 0, 0.3);
    }
    
    .stTextInput > div > div > input:focus {
        border-color: var(--primary-color);
        box-shadow: 0 0 0 3px rgba(139, 92, 246, 0.2), 
                    inset 0 2px 10px rgba(0, 0, 0, 0.3);
        outline: none;
        background: rgba(25, 25, 40, 0.9);
    }
    
    .stTextInput > div > div > input::placeholder {
        color: var(--text-secondary);
        opacity: 0.7;
    }

    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, var(--primary-color), var(--secondary-color)) !important;
        color: white !important;
        border: none !important;
        border-radius: 16px !important;
        padding: 16px 32px !important;
        font-weight: 700 !important;
        font-size: 16px !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 8px 25px rgba(139, 92, 246, 0.4), 
                    0 0 20px rgba(139, 92, 246, 0.2) !important;
        text-transform: none !important;
        letter-spacing: 0.05em;
        position: relative;
        overflow: hidden;
    }
    
    .stButton > button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
        transition: left 0.5s;
    }
    
    .stButton > button:hover::before {
        left: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-4px) scale(1.05) !important;
        box-shadow: 0 12px 35px rgba(139, 92, 246, 0.6), 
                    0 0 30px rgba(236, 72, 153, 0.4) !important;
        background: linear-gradient(135deg, var(--secondary-color), var(--accent-color)) !important;
    }

    /* Content area styling */
    .content-card {
        background: var(--card-bg);
        border-radius: 20px;
        padding: 2rem;
        margin: 1.5rem 0;
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.4), 
                    0 0 0 1px var(--border-color),
                    inset 0 1px 0 rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(20px);
        border: 1px solid var(--border-color);
        animation: fadeIn 1s ease-out;
        position: relative;
        transition: all 0.3s ease;
    }
    
    .content-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 20px 45px rgba(0, 0, 0, 0.5), 
                    0 0 20px var(--glow-color);
    }

    /* Markdown content styling */
    .content-card h3 {
        color: var(--primary-color) !important;
        font-size: 1.8rem !important;
        font-weight: 700 !important;
        margin-bottom: 1.5rem !important;
        display: flex;
        align-items: center;
        gap: 0.8rem;
        text-shadow: 0 0 20px rgba(139, 92, 246, 0.5);
    }

    .content-card p, .content-card div {
        color: var(--text-primary) !important;
        line-height: 1.7 !important;
        font-size: 1.05rem !important;
    }

    /* Image styling */
    .stImage > img {
        border-radius: 16px;
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.5), 
                    0 0 20px var(--glow-color);
        transition: all 0.3s ease;
        border: 1px solid var(--border-color);
    }
    
    .stImage > img:hover {
        transform: scale(1.03) rotate(0.5deg);
        box-shadow: 0 20px 45px rgba(0, 0, 0, 0.6), 
                    0 0 30px rgba(236, 72, 153, 0.4);
    }

    /* Spinner styling */
    .stSpinner > div {
        border-top-color: var(--primary-color) !important;
        box-shadow: 0 0 10px var(--glow-color);
    }

    /* Warning message styling */
    .stWarning {
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.1), rgba(220, 38, 38, 0.1)) !important;
        border-left: 4px solid #ef4444 !important;
        border-radius: 12px !important;
        color: var(--text-primary) !important;
        backdrop-filter: blur(10px);
    }

    /* Info message styling */
    .stInfo {
        background: linear-gradient(135deg, rgba(139, 92, 246, 0.1), rgba(236, 72, 153, 0.1)) !important;
        border-left: 4px solid var(--primary-color) !important;
        border-radius: 12px !important;
        color: var(--text-primary) !important;
        backdrop-filter: blur(10px);
    }

    /* Success message styling */
    .stSuccess {
        background: linear-gradient(135deg, rgba(34, 197, 94, 0.1), rgba(16, 185, 129, 0.1)) !important;
        border-left: 4px solid #22c55e !important;
        border-radius: 12px !important;
        color: var(--text-primary) !important;
        backdrop-filter: blur(10px);
    }

    /* Animations */
    @keyframes fadeInDown {
        from {
            opacity: 0;
            transform: translateY(-30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes fadeIn {
        from { 
            opacity: 0; 
            transform: scale(0.95);
        }
        to { 
            opacity: 1; 
            transform: scale(1);
        }
    }

    /* Scrollbar styling */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(0, 0, 0, 0.3);
    }
    
    ::-webkit-scrollbar-thumb {
        background: var(--primary-color);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: var(--secondary-color);
    }

    /* Responsive design */
    @media (max-width: 768px) {
        .title-header h1 {
            font-size: 2.8rem !important;
        }
        .card {
            padding: 1.8rem;
            margin: 1rem 0;
        }
        .content-card {
            padding: 1.5rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# Beautiful header with animation
st.markdown("""
<div class="title-header">
    <h1>📚 Multimodal Education Creator</h1>
</div>
""", unsafe_allow_html=True)

st.markdown('<p class="subtitle">✨ Transform complex concepts into stunning visual and textual learning experiences</p>', unsafe_allow_html=True)

# Input section without card
col1, col2 = st.columns([3, 1])
with col1:
    topic = st.text_input("🎯 Enter an Educational Concept", placeholder="e.g., Photosynthesis, Python Programming, World War II...")
with col2:
    st.markdown('<br>', unsafe_allow_html=True)  # Spacing for alignment
    generate_btn = st.button("✨ Generate", use_container_width=True)

if generate_btn:
    if topic:
        # Generate explanation
        with st.spinner("🧠 Generating explanation..."):
            explanation = generate_explanation(topic)

        # Only generate image if explanation is valid
        if "Sorry, this topic is not supported" not in explanation:
            with st.spinner("🎨 Generating visual (fast diffusion)..."):
                image = generate_image(topic)
        else:
            image = None  # Skip image generation

        # Store in session state
        content_data = {
            'topic': topic,
            'explanation': explanation,
            'image': image,
            'timestamp': len(st.session_state.get('generated_content', [])) + 1
        }
        st.session_state.generated_content.append(content_data)

        # Display results with beautiful cards
        st.markdown('<div style="margin-top: 2rem;">', unsafe_allow_html=True)
        col1, col2 = st.columns(2, gap="large")
        
        with col1:
            st.markdown("""
            <div class="content-card">
                <h3>📖 Explanation</h3>
            </div>
            """, unsafe_allow_html=True)
            st.write(explanation)

        with col2:
            st.markdown("""
            <div class="content-card">
                <h3>🖼️ Visual</h3>
            </div>
            """, unsafe_allow_html=True)
            if image:
                st.image(image, use_container_width=True)
            else:
                st.info("🎭 No visual generated for this topic.")
        
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.warning("⚠️ Please enter an educational concept to get started!")


# Sidebar with favorites only
with st.sidebar:
    if st.session_state.favorites:
        st.markdown('<div class="card"><h3>❤️ Your Favorites</h3></div>', unsafe_allow_html=True)
        for i, fav in enumerate(st.session_state.favorites[-3:]):
            with st.expander(fav['topic'][:30] + "..."):
                st.write(fav['explanation'][:200] + "..." if len(fav['explanation']) > 200 else fav['explanation'])
                if st.button("Remove", key=f"remove_fav_{i}"):
                    st.session_state.favorites.remove(fav)
                    st.success("Removed from favorites!")
                    st.rerun()