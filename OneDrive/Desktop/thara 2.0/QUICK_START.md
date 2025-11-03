# Quick Start Guide - Purple 2.0

## 5-Minute Setup

### Step 1: Install Python
Make sure you have Python 3.7+ installed. Check with:
```bash
python --version
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Train the Model (First Time Only)
```bash
python model_train.py
```
This will generate:
- `chat_model.h5`
- `tokenizer.pkl`
- `label_encoder.pkl`

### Step 4: Run the Assistant
```bash
python main.py
```

## First Run

1. The assistant will greet you
2. Choose input method:
   - Press Enter for voice mode (default)
   - Type `2` for text mode
3. Start giving commands!

## Basic Commands

Try these first:
- **"open calculator"** - Opens Calculator app
- **"close calculator"** - Closes Calculator app
- **"open youtube"** - Opens YouTube in browser
- **"system condition"** - Shows system stats
- **"schedule"** - Shows today's schedule
- **"exit"** - Quits the program

## Troubleshooting Quick Fixes

**Microphone not working?**
- Switch to text mode: Type `2` when prompted
- Check Windows microphone permissions

**Model files missing?**
- Run: `python model_train.py`

**Import errors?**
- Install missing packages: `pip install [package-name]`

**Can't close apps?**
- Make sure you say "close [app name]" clearly
- Try running Python as administrator

## Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Customize your schedule in `main.py`
- Train the model with your own intents in `intents.json`

Enjoy using Purple 2.0! 🚀

