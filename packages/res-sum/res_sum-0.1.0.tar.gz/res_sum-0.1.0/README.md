# Research summarizer
Leveraging LLMs for Research Synthesis

This package is designed to leverage the power of Large Language Models (LLMs) to summarize research papers. It uses a combination of Natural Language Processing (NLP) techniques and LLMs to extract and summarize key sections from research papers. The summarizer focuses on the methodology, results, discussion, and conclusion sections, providing a high-level summary of the key findings and conclusions (although you could extend to cover introduction or other parts of the paper).



## Features

- **PDF Extraction:** Extract text content from PDF files.
- **Text Preprocessing:** Clean and preprocess the extracted text for better summarization.
- **Section Extraction:** Identify and extract specific sections from the research paper.
- **Text Summarization:** Generate high-level summaries of the extracted sections using Open source LLMs like Llama 3 and Open AI's GPT-4 model.
- It can batch process multiple research papers at once.
- So, users just need to upload a folder containing multiple research papers and the summarizer will process all the papers and return a summary of each paper.
- The summaries are saved to a folder on your machine.
- **Streamlit Interface:** A user-friendly web interface for uploading PDF files and displaying summaries. You can access the web app via this [link](https://sum-tool.streamlit.app/)

## Installation

1. **Clone the repository:**

   ```sh
   git clone https://github.com/drhammed/res-sum.git
   



## Set up a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

## Install the required packages:
`pip install -r requirements.txt`

## Download NLTK data:
`python -m nltk.downloader punkt wordnet`

## Configuration

1. Google Drive API Credentials:

- Create a project on the (Google Cloud Console).

- Enable the Google Drive API.

- Create credentials (OAuth 2.0 Client IDs) and download the credentials.json file.

- Place the credentials.json file in the project directory. For a full instruction on this, see my [GDriveOps python package](https://pypi.org/project/GDriveOps/)


2. OpenAI API Key:
Obtain an API key from [Groq](https://console.groq.com/keys).

For the OpenAI API key, you can obtain one from [OpenAI](https://platform.openai.com/apps).

You can the set the API keys in the .env file or in the .env.local file.



## Usage




## Acknowledgments

- This project uses the API key from Groq AI and OpenAI GPT-4 model for text summarization.
- So, I want to thank the Groq AI for providing free tier access to interact with their models.
- Thanks to the Google Drive API for providing the tools to interact with Google Drive.

