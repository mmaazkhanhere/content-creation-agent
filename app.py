import streamlit as st
import requests
import time

from specialized_agents.personal_branding_agent import run_personal_branding_agent

# Note: We'll use asyncio.run to call the async agent function in Streamlit

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
        try:
            # Running the async function in a synchronous context
            import asyncio
            result = asyncio.run(run_personal_branding_agent("Latest AI/LLM trends for personal branding"))
            st.session_state.content = result
        except Exception as e:
            st.error(f"An error occurred: {e}")

st.markdown("---")

# --- DISPLAY ---
if "content" in st.session_state:
    final_output = st.session_state.content
    
    for i, topic_content in enumerate(final_output.topics):
        st.markdown(f"## Topic {i+1}: {topic_content.topic}")
        
        col1, col2 = st.columns([1, 1], gap="large")
        
        with col1:
            st.subheader("LinkedIn Post")
            st.markdown(topic_content.linkedin_post)
            st.code(topic_content.linkedin_post, language="markdown")
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            st.subheader("Twitter / X Thread")
            tweets_text = "\n---\n".join(topic_content.twitter_tweets)
            st.markdown(tweets_text)
            st.code(tweets_text, language="text")
            
        with col2:
            st.subheader("🖼️ Image Generation Prompts")
            # Since we only have prompts, we display them clearly
            prompt_data = topic_content.image_generation
            # We determine which prompt to show based on topic index (1 or 2)
            current_prompt = prompt_data.image_1_prompt if i == 0 else prompt_data.image_2_prompt
            
            st.info(f"**Prompt:** {current_prompt.prompt}")
            st.write(f"**Style:** {current_prompt.style}")
            st.write(f"**Notes:** {current_prompt.notes}")
            
            # Using a relevant Unsplash image as a placeholder since we don't have a real generator tool yet
            placeholder_url = f"https://images.unsplash.com/photo-1677442136019-21780ecad995?q=80&w=1600&auto=format&fit=crop&sig={i}"
            st.image(placeholder_url, use_container_width=True, caption=f"Visual representation for: {topic_content.topic}")
        
        st.markdown("---")

else:
    # Empty state
    st.info("Ready when you are! Click the button above to start.")

# Footer
st.markdown("<br><br><p style='text-align: center;'>Created with  ❤  by [mmaazkhan](https://linkedin.com/in/mmaazukhan)</p>", unsafe_allow_html=True)