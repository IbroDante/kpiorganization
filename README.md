# KPI Organization website

The frontend is React/Vite. Flask serves the built website and sends contact/training enquiries through the **existing Brevo transactional email API**. The API key stays on the server; it must never be added to React or committed to the repository.

## Run locally

1. Install Python dependencies: `pip install -r requirements.txt`.
2. Install JavaScript dependencies: `npm ci`.
3. Configure the existing `BREVO_API_KEY` on the Flask server (or in a local `.env` file). The existing defaults are `BREVO_SENDER_EMAIL=929aca001@smtp-brevo.com` and `BREVO_RECIPIENT_EMAIL=info@kpiorganization.ng`; keep or set these to the **verified sender** and receiving inbox already configured for your Brevo account. These addresses have not been changed by the redesign.
4. Run `python app.py` and, in another terminal, `npm run dev`. Both `npm run dev` and `npm run preview` proxy `/api` to Flask on port 5000. Preview also requires `npm run build` first.

## Production deployment

Deploy the React build and Flask API **together on the same service and origin**. An independently hosted static site cannot send to `/api/training-inquiry` unless its host is explicitly configured to proxy `/api` to the Flask service. Vite's local proxy is not a production server.

For an existing Python web service, use these commands (Node.js and Python must be available in the build environment):

- Build: `pip install -r requirements.txt && npm ci && npm run build`
- Start: `gunicorn app:app`

Keep the Brevo environment variables on that same running service when deploying the redesign. On Render, update the existing service's build command to the above rather than creating a separate static site with no API. Verify Node is installed in the service's build environment.

If an enquiry fails, the form will show an error and retain the entered information. Check the Flask service logs for a missing API key, a network error, or a Brevo HTTP error. Confirm the key is a Brevo **API key** (not the SMTP password), the sender is verified for that account, and the configured receiving address is correct. The app only reports success when Brevo accepts the email. A `201` response indicates acceptance by Brevo, not necessarily final inbox delivery; check Brevo's transactional email logs for delivery/bounce details.

Run the backend tests with `python -m unittest discover -s tests`.
