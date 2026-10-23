import os

import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

from src.builder import build_messages
from src.validate import MarketingResponse
from src.export import (
    make_text_export,
    make_pdf_export
)
from src.templates import (
    PLATFORMS,
    TONES,
    LANGUAGES,
    LENGTHS
)


load_dotenv()

st.set_page_config(
    page_title="Cognetix Marketing Generator",
    page_icon="✍️",
    layout="wide"
)

st.title("Cognetix AI Marketing Content Generator")

st.write(
    "Generate, edit, and export marketing content "
    "for Instagram, LinkedIn, and Email."
)


with st.sidebar:
    st.header("Generation Settings")

    platform = st.selectbox(
        "Platform",
        list(PLATFORMS.keys())
    )

    tone = st.selectbox(
        "Tone",
        TONES
    )

    length = st.selectbox(
        "Length",
        LENGTHS,
        index=1
    )

    language = st.selectbox(
        "Language",
        LANGUAGES
    )

    variations = st.slider(
        "Number of variations",
        min_value=1,
        max_value=5,
        value=3
    )

    use_examples = st.toggle(
        "Use few-shot examples",
        value=True
    )


with st.form("marketing_form"):
    st.subheader("Product Information")

    product = st.text_input(
        "Product or service",
        placeholder="Example: Reusable insulated bottle"
    )

    features = st.text_area(
        "Features and benefits",
        placeholder="Enter the main features and benefits."
    )

    audience = st.text_input(
        "Target audience",
        placeholder="Example: College students"
    )

    call_to_action = st.text_input(
        "Call to action (optional)",
        placeholder="Example: Explore the collection"
    )

    submitted = st.form_submit_button(
        "Generate Content",
        type="primary"
    )


if "drafts" not in st.session_state:
    st.session_state.drafts = []

if "last_request" not in st.session_state:
    st.session_state.last_request = {}


def get_client():
    api_key = os.getenv(
        "LLM_API_KEY",
        ""
    ).strip()

    if (
        not api_key
        or api_key == "your_api_key_here"
    ):
        raise ValueError(
            "Add your API key to the .env file."
        )

    base_url = os.getenv(
        "LLM_BASE_URL",
        "https://api.openai.com/v1"
    ).strip()

    return OpenAI(
        api_key=api_key,
        base_url=base_url or None,
        timeout=45,
        max_retries=2
    )


if submitted:
    if not product.strip():
        st.error("Please enter a product or service.")

    elif not features.strip():
        st.error("Please enter product features.")

    elif not audience.strip():
        st.error("Please enter your target audience.")

    else:
        try:
            client = get_client()

            messages = build_messages(
                product=product.strip(),
                features=features.strip(),
                audience=audience.strip(),
                tone=tone,
                platform=platform,
                length=length,
                language=language,
                variations=variations,
                call_to_action=call_to_action.strip(),
                use_examples=use_examples
            )

            model = os.getenv(
                "MODEL_NAME",
                "gpt-4.1-mini"
            ).strip()

            max_tokens = int(
                os.getenv("MAX_TOKENS", "1400")
            )

            with st.spinner("Generating content..."):
                response = client.chat.completions.create(
                    model=model,
                    messages=messages,
                    temperature=0.2,
                    max_tokens=max_tokens,
                    response_format={
                        "type": "json_object"
                    }
                )

            raw_output = (
                response.choices[0].message.content
                or ""
            )

            validated = MarketingResponse.model_validate_json(
                raw_output
            )

            if len(validated.variations) != variations:
                st.warning(
                    f"Requested {variations} variations, "
                    f"but received {len(validated.variations)}."
                )

            st.session_state.drafts = [
                draft.model_dump()
                for draft in validated.variations
            ]

            st.session_state.last_request = {
                "product": product,
                "platform": platform,
                "tone": tone,
                "length": length,
                "language": language,
                "audience": audience,
                "features": features,
                "use_examples": use_examples
            }

            st.success("Content generated successfully!")

        except Exception as exc:
            st.error(f"Generation failed: {exc}")
            st.info(
                "Check your API key, model name, "
                "API quota, and internet connection."
            )


if st.session_state.drafts:
    st.divider()
    st.subheader("Edit Your Marketing Content")

    tabs = st.tabs([
        f"Variation {index + 1}"
        for index in range(
            len(st.session_state.drafts)
        )
    ])

    edited_drafts = []

    for index, (tab, draft) in enumerate(
        zip(tabs, st.session_state.drafts)
    ):
        with tab:
            headline = st.text_input(
                "Headline / Email Subject",
                value=draft.get("headline", ""),
                key=f"headline_{index}"
            )

            content = st.text_area(
                "Marketing Content",
                value=draft.get("content", ""),
                height=220,
                key=f"content_{index}"
            )

            hashtags_text = st.text_input(
                "Hashtags",
                value=" ".join(
                    draft.get("hashtags", [])
                ),
                key=f"hashtags_{index}"
            )

            combined = "\n".join([
                headline,
                content,
                hashtags_text
            ])

            st.caption(
                f"Character count: {len(combined)}"
            )

            st.caption(
                f"Content word count: {len(content.split())}"
            )

            edited_drafts.append({
                "headline": headline,
                "content": content,
                "hashtags": [
                    tag
                    for tag in hashtags_text.split()
                    if tag.strip()
                ]
            })

    st.session_state.drafts = edited_drafts

    st.divider()
    st.subheader("Download Your Content")

    text_data = make_text_export(
        st.session_state.drafts,
        st.session_state.last_request
    )

    col1, col2 = st.columns(2)

    with col1:
        st.download_button(
            label="Download TXT",
            data=text_data,
            file_name="marketing_drafts.txt",
            mime="text/plain",
            use_container_width=True
        )

    with col2:
        try:
            pdf_data = make_pdf_export(
                st.session_state.drafts,
                st.session_state.last_request
            )

            st.download_button(
                label="Download PDF",
                data=pdf_data,
                file_name="marketing_drafts.pdf",
                mime="application/pdf",
                use_container_width=True
            )

        except Exception as exc:
            st.warning(
                f"PDF export failed: {exc}"
            )

    with st.expander("View JSON Output"):
        st.json({
            "variations": st.session_state.drafts
        })


st.divider()

st.caption(
    "Review all generated content and claims before publishing. "
    "Do not enter API keys or private customer information here."
)