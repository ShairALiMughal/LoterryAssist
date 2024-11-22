# Lottery Prediction Assistant 🎲

A sophisticated Python desktop application that uses Google's Gemini AI to analyze lottery patterns and provide statistical insights. Built with CustomTkinter for a modern, user-friendly interface.

![Lottery Prediction Assistant](screenshots/app_preview.png)

## Features 🌟

- **AI-Powered Analysis**: Integrates with Google's Gemini AI for intelligent lottery analysis
- **Real-time Responses**: Watch AI responses appear word by word as they're generated
- **Modern UI**: Clean, dark-themed interface with message bubbles and chat history
- **Statistical Analysis**: 
  - Pattern recognition
  - Historical data correlation
  - Numerical sequence analysis
  - Probability calculations
- **Chat History Management**: Save and reload previous conversations
- **Markdown Support**: Format messages with bold text, bullet points, and numbered lists

## Installation 🚀

### Prerequisites

- Python 3.12 or higher
- Ubuntu/Linux (for other OS, steps might vary)

### Setting Up the Environment

1. Update your system:
```bash
sudo apt update
sudo apt upgrade
```

2. Install Python if not already installed:
```bash
sudo apt install python3
```

3. Install pip:
```bash
sudo apt install python3-pip
```

4. Install required system packages:
```bash
sudo apt install python3-dev python3-tk
```

### Project Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/lottery-predictor.git
cd lottery-predictor
```

2. Create and activate virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install required packages:
```bash
pip install customtkinter
pip install pandas
pip install numpy
pip install google-generativeai
```

4. Add your Google Gemini API key:
- Open `app.py`
- Replace `YOUR_API_KEY` with your actual Gemini API key

## Running the Application 🎮

1. Ensure your virtual environment is activated:
```bash
source venv/bin/activate
```

2. Run the application:
```bash
python3 app.py
```

## Usage Guide 📖

1. **Starting a New Chat**:
   - Click the "New Chat" button in the sidebar
   - Type your question in the input box at the bottom
   - Press "Send" or hit Enter

2. **Chat History**:
   - Previous conversations appear in the sidebar
   - Click on any conversation to reload it

3. **AI Analysis**:
   The assistant can help with:
   - Analyzing lottery number patterns
   - Identifying statistical trends
   - Calculating probabilities
   - Providing insights based on historical data

4. **Message Formatting**:
   - Use **bold** for emphasis
   - Create bullet points with *
   - Create numbered lists with 1., 2., etc.

## Technical Details 🔧

### Architecture

- **Frontend**: CustomTkinter for GUI
- **Backend**: Python 3.12
- **AI Integration**: Google Gemini API
- **Async Processing**: AsyncIO for non-blocking API calls
- **Threading**: Concurrent execution for smooth UI

### Key Components

1. **Main Application Window**:
   - Left sidebar for chat history
   - Main chat area for messages
   - Input area for user messages

2. **Message Handler**:
   - Async processing of messages
   - Real-time streaming of AI responses
   - Message formatting and display

3. **Chat Management**:
   - Chat history storage
   - Conversation loading/saving
   - Message threading

## Contributing 🤝

1. Fork the repository
2. Create a new branch (`git checkout -b feature/improvement`)
3. Make changes
4. Commit your changes (`git commit -am 'Add new feature'`)
5. Push to the branch (`git push origin feature/improvement`)
6. Create a Pull Request

## License 📄

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

## Acknowledgments 👏

- Google Gemini AI for providing the prediction engine
- CustomTkinter for the modern UI components
- The open-source community for various inspirations and solutions

## Support 🆘

For support, please open an issue in the GitHub repository or contact [your-email@example.com].

## Roadmap 🗺️

- [ ] Add support for different lottery types
- [ ] Implement data visualization
- [ ] Add export functionality for analysis results
- [ ] Integrate more AI models
- [ ] Add multi-language support

---

⚠️ **Disclaimer**: This application is for educational and entertainment purposes only. It does not guarantee any lottery wins and should not be used as financial advice.
