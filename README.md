# KPI Organization website

The website frontend is built with React and Vite. The existing Flask/Brevo backend remains responsible for sending enquiries so the Brevo API key stays on the server.

## Development

1. Install frontend dependencies with `npm install`.
2. Install backend dependencies with `pip install -r requirements.txt`.
3. Set `BREVO_API_KEY` and, if needed, `BREVO_SENDER_EMAIL` and `BREVO_RECIPIENT_EMAIL` in your environment or `.env` file.
4. Run `python app.py` for the API and `npm run dev` for the React development server. Vite proxies `/api` to Flask.

## Production

Run `npm run build`, then serve the Flask app (for example, `gunicorn app:app`). Flask serves the built React app and the enquiry API. Enquiries require a configured Brevo key; when delivery fails the form displays an error rather than claiming the message was received.
