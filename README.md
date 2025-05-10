# ©️ ishort (Link Shortner)

A lightweight URL shortening service built to create short, unique links from long URLs with click tracking. This backend project showcases RESTful API design, threading for concurrent request handling, and database integration, demonstrating scalable and thread-safe web development.

Live Demo

🚀 Try the live app at:   https://ishort.onrender.com.

## Features
- **URL Shortening**: Generate short links for long URLs.
- **Click Tracking**: Monitor click counts for analytics.
- **RESTful APIs**: Endpoints for creating and redirecting URLs.
- **Thread-Safe**: Handles concurrent requests efficiently.

## Tech Stack
- **Language**: Python
- **Framework**: FastAPI
- **Database**: MongoDB
- **Threading**: Python’s `threading` module

## Setup Instructions
1. **Clone Repository**:
   ```bash
   git clone https://github.com/iamsuvhro/link-shortner.git
   cd link-shortner
   ```
2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Run Application**:
   ```bash
   uvicorn main:app --reload
   ```
4. **Access API**: Visit `http://localhost:8000`.

## Usage
- **Shorten URL**: POST `/shorten` with `{"url": "https://example.com"}`.
- **Redirect**: GET `/{short_code}` to visit the original URL.
- **Analytics**: GET `/analytics/{short_code}` for click data.

## Architecture
- **API Layer**: FastAPI-based REST endpoints.
- **Service Layer**: URL encoding and click tracking logic.
- **Data Layer**: MongoDB for persistent storage.

## Contributing
Fork, create a branch, commit changes, and submit a pull request. Follow the [Code of Conduct](CODE_OF_CONDUCT.md).

## License
MIT License. See [LICENSE](LICENSE).

---

**Built by Suvhro**  
🔗 [GitHub](https://github.com/iamsuvhro) | 🔗 [LinkedIn](https://linkedin.com/in/iamsuvhro)

---

**Notes**:
- The README is concise (230 words) and tailored to the provided GitHub repository ([https://github.com/iamsuvhro/link-shortner](https://github.com/iamsuvhro/link-shortner)), which uses FastAPI, MongoDB, and Python.
- The repository lacks a detailed setup guide, so I provided standard FastAPI setup steps. Confirm if additional steps (e.g., database initialization) are needed.
- If you want specific code snippets or adjustments (e.g., adding a screenshot or diagram), please share more details!
