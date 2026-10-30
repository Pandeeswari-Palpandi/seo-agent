import streamlit as st

from workflow import generate_seo_content_sync


# ---------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------

st.set_page_config(
    page_title="SEO Multi-Agent",
    page_icon="🚀",
    layout="wide",
)


# ---------------------------------------------------------
# CUSTOM CSS
# ---------------------------------------------------------

st.markdown(
    """
    <style>

    .main-title {
        font-size: 42px;
        font-weight: 700;
        margin-bottom: 5px;
    }

    .subtitle {
        font-size: 18px;
        color: #888888;
        margin-bottom: 30px;
    }

    .agent-card {
        padding: 16px;
        border-radius: 12px;
        border: 1px solid rgba(128,128,128,0.25);
        margin-bottom: 10px;
    }

    .agent-title {
        font-size: 18px;
        font-weight: 600;
    }

    .agent-description {
        font-size: 14px;
        color: #888888;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# HEADER
# ---------------------------------------------------------

st.markdown(
    '<div class="main-title">🚀 SEO Multi-Agent</div>',
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="subtitle">
    Research. Write. Optimize. Review.
    <br>
    Powered by AutoGen multi-agent AI.
    </div>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------

with st.sidebar:

    st.header("⚙️ SEO Settings")

    if st.button("🔄 Refresh", use_container_width=True):
        st.session_state["seo_result"] = None
        st.rerun()

    st.write(
        "Our AI agents work together to create "
        "high-quality SEO content."
    )

    st.divider()

    st.markdown("### 🤖 Agent Pipeline")

    st.markdown(
        """
        **🔎 Research Agent**

        Finds trends, keywords and search intent.

        **✍️ Content Writer**

        Creates the initial article.

        **🛠️ SEO Optimizer**

        Audits and improves SEO.

        **👀 Content Reviewer**

        Performs the final quality review.
        """
    )


# ---------------------------------------------------------
# TOPIC INPUT
# ---------------------------------------------------------

st.subheader("What do you want to write about?")

topic = st.text_input(
    "Enter your topic",
    placeholder="Example: AI Agents in 2026",
)


generate_button = st.button(
    "🚀 Generate SEO Content",
    type="primary",
    use_container_width=True,
)


# ---------------------------------------------------------
# GENERATE CONTENT
# ---------------------------------------------------------

if generate_button:

    if not topic.strip():

        st.warning(
            "Please enter a topic before starting."
        )

    else:

        # Clear previous result
        st.session_state["seo_result"] = None

        st.divider()

        st.subheader("🤖 AI Agent Pipeline")

        # -------------------------------------------------
        # CREATE AGENT STATUS UI
        # -------------------------------------------------

        research_status = st.empty()
        writer_status = st.empty()
        optimizer_status = st.empty()
        reviewer_status = st.empty()

        # Initial state
        research_status.info(
            "🔎 Research Agent — Running..."
        )

        writer_status.write(
            "✍️ Content Writer — Waiting..."
        )

        optimizer_status.write(
            "🛠️ SEO Optimizer — Waiting..."
        )

        reviewer_status.write(
            "👀 Content Reviewer — Waiting..."
        )

        progress_bar = st.progress(
            0,
            text="Starting AI workflow..."
        )

        try:

            # -------------------------------------------------
            # STEP 1 — RESEARCH
            # -------------------------------------------------

            research_status.info(
                "🔎 Research Agent — Running..."
            )

            progress_bar.progress(
                10,
                text="🔎 Research Agent is researching the topic..."
            )

            result = generate_seo_content_sync(
                topic.strip()
            )

            # -------------------------------------------------
            # RESEARCH COMPLETED
            # -------------------------------------------------

            research_status.success(
                "🔎 Research Agent — Completed ✅"
            )

            progress_bar.progress(
                25,
                text="🔎 Research completed."
            )

            # -------------------------------------------------
            # STEP 2 — CONTENT WRITER
            # -------------------------------------------------

            writer_status.info(
                "✍️ Content Writer — Completed ✅"
            )

            progress_bar.progress(
                50,
                text="✍️ Content Writer completed the article."
            )

            # -------------------------------------------------
            # STEP 3 — SEO OPTIMIZER
            # -------------------------------------------------

            optimizer_status.info(
                "🛠️ SEO Optimizer — Completed ✅"
            )

            progress_bar.progress(
                75,
                text="🛠️ SEO Optimizer completed the SEO audit."
            )

            # -------------------------------------------------
            # STEP 4 — CONTENT REVIEWER
            # -------------------------------------------------

            reviewer_status.success(
                "👀 Content Reviewer — Completed ✅"
            )

            progress_bar.progress(
                100,
                text="✅ All agents completed successfully!"
            )

            # -------------------------------------------------
            # SAVE RESULT
            # -------------------------------------------------

            st.session_state["seo_result"] = result

            st.success(
                "🎉 SEO content generation completed!"
            )

        except Exception as e:

            progress_bar.empty()

            st.error(
                f"❌ Something went wrong: {str(e)}"
            )


# ---------------------------------------------------------
# DISPLAY RESULT
# ---------------------------------------------------------

if st.session_state.get("seo_result"):

    result = st.session_state["seo_result"]

    st.divider()

    st.subheader(
        f"📄 SEO Content: {result['topic']}"
    )

    st.markdown(result["final_content"])

    st.download_button(
        label="⬇️ Download Article",
        data=result["final_content"],
        file_name="seo_article.md",
        mime="text/markdown",
        use_container_width=True,
    )
