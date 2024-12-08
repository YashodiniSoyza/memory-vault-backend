# Memory Vault - An Interactive Reminiscence Therapy Solution for Dementia Patients
## Student Name: W.M.Y. Soysa
## Student ID: IT21244698

## Description
Memory Vault is a backend application designed to provide interactive reminiscence therapy for dementia patients. The application helps enhance cognitive abilities and emotional well-being through personalized therapy sessions, memory recall exercises, and emotional support, powered by advanced machine learning and AI technologies.

---

## System Overview Diagram

![System Diagram](diagrams/system-diagram.png)

---

## Prerequisites

Before running the Flask server, ensure you have the following installed:

- Python 3.x
- `pip` package manager
- A virtual environment tool (`venv`)

---

## Steps to Run the Flask Server

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/24-25J-194-research-project/memory-vault-backend.git
   cd memory-vault-backend

2. **Create a Virtual Environment:**
   ```bash
   python -m venv venv
   
3. **Activate the Virtual Environment:**
    - **Windows:**
      ```bash
      venv\Scripts\activate
    - **macOS/Linux:**
      ```bash
      source venv/bin/activate
      
4. **Install Required Packages:**

   Once the virtual environment is activated, install the necessary packages listed in `requirements.txt`.
    ```bash
    pip install -r requirements.txt
   
5. **Set Up the Environment Variables:**

   Create a `.env` file in the root directory and add the following environment variables:
   ```bash
   PORT=5000 
   PROFILE=LOCAL
   MONGO_URI=mongodb://localhost:27017 
   DATABASE_NAME=MEMORY_VAULT
   OPENAI_API_KEY_NEW=your_openai_api_key
   ```
   **Note:** Replace `your_openai_api_key` with your OpenAI API key.

6. **Run the Flask Server:**
   ```bash
   python main.py
   ```
   The server should now be running on `http://localhost:5000`.
   