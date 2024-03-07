# Use an official Python runtime for x86-64 architecture
FROM python:3.9-slim-buster

# Install git, libmagic1, and other dependencies
RUN apt-get update && \
    apt-get install -y git libxml2 libxslt1.1 libffi-dev build-essential \
    libpoppler-cpp-dev pkg-config python3-dev

# Set the working directory in the container
WORKDIR /app

# Copy the app.py file into the container
COPY app.py /app/

# Clone the question_generator library from GitHub
RUN git clone https://github.com/AMontgomerie/question_generator.git /app/question_generator

# Install Streamlit
RUN pip install streamlit

# Install PyPDF2 for PDF text extraction

# Make port 8501 available to the world outside this container
EXPOSE 8501

# Run the Streamlit app
CMD ["streamlit", "run", "app.py", "--server.enableCORS", "false", "--server.enableXsrfProtection", "false"]