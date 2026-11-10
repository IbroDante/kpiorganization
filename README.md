# KPI Organization website

The frontend is React/Vite. Flask serves the built website and sends contact/training enquiries through the **existing Brevo transactional email API**. The API key stays on the server; it must never be added to React or committed to the repository.

## Run locally

1. Install Python dependencies: `pip install -r requirements.txt`.
2. Install JavaScript dependencies: `npm ci`.
3. Configure the existing `BREVO_API_KEY` on the Flask server (or in a local `.env` file). The existing defaults are `BREVO_SENDER_EMAIL=929aca001@smtp-brevo.com` and `BREVO_RECIPIENT_EMAIL=info@kpiorganization.ng`; keep or set these to the **verified sender** and receiving inbox already configured for your Brevo account. These addresses have not been changed by the redesign.
4. Run `python app.py` and, in another terminal, `npm run dev`. Both `npm run dev` and `npm run preview` proxy `/api` to Flask on port 5000. Preview also requires `npm run build` first.

## Production deployment: Render Static Site + Flask Web Service

A Render Static Site cannot run Flask. The React build must send enquiries to the separate, running Flask Web Service. Do not put the Brevo API key in the Static Site or any `VITE_` variable.

1. On the **existing Flask Web Service**, deploy this version of the repository. Its build command can remain `pip install -r requirements.txt`, and its start command can remain `gunicorn app:app`. Keep the existing `BREVO_API_KEY`, `BREVO_SENDER_EMAIL`, and `BREVO_RECIPIENT_EMAIL` settings on this Web Service. Do not replace the existing recipient.
2. By default, the Flask API accepts browser requests from `https://kpiorganization.ng` and `https://www.kpiorganization.ng`. If using other domains (for example the Static Site's `onrender.com` address), set `ALLOWED_ORIGINS` on the Web Service to a comma-separated list of all exact frontend origins, including the custom domain; this setting replaces the defaults. Do not include paths or a wildcard. Apply/redeploy the Web Service.
3. On the **Render Static Site**, set `VITE_API_BASE_URL` to the Flask Web Service's public HTTPS origin, e.g. `https://your-web-service.onrender.com` (replace this example with the actual address; omit `/api` and any trailing path). This address is public, not a secret. The Vite build embeds the value, so redeploy the Static Site after adding/changing it. Build command: `npm ci && npm run build`; publish directory: `dist`.
4. When both deployments have completed, submit a test enquiry on the custom domain. Check the actual destination inbox and Brevo transactional logs. The browser will send to `VITE_API_BASE_URL/api/training-inquiry`; an empty variable instead uses the same-origin `/api` path for local development or a single-service deployment.

### Alternative: one Web Service

To serve the React app and Flask on the same origin, run `pip install -r requirements.txt && npm ci && npm run build` for the Web Service build and `gunicorn app:app` for startup (Node.js and Python must both be installed). Leave `VITE_API_BASE_URL` unset when building React. A Vite local proxy does not apply in production.

If an enquiry fails, the form will show an error and retain the entered information. Check the Flask service logs for a missing API key, a network error, or a Brevo HTTP error. Confirm the key is a Brevo **API key** (not the SMTP password), the sender is verified for that account, and the configured receiving address is correct. The app only reports success when Brevo accepts the email. A `201` response indicates acceptance by Brevo, not necessarily final inbox delivery; check Brevo's transactional email logs for delivery/bounce details.

Run the backend tests with `python -m unittest discover -s tests` and the frontend URL tests with `node --test tests/inquiry-url.test.js`.
