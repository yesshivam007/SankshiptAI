import streamlit as st
from helper import chunkify_by_size, translate_text, manual_prompt, filter_wise


st.set_page_config(
    page_title='Sankshipt: Custom PDF Summary',
    page_icon='⏱️',
    layout='wide'
)


st.title('⏱️ Sankshipt: Custom PDF Summary')

pdf_file = st.sidebar.file_uploader('Upload your PDF File', type='pdf')
if pdf_file is not None:
   
    user_menu = st.sidebar.radio(
    'Summary Mode',
    options=('Manual Prompt', 'Filter-wise')
    )
    
    text_chunks = chunkify_by_size(pdf_file)
    translated_text = translate_text(text_chunks)

    if user_menu == 'Manual Prompt':
        manual_prompt(translated_text)
        
    elif user_menu == 'Filter-wise':
        filter_wise(translated_text)
