# ai-command-generator

**Generate and run Linux commands in your terminal using AI.**  
Powered by Google's Gemini API, this tool helps you generate, edit, and execute shell commands on the go — right from your terminal.

---

## 🧠 What is it?

`ai-command-generator` uses the Gemini AI API to generate Linux shell commands based on natural language input. It types the command directly into your terminal, allowing you to modify it if needed before execution.

---

## ✨ Features

- ✅ Free to use Gemini API
- ⌨️ Auto-types the command in your terminal (press Enter to run, edit inline, or Ctrl+C to cancel)
- ⚡ Choose between different Gemini models (e.g., `gemini-2.0-flash`, `gemini-2.5-pro`)
- 🖥️ Optionally includes system info (like distro, shell, and current directory) to personalize command generation
- 🗂️ Caching for faster responses to repeated questions *(coming soon)*
- 📜 Ask about previous commands using shell history *(coming soon)*
- 📖 Uses your local man pages to improve accuracy when asking about a specific command *(coming soon)*
- 🎛️ Supports multiple system prompt profiles *(coming soon)*

---

## 🚀 Installation

```bash
git clone https://github.com/SleepInfinity/ai-command-generator
cd ai-command-generator
pip install -r requirements.txt
cp .env.example .env
nano .env
````

Edit the `.env` file and paste your API key from [Google AI Studio](https://aistudio.google.com/app/apikey):

```dotenv
GEMINI_API_KEY=AIxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

---

## 🧪 Usage

Basic usage:

```bash
python3 ai.py "command to update the system"
```

Example output:

```
> sudo apt update && sudo apt upgrade -y
[Modify inline or press Enter to execute, Ctrl+C to cancel]
```

### 🔧 Make it easier to use with an alias:

Add this line to your shell configuration file (`~/.bashrc`, `~/.zshrc`, etc.):

```bash
echo "alias ai='python3 $(pwd)/ai.py'" >> ~/.bashrc
```

Then restart your terminal, and you can simply run:

```bash
ai "command to update the system"
```

---

## 🤝 Contribute

Contributions are welcome!
Feel free to:

* Open issues for bugs, feature suggestions, or compatibility problems
* Submit pull requests to improve the tool
