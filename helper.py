import streamlit as st
from deep_translator import GoogleTranslator
from PyPDF2 import PdfReader
import google.generativeai as genai


GOOGLE_API_KEY = 'PASTE_YOUE_GEMINI_API_KEY'

genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro')


def chunkify_by_size(pdf_file, chunk_size=3000):
    text_chunks = []
    pdf_reader = PdfReader(pdf_file)
    full_text = ""
    for page in pdf_reader.pages:
        full_text += page.extract_text()

    # Loop through text in chunks
    for i in range(0, len(full_text), chunk_size):
        text_chunks.append(full_text[i:i+chunk_size])
    
    return text_chunks


def translate_text(text_chunks):
    loops = len(text_chunks)
    translated_text = ''
    my_bar1, iter = st.sidebar.progress(0), 1
    for text_chunk in text_chunks:
        translated_text += GoogleTranslator(target='en').translate(text_chunk)
        translated_text += ' '
        my_bar1.progress(int(100/loops)*iter)
        iter += 1
    
    my_bar1.progress(100)
    
    return translated_text


def manual_prompt(translated_text):

    prompt = st.text_input('Enter your Prompt')
    button = st.button('Generate Summary')

    if button:
        my_bar2 = st.progress(0)
        response = model.generate_content(
            f"""Understand and analyze the following text, and generate a summary for it according to the given prompt:
            Prompt: {prompt}, 
            Text: {translated_text}"""
        )
        my_bar2.progress(100)

        st.write(response.text)


def filter_wise(translated_text):

    categories = [
        "Academic",
        "Business",
        "Technical",
        "Legal",
        "Medical",
        "Government",
        "Financial",
        "News",
        "Entertainment",
        "Sports",
        "Arts",
        "Travel",
        "Lifestyle",
        "Science",
        "History",
        "Technology",
        "Literature",
        "Personal",
        "Education",
    ]
    document_types = [
        "Research Paper",
        "Thesis",
        "Syllabus",
        "Dissertation",
        "Lecture Notes",
        "Lab Report",
        "Case Study",
        "Grant Proposal",
        "Textbook",
        "Journal Article",
        "Presentation Slides",
        "Resume",
        "Cover Letter",
        "Business Plan",
        "Meeting Minutes",
        "Marketing Brochure",
        "Financial Statement",
        "Contract",
        "Proposal",
        "Email",
        "Report",
        "White Paper",
        "Software Documentation",
        "API Reference",
        "User Manual",
        "Technical Report",
        "Feasibility Study",
        "Product Specification",
        "Research Paper (Technical)",
        "Patent Application",
        "Code Documentation",
        "System Design Document",
        "Lease Agreement",
        "Non-Disclosure Agreement (NDA)",
        "Terms of Service (TOS)",
        "Privacy Policy",
        "Court Order",
        "Affidavit",
        "Will",
        "Lawsuit Complaint",
        "Legal Brief",
        "News Article",
        "Blog Post",
        "Email Thread",
        "Social Media Post",
        "Script",
        "Book Chapter",
        "Policy Document",
        "Customer Review",
        "Product Description",
        "Travel Brochure",
        "Recipe"
    ]
    summary_formats = [
        "Bullet Points",
        "Paragraph",
        "Table",
        "Key Points",
        "Annotated Outline",
        "Executive Summary"
    ]
    lengths = [
        'Short',
        'Medium',
        'Long'
    ]
    summary_styles = [
        "Informative",
        "Objective",
        "Concise",
        "Comprehensive",
        "Analytical",
        "Interpretive",
        "Formal",
        "Informal",
        "Actionable",
        "Targeted",
        "Creative",
    ] 
    
    col1, col2 = st.columns(2)
    with col1:
        document_type = st.selectbox('File Type', document_types)
    with col2:
        summary_format = st.selectbox('Summary Format', summary_formats)

    col1, col2 = st.columns(2)
    with col1:
        category = st.selectbox('Category', categories)
    with col2:
        length = st.selectbox('Summary Format', lengths)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        summary_style = st.selectbox('Summary Style', summary_styles)

    button = st.button('Generate Summary')

    if button:
        my_bar3 = st.progress(0)
        prompt = f"""please summarize the content of the provided PDF file based on the following parameters:

            File Type: {document_type}
            Category: {category}
            Summary Format: {summary_format}
            Length: {length}
            Summary Style: {summary_style}
            Please ensure that the summary accurately captures the key points of the text while adhering to the specified
            format, length, and style.

            Text: {translated_text}
        """
    
        resonse = model.generate_content(prompt)

        my_bar3.progress(100)

        st.write(resonse.text)