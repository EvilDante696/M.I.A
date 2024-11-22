
# MIA: A Multifunctional Conversational AI

## Overview

MIA is a conversational AI assistant built with Python, combining speech recognition, OpenAI's GPT model, Spotify integration, database queries, and text-to-speech conversion. Designed as a versatile assistant, MIA can naturally interact with users, search and play music, query a database, and perform additional tasks such as running Python scripts.

---

## Features

- **Speech Recognition**:  
  Uses `SpeechRecognition` for real-time interaction in French.

- **AI Conversation**:  
  Implements OpenAI's GPT-3.5-turbo for intelligent conversation and advanced responses.

- **Spotify Integration**:  
  Searches and plays music via Spotify using the `Spotipy` library.

- **Database Interactions**:  
  Connects to a MySQL database to retrieve user information or find specific data like email addresses.

- **Text-to-Speech**:  
  Converts AI-generated responses to audio using `gTTS` and adjusts playback speed with `pydub`.

- **Script Execution**:  
  Dynamically executes external Python scripts.

---

## Prerequisites

### Required Libraries

Install the following Python packages using pip:

```bash
pip install openai gTTS pygame speechrecognition spotipy mysql-connector-python pydub
```

### Additional Dependencies

**FFmpeg**: Required by `pydub` for audio processing. Install it via your package manager:

```bash
# For Debian/Ubuntu
sudo apt-get install ffmpeg

# For macOS (via Homebrew)
brew install ffmpeg
```

**Spotify Developer Account**:  
Create a Spotify developer application to obtain `client_id`, `client_secret`, and `redirect_uri`.

**OpenAI API Key**:  
Obtain an API key from [OpenAI](https://platform.openai.com/).

---

## Configuration

### 1. OpenAI API Key  
Set your OpenAI API key:

```python
openai.api_key = 'your_openai_api_key'
```

### 2. Spotify Authentication  
Configure your Spotify credentials:

```python
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id='your_client_id',
    client_secret='your_client_secret',
    redirect_uri='your_redirect_uri',
    scope='user-library-read user-modify-playback-state'
))
```

### 3. MySQL Database  
Update the database connection details:

```python
connection = mysql.connector.connect(
    host="your_database_host",
    user="your_database_user",
    password="your_database_password",
    database="your_database_name"
)
```

---

## Usage

### Run the Script  
```bash
python mia.py
```

### Interact with MIA  
- **General Conversation**: Speak to MIA, and it will respond intelligently.  
- **Play Music**: Say "Search for the song [song name]" to play music.  
- **Database Query**: Ask for user emails or general database information.  
- **Run Script**: Say "eyes" to execute an external Python script.

---

## File Structure

- `mia.py`: Main script.  
- `message.mp3`: Temporary file for text-to-speech output.  
- `message_accelerated.mp3`: Accelerated speech output file.

---

## Known Issues

### Speech Recognition  
- Reduced performance in noisy environments.  
- Requires an internet connection for the Google Web Speech API.

### Spotify Playback  
- Spotify requires an active playback device for music streaming.

### Database Connectivity  
- Ensure the MySQL server is running and accessible.

---

## Future Improvements

- Add support for multiple languages.  
- Enhance error handling for database operations and API requests.  
- Integrate additional APIs for weather, news, and more.

---

## Contributing

Contributions are welcome! Feel free to fork this repository, add new features, and submit a pull request.
