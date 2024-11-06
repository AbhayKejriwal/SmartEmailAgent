# Smart Email Agent

The **Smart Email Agent** is a personalized email filtering and categorization tool that integrates with Gmail to organize your inbox based on user-defined preferences. Utilizing the power of the Google Gemini AI, this app summarizes emails, classifies them into categories, and labels them for easy identification.

---

## Table of Contents

1. [Project Description](#project-description)
2. [Features](#features)
3. [Setup Guide for Normal Users](#setup-guide-for-normal-users)
   - [Prerequisites](#prerequisites)
   - [Download and Setup](#download-and-setup)
   - [Setting Up Gmail API Credentials](#setting-up-gmail-api-credentials)
   - [Obtaining Gemini API Key](#obtaining-gemini-api-key)
   - [Editing Preferences](#editing-preferences)
   - [Running the App](#running-the-app)
4. [Setup Guide for Developers](#setup-guide-for-developers)
   - [Prerequisites](#prerequisites-1)
   - [Repository Setup](#repository-setup)
   - [Google Cloud Setup for Gmail API](#google-cloud-setup-for-gmail-api)
   - [Configuring Google AI Gemini API](#configuring-google-ai-gemini-api)
   - [Modifying Preferences](#modifying-preferences)
   - [Running and Testing](#running-and-testing)
5. [Contribution Guide](#contribution-guide)

---

## Project Description

The Email Assistant App automates the tedious task of email organization, allowing users to filter, summarize, and categorize emails based on personalized rules and preferences. Using Google Cloud's Gmail API and the Gemini AI model, the app leverages machine learning to label emails as *Priority*, *Not Important* or *Useless*. However, the user can also mention their own labels in the preferences for the agent to use. The app is especially useful for users who manage large volumes of emails and want an automated way to prioritize their inbox.

---

## Features

- **Automated Email Labeling**: Emails are tagged with labels like *Priority*, *Not Important* or *Useless* by default. Non-*Priority* labeled emails are removed from the inbox.

- **User-Defined Filtering**: Filters based on personalized settings and preferences stored in a preferences file.

- **User-Defined Labels**: The user can also define their own custom labels for the agent to use in the preferences.

- **GUI Interface**: Simple user interface with progress indicators for processing emails.

---

## Setup Guide for Normal Users

### Prerequisites

- Windows 10 or 11.
- Google Cloud Console Account: Required to enable Gmail API and create OAuth credentials. Steps to get one are mentioned below.
- Google AI Studio Account: Needed to get an API key for Gemini AI. Steps to get one are mentioned below. 

### Download and Setup

1. Download the app's zip file from the releases section or directly download the SmartEmailAgent_vX.Y.Z.zip from the repository above and extract it to a location on your computer.
2. In the extracted folder, you’ll find the executable `.exe` file to run the app, along with configuration files. The executable will only run on Windows 10 and 11. For other OS, you have to follow the developer guide.

### Setting Up Gmail API Credentials

1. **Enable the Gmail API**:
   - Go to the [Google Cloud Console](https://console.cloud.google.com/).
   - Create a new project or use an existing one.
   - Navigate to **APIs & Services > Library** and enable **Gmail API**.

2. **Create OAuth Client Credentials**:
   - Go to **APIs & Services > Credentials** and click **Create Credentials**.
   - Select **OAuth client ID** and follow the steps to configure the OAuth consent screen. Add your email to the **Test Users** section (more details below in Step 3).
   - Set the application type as **Desktop app** and configure it with the necessary details (App name, User support email, etc.).
   - Download the `OAuth client`, it will be a json file named something like `client_secret_17...0i.apps.googleusercontent.com.json`.
   - Rename the `client_secrets` file to `credentials.json` and save the file in the same directory as the `EmailAssistant.exe` file.

3. **Add Your Email to OAuth Test Users**:
   - Under **OAuth consent screen** in **APIs & Services**, add your email address to **Test Users**. This allows the app to access your Gmail account, as it's still in development/testing mode.
   
   **Why this is needed**: Adding yourself as a test user authorizes the app to perform actions on your Gmail account and ensures Google’s consent requirements for API access.

### Obtaining Gemini API Key

1. Go to [Google AI Studio](https://studio.ai.google/) and create an account if you haven’t already.
2. Obtain an API key for Gemini and save it in a file named `.env` in the app directory in this format:
   ```plaintext
   GEMINI_API_KEY=your_gemini_api_key
   ```

### Editing Preferences

Open `Prefs.txt` in a text editor to customize your email handling preferences. Include details about your priorities, required categories or labels, and any specific instructions for filtering. The app will use these settings to tailor email summaries and classifications.

### Running the App
- Double-click the `EmailAssistant.exe` file to launch the Email Assistant app GUI.
- Use the provided buttons to Fetch and Filter Emails.
- When using the app for the first time, the app will prompt to sign-in to your Gmail Account and give permission to acces your emails. Give the appropriate permissions and click on continue. This will create an authentication token which will be stored in a token.json file in the root folder.

**Note**: Please note that the Google will warn the application to be unverified. That is because you have not verified the purpose for which you are using the credential.json file. That is not an issue, click on Continue.

- Follow the on-screen progress updates to see the status of your email processing.


**Note**: In case the application is not working or taking too much time to respond, the **login token** might have expired. **Delete the token.json file in the root folder and try running the application again**. The app will prompt you to sign in to your Gmail Account again in this case and will create a new token.

---

## Setup Guide for Developers

If you're interested in customizing the code or contributing, follow the steps below.

### Prerequisites

- **Python 3.8+**
- **Google Cloud Console Account**: Required to enable Gmail API and create OAuth credentials. Steps to get one are mentioned below.
- **Google AI Studio Account**: Needed to get an API key for Gemini AI. Steps to get one are mentioned below. 
- Project dependencies listed in `requirements.txt`

### Repository Setup

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/AbhayKejriwal/SmartEmailAgent
   cd SmartEmailAgent
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

### Google Cloud Setup for Gmail API

1. **Enable the Gmail API** in the [Google Cloud Console](https://console.cloud.google.com/).
2. **Create OAuth Credentials**:
   - Follow the [user setup instructions](#google-cloud-setup-for-gmail-api) above to create OAuth credentials and download the `credentials` file which is a json file.
   - Rename the file to `credentials.json` and place the file in the project’s root directory.

### Configuring Google AI Gemini API

1. **Obtain Gemini API Key**:
   - Go to [Google AI Studio](https://studio.ai.google/), create your account and get your API key for Gemini.
2. **Store the API Key**:
   - Create a `.env` file in the project’s root and add the key:
     ```plaintext
     GEMINI_API_KEY=your_gemini_api_key
     ```

### Modifying Preferences

Edit `Prefs.txt` to define your email preferences and filtering instructions. This file allows you to customize email categorization criteria.

### Running and Testing

To run the app directly in the terminal:
```bash
python Main.py
```

To run the app using the GUI, use:
```bash
python MainGUI.py
```

### Code Structure

- **GmailAPI.py**: Manages Gmail API interactions.
- **EmailAsst.py**: Handles email classification and summarization.
- **MainGUI.py**: Provides the PySimpleGUI interface for user interaction.
- **Main.py**: Provides the terminal version of the app.

---

## Contribution Guide

If you’d like to contribute:

1. **Fork and Clone** the repository.
2. **Create a New Branch** for your feature or bug fix:
   ```bash
   git checkout -b feature-name
   ```
3. **Commit Changes** with clear descriptions:
   ```bash
   git commit -m "Description of the change"
   ```
4. **Push** and **Create a Pull Request** for review.

---

Thank you for using and contributing to the Email Assistant App! For any issues or questions, please open an issue on GitHub.