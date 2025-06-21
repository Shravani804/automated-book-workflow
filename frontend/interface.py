import streamlit as st
from pathlib import Path
import requests
import streamlit.components.v1 as components


# Load file content or return empty string
def load_file(path):
    if Path(path).exists():
        return Path(path).read_text(encoding="utf-8")
    return ""

st.set_page_config(page_title="Chapter Editor", layout="wide")
st.title("📚 Finalize Your Chapter")

# Load versions
original = load_file("data/chapter1.txt")
spun = load_file("data/chapter1_spun.txt")
reviewed = load_file("data/chapter1_reviewed.txt")

# Display sections
st.subheader("🔹 Original Chapter (Scraped)")
st.text_area("Original", original, height=200)

st.subheader("🔸 AI-Spun Chapter")
st.text_area("Spun", spun, height=200)

st.subheader("🔄 Compare & Finalize")
col1, col2 = st.columns(2)

with col1:
    st.markdown("🧠 **AI-Reviewed Chapter**")
    st.text_area("Reviewed", reviewed, height=250, key="reviewed_text")

with col2:
    st.markdown("✍️ **Editable Final Version**")
    final = st.text_area("Final", reviewed, height=250, key="final_text")

#Save the final version
st.markdown("---")
centered_cols = st.columns(3)
with centered_cols[1]:  # center column
    if st.button("💾 Save Final Version", use_container_width=True):
        # Save locally
        Path("data/chapter1_final.txt").write_text(final, encoding="utf-8")

        # Save to backend and ChromaDB
        try:
            res = requests.post("http://127.0.0.1:8000/finalize", json={"content": final})
            res.raise_for_status()
            data = res.json()
            version_id = data.get("id")
            st.success(f"✅ Final version saved! Version ID: `{version_id}`")
            st.session_state["version_id"] = version_id  # Store for rating
        except Exception as e:
            st.error(f"❌ Failed to save via API: {e}")

# Rating Section
if "version_id" in st.session_state:
    # st.markdown("### ⭐ Rate This Final Version")

    components.html(
    """
    <style>
        .rating-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            margin-top: 1rem;
        }

        .star-label {
            font-size: 2rem;
            cursor: pointer;
            color: #ccc;
            transition: color 0.3s ease;
        }

        input[name="rating"]:checked ~ label,
        label:hover,
        label:hover ~ label {
            color: gold;
        }

        .star-label.checked {
            color: gold;
        }

        .rating-title {
            font-size: 1.5rem;
            font-weight: bold;
            margin-bottom: 0.5rem;
        }
    </style>

    <div class="rating-container">
        <div class="rating-title">⭐ Rate This Final Version</div>
        <div id="stars">
            <input type="radio" name="rating" id="star5" value="5"><label class="star-label" for="star5">★</label>
            <input type="radio" name="rating" id="star4" value="4"><label class="star-label" for="star4">★</label>
            <input type="radio" name="rating" id="star3" value="3"><label class="star-label" for="star3">★</label>
            <input type="radio" name="rating" id="star2" value="2"><label class="star-label" for="star2">★</label>
            <input type="radio" name="rating" id="star1" value="1"><label class="star-label" for="star1">★</label>
        </div>
        <p id="ratingValue"></p>
        <script>
            const stars = document.querySelectorAll('input[name="rating"]');
            stars.forEach(star => {
                star.addEventListener('change', function() {
                    const value = this.value;
                    document.getElementById('ratingValue').innerText = `⭐ You rated: ${value} star${value > 1 ? 's' : ''}`;
                });
            });
        </script>
    </div>
    """,
    height=200,
)
# Download Button Centered
st.markdown("---")
dl_cols = st.columns(3)
with dl_cols[1]:
    st.download_button(
        label="📥 Download Final Version",
        data=final,
        file_name="chapter1_final.txt",
        mime="text/plain",
        use_container_width=True
    )