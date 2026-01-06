import streamlit as st
import requests
import time

# --- MOCK AGENT FUNCTION ---
def run_content_agents():
    """
    Placeholder function for the agents logic.
    """
    # Simulating work
    time.sleep(1.5) 
    
    linkedin_post = """🚀 **Revolutionizing Content with AI!**

I just used our new AI Agent to generate this post. It's incredible how much time we can save while maintaining high quality. 

Key benefits:
✅ Faster iterations
✅ Consistent brand voice
✅ Data-driven insights

What are your thoughts on AI-driven content? Let's discuss! 👇

#AI #ContentCreation #Marketing #Innovation #FutureOfWork"""

    twitter_post = "AI is changing the game for creators! 🤖✨ \n\nJust generated this with our new agent. The future is here. \n\n#AI #Tech #ContentStrategy"
    
    # High-quality AI-related image
    image_url = "https://images.unsplash.com/photo-1677442136019-21780ecad995?q=80&w=1600&auto=format&fit=crop"
    
    return {
        "linkedin": linkedin_post,
        "twitter": twitter_post,
        "image_url": image_url
    }

# --- UI CONFIGURATION ---
st.set_page_config(
    page_title="Content Creator",
    layout="wide"
)

# Custom CSS for a premium, clean look
st.markdown("""
    <style>
    .stApp {
        background-color: #0e1117;
    }
    div.stButton > button:first-child {
        background: linear-gradient(45deg, #6200ea, #03dac6);
        color: white;
        border: none;
        padding: 10px 24px;
        border-radius: 8px;
        font-weight: 600;
        font-size: 1.1rem;
        transition: all 0.3s ease;
        width: 100%;
        margin-top: 10px;
    }
    div.stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(98, 0, 234, 0.4);
    }
    .content-box {
        background-color: #1a1c24;
        padding: 24px;
        border-radius: 12px;
        border: 1px solid #2d2f39;
        margin-bottom: 1.5rem;
    }
    h1, h2, h3 {
        color: #ffffff !important;
    }
    .stMarkdown p {
        color: #e0e0e0;
    }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER ---
st.title("Content Creation Agent")
st.markdown("Click the button below to generate LinkedIn posts and tweets on latest relevant AI topics for building personal brand")

# --- ACTION ---
if st.button("Create Content"):
    with st.spinner("We are working with our magic..."):
        st.session_state.content = run_content_agents()

st.markdown("---")

# --- DISPLAY ---
if "content" in st.session_state:
    c = st.session_state.content
    
    col1, col2 = st.columns([1, 1], gap="large")
    
    with col1:
        st.subheader("Generated Content")
        
        # LinkedIn Section
        st.markdown("### LinkedIn")
        st.markdown(c["linkedin"]) # Show rendered markdown
        st.code(c["linkedin"], language="markdown") # Provide easy copy block
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Twitter Section
        st.markdown("### Twitter / X")
        st.markdown(c["twitter"])
        st.code(c["twitter"], language="text")
        
    with col2:
        st.subheader("🖼️ Generated Image")
        st.image(c["image_url"], use_container_width=True, caption="AI-Generated Asset")
        
        # Download button for the image
        try:
            response = requests.get(c["image_url"])
            if response.status_code == 200:
                st.download_button(
                    label="📥 Download Image",
                    data=response.content,
                    file_name="generated_ai_asset.png",
                    mime="image/png"
                )
        except Exception as e:
            st.error("Error fetching image for download.")

else:
    # Empty state
    st.info("Ready when you are! Click the button above to start.")

# Footer
st.markdown("<br><br><p style='text-align: center;'>Created with  ❤  by [mmaazkhan](https://linkedin.com/in/mmaazukhan)</p>", unsafe_allow_html=True)