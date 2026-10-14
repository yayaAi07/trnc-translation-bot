# TRNC Translation Bot 🌍

A free Telegram bot that translates text between **Arabic, French, English, Spanish, and Turkish** — built with zero infrastructure cost.

## 🎯 The Problem

In North Africa, users navigate a trilingual environment daily (Arabic, French, English). Existing translation tools are either paid, slow, or inaccessible on mobile. This bot solves that.

## ✨ Features

- 🌐 Translate text between 5 languages instantly
- 🔄 Automatic retry on API failures (3 attempts)
- 💰 Zero cost — uses Pollinations.ai (free API)
- 📱 Runs 24/7 on any device (even Android via Termux)
- 🎨 Clean, Arabic-first UI with inline keyboards

## 🛠️ Tech Stack

- **Python 3.13**
- **python-telegram-bot** — Telegram Bot API wrapper
- **Pollinations.ai** — Free AI translation backend
- **pypdf** — PDF text extraction (optional)
- **Google Gemini** — Image OCR (optional)

## 🚀 How to Run

1. Clone the repository:
   ```bash
   git clone https://github.com/yayaAi07/trnc-translation-bot.git
   cd trnc-translation-bot
