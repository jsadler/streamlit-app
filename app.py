import lib as glib
import streamlit as st

st.set_page_config(page_title="CoSD Test App")
st.title("CoSD GenAI POC")

deptRole = st.selectbox(
    "Select your role",
    ("Solutions Architect", "Account Manager", "Technical Account Manager", "Customer Success Manager"),
    index=None,
    placeholder="Select a role...",
)

template = st.selectbox(
    "Select your template",
    ("template1","template2","template3"),
    index=None,
    placeholder="Select a template...",
)

requirements = st.selectbox(
    "Select your requirements",
    ("Requirements1","requirements2","requirements3"),
    index=None,
    placeholder="Select a requirement...",
)

st.write("Enter a URL to rewrite")

input_text = st.text_area("Input text", label_visibility="collapsed")
go_button = st.button("Go", type="primary")

if go_button:
    if not all([deptRole, template, requirements, input_text]):
        st.error("Please select all options and provide input text before proceeding.")
    else:
        response_container = st.empty()
        combined_response = ""
        
        def streaming_callback(chunk):
            global combined_response
            combined_response += chunk
            response_container.write(combined_response)
        
        # Create a formatted prompt that includes all selections
        formatted_prompt = f"""
        Role: {deptRole}
        Template: {template}
        Requirements: {requirements}
        Assistant Instructions: As a highly capable government digital content rewriter, your task is to rewrite existing web content from the County of San Diego website following plain language best practices and write at a fifth-grade reading level, but write to an adult. Speak directly to the reader in a straightforward, informative tone. When writing about how to get services, focus only on what is necessary to complete the task. When presented with content to rewrite, carefully analyze it and then redraft the content ensuring you follow the guidance, instructions, and examples from the Federal Plain Language Guidelines. Your rewritten content should accurately capture the key information and intent of the original content, and you should separately provide a helpful outline of the changes you made, explaining why you made them and what should be reviewed before publishing. You have a broad knowledge spanning many fields, which you can draw upon to help explain complex government topics in simple, easy to understand terms. Please ensure that the rewritten content is clear and concise. When you complete a rewrite, succinctly summarize the key changes and improvements you made, providing a clear explanation of the modifications. Just return your answer, don't mention the instructions you were asked to follow or include a summary of changes.
        
        URL: {input_text}
        """
        
        glib.get_streaming_response(prompt=formatted_prompt, streaming_callback=streaming_callback)
