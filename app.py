import streamlit as st
import os
import textract
import time
# Add the correct path to the Python system path
import sys
sys.path.append('/app/')

# Now, import the QuestionGenerator
from question_generator.questiongenerator import QuestionGenerator

def generate_questions(text, num_questions):
    qg = QuestionGenerator()
    return qg.generate(text, num_questions=num_questions)

def read_file(file_path):
    try:
        text = textract.process(file_path)
        return text.decode('utf-8')
    except UnicodeDecodeError:
        try:
            text = textract.process(file_path, encoding='ISO-8859-1')
            return text.decode('ISO-8859-1')
        except Exception as e:
            st.error(f"Error: {e}")
            return None
    except Exception as e:
        st.error(f"Error: {e}")
        return None

st.title('AI Question Generator')
st.sidebar.markdown('**AI Question Generator** is an NLP system for generating reading comprehension-style questions from texts such as news articles or pages excerpts from books. ')

file_upload = st.file_uploader('Choose a file', type=['txt', 'pdf'])
text_area = st.text_area('Or input the text here')

if file_upload is not None:
    file_bytes = file_upload.getvalue()
    with open('temp_file','wb') as f:
        f.write(file_bytes)
    text = read_file('temp_file')
    os.remove('temp_file')
elif text_area != '':
    text = text_area

if 'text' in locals():
    num_questions = st.number_input('Number of Questions', min_value=1, max_value=20, value=10)
    if st.button('Generate Questions'):
        if text:
            with st.spinner('Generating Questions...'):
                progress_bar = st.progress(0)
                for i in range(100):
                    time.sleep(0.01)
                    progress_bar.progress(i+1)
                questions = generate_questions(text, num_questions)
                for i, qa in enumerate(questions):
                    with st.expander(f"Question {i+1}"):
                        st.write(qa['question'])
                        if isinstance(qa['answer'], list):
                            st.write("Answer:")
                            for option in qa['answer']:
                                if option['correct']:
                                    st.write(f"- **{option['answer']}** (Correct)")
                                else:
                                    st.write(f"- {option['answer']}")
                        else:
                            st.write(f"Answer: {qa['answer']}")
        else:
            st.warning('Please upload a file or enter text to generate questions.')
