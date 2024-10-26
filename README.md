# Chatbot API
![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)
![Vercel](https://img.shields.io/badge/vercel-%23000000.svg?style=for-the-badge&logo=vercel&logoColor=white)
![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/github%20actions-%232671E5.svg?style=for-the-badge&logo=githubactions&logoColor=white)

This is a chatbot API integrated with OpenAI and Vanna AI, connected through a Chrome extension that provides users with real-time assistance based on the UoM Student Handbook.

## System Architecture Overview
![alt text](image.png)

- **User Interaction**: Users interact through a Chrome extension that pops up when they access the UoM Student Handbook in their browser.
- **Chrome Extension**: This extension, comprising HTML, JavaScript, and manifest files, triggers the UoM Handbook Chatbot popup.
- **Chatbot API**: The Chrome extension sends user questions to the Flask Python-based chatbot API.
- **Vanna AI & OpenAI Integration**: The chatbot API sends user questions to Vanna AI for query processing. If natural language understanding or additional processing is needed, OpenAI is used to generate responses.
- **Supabase**: The data used by Vanna AI is stored in Supabase, which contains information scraped from the University of Melbourne Student Handbook.

## Getting Started

### Step 1: Clone the repository

```bash
git clone https://github.com/may-bee/it-project2024-sm-2.git
```

### Step 2: Environment Setup

1. **Install Python**  
   Ensure Python 3.x is installed on your system. You can verify by running:
   ```sh
   python3 --version
   ```

2. **Create a Virtual Environment**  
   Set up a virtual environment to isolate the dependencies:
   ```sh
   python3 -m venv venv
   ```

3. **Activate the Virtual Environment**  
   For Windows:
   ```sh
   venv\Scripts\activate
   ```
   For Linux or macOS:
   ```sh
   source venv/bin/activate
   ```

4. **Install Dependencies**  
   Install the necessary dependencies from `requirements.txt`:
   ```sh
   pip install -r requirements.txt
   ```

### Step 3: Vercel CLI Installation

1. **Install Node.js and NPM**  
   Ensure that Node.js and npm are installed on your machine, as Vercel requires npm. You can check the versions with:
   ```sh
   node -v
   npm -v
   ```

2. **Install Vercel CLI**  
   To install the Vercel command-line tool globally, run:
   ```sh
   npm install -g vercel
   ```

### Step 4: Build Procedures

Vercel automatically detects and builds your project when deploying. However, to ensure everything goes smoothly, set up the necessary `build` command.

1. **Create a Start Script**  
   Add a start command to `app.py` if not already present:
   ```python
   if __name__ == '__main__':
       from os import environ
       app.run(debug=False, port=int(environ.get('PORT', 5000)), host='0.0.0.0')
   ```

2. **Ensure Dependencies**  
   Make sure all necessary Python dependencies are included in `requirements.txt`.

### Step 5: Deploying to Vercel

1. **Log in to Vercel**  
   Use the Vercel CLI to log in:
   ```sh
   vercel login
   ```

2. **Initialize Deployment**  
   Navigate to your project directory and initialize Vercel deployment:
   ```sh
   vercel
   ```

### Step 6: Environment Variables

1. **Add Environment Variables**  
   Use the `.env.sample` as a reference for necessary environment variables. You can add these to Vercel's configuration:
   ```sh
   vercel env add VARIABLE_NAME VARIABLE_VALUE
   ```
   You can also use the Vercel Dashboard to manage environment variables.

### Step 7: Push to Production

1. **Test the Deployment**  
   After the initial deployment, Vercel provides a unique staging URL where you can test your API to ensure it works as expected.

2. **Promote to Production**  
   If everything looks good on the staging URL, you can promote the app to production using:
   ```sh
   vercel --prod
   ```

Vercel will handle the build and deployment processes and provide you with an updated production link.