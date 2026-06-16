# Forefront HQ


![Forefront Mockup](./static/images/forefront-hq-mock-ups.png)

## Table of Contents

[Introduction](#introduction)

[View Live Site](#view-live-site)

1. [UX](#ux)
    - [Project Goals](#project-goals)
    - [User Goals](#user-goals)
    - [User Stories](#user-stories)
    - [Developer Goals](#developer-goals)
    - [Design Choices](#design-choices)
        - [Colour Palette](#colour-palette)
        - [Frontend Design (Canva)](#frontend-design-canva)
            - [Home Page](#home-page)
            - [About Page](#about-page)
            - [Genre Page](#genre-page)
            - [Explore Page](#explore-page)
            - [Album Discussion Page](#album-discussion-page)
            - [Login Page](#login-page)
            - [Signup Page](#signup-page)
        - [Wireframes](#wireframes)
            - [Mobile](#mobile)
            - [Tablet](#tablet)
            - [Desktop](#desktop)
        - [ERD](#erd)
2. [Agile Development](#agile-development)
    - [GitHub Projects Board](#github-projects-board)
    - [MoSCoW Prioritisation](#moscow-prioritisation)
    - [Development Phases](#development-phases)
3. [Features](#features)
    - [Existing Features](#existing-features)
    - [Features to Implement](#features-to-implement)
4. [Technologies Used](#technologies-used)
5. [Testing](#testing)
    - [Code Validation](#code-validation)
    - [Bugs Discovered](#bugs-discovered)
    - [Usability Testing](#usability-testing)
    - [Responsiveness Testing](#responsiveness-testing)
    - [Data Managemnt Testing](#data-management-testing)
    - [Manual Testing](#manual-testing)
    - [Automated Testing](#automated-testing)
    - [Lighthouse Testing](#lighthouse-testing)
6. [Deployment](#deployment)
    - [Prerequisites](#prerequisites)
    - [Deploying to Heroku](#deploying-to-heroku)
    - [How To Run The Project Locally](#how-to-run-the-project-locally)
7. [Credits](#credits)
    - [Content](#content)
    - [Code](#code)
    - [Images](#images)
    - [API](#api)
    - [Acknowledgements](#acknowledgdements)

## Introduction 

**Forefront HQ** is a business website where potential clients can explore the companies services, 

## View Live Site

[ForeFront HQ Live Site](https://forefront-hq-new-a54ac6718d65.herokuapp.com/)

# UX

## Project Goals

## User Goals

## User Stories

## Developer Goals

## Design Choices

# Testing


## Bugs Discovered

### Bug 1 — `ModuleNotFoundError: No module named 'forefront_hq'`
**Description:** After renaming the Django config package from `webhive` to `forefront_hq`, Heroku could not find the settings module on deployment.  
**Cause:** The `DJANGO_SETTINGS_MODULE` config var on Heroku still pointed to `webhive.settings` after the rename.  
**Fix:** Updated the Heroku config var via CLI:
```
heroku config:set DJANGO_SETTINGS_MODULE=forefront_hq.settings --app forefront-hq
```

---

### Bug 2 - `Bad Request (400)` on Deployed Heroku App
**Description:** The deployed app returned a 400 error immediately after the Heroku app was renamed.  
**Cause:** `ALLOWED_HOSTS` in `settings.py` still contained the old Heroku hostname (`webhive-ca8f62799334.herokuapp.com`). Heroku also retains a random suffix in the hostname after a rename, meaning the expected clean URL `forefront-hq.herokuapp.com` was never the actual hostname.  
**Fix:** Updated `ALLOWED_HOSTS` to include the correct hostname:
```python
ALLOWED_HOSTS = ['127.0.0.1', 'localhost', 'forefront-hq-cd14dedc71a3.herokuapp.com']
```

---

### Bug 3 — `Not Found (404)` After Fixing ALLOWED_HOSTS
**Description:** App returned a 404 on all routes after the 400 was resolved.  
**Cause:** `ROOT_URLCONF` was defined twice in `settings.py` — the first instance (`webhive.urls`) was conflicting with the correct one (`forefront_hq.urls`). The `accounts/urls.py` file also did not exist yet.  
**Fix:** Removed the duplicate `ROOT_URLCONF` entry and created `accounts/urls.py` with the required URL patterns.
 
---

### Bug 4 — `ModuleNotFoundError: No module named 'accounts.urls'`
**Description:** Internal server error (500) on all routes after the 404 was resolved.  
**Cause:** `forefront_hq/urls.py` included `accounts.urls` but the file did not exist.  
**Fix:** Created `accounts/urls.py` with a basic home route.
 
---
 
### Bug 5 — `ImproperlyConfigured: allauth.account.middleware.AccountMiddleware`
**Description:** Server failed to start after installing `django-allauth`.  
**Cause:** The allauth middleware was not added to `MIDDLEWARE` in `settings.py`.  
**Fix:** Added `allauth.account.middleware.AccountMiddleware` to the bottom of the `MIDDLEWARE` list:
```python
'allauth.account.middleware.AccountMiddleware',
```
 
---
 
### Bug 6 — `ModuleNotFoundError: No module named 'requests'`
**Description:** Server failed to start after adding allauth social account providers.  
**Cause:** The `requests` package was not installed in the virtual environment.  
**Fix:** Ran the following and updated `requirements.txt`:
```
pip install requests
```
 
---
 
### Bug 7 — `ModuleNotFoundError: No module named 'jwt'`
**Description:** Server failed to start after installing `requests`.  
**Cause:** The `PyJWT` package required by allauth's Google provider was not installed.  
**Fix:** Ran the following and updated `requirements.txt`:
```
pip install PyJWT
```
 
---
 
### Bug 8 — `ModuleNotFoundError: No module named 'cryptography'`
**Description:** Server failed to start after installing `PyJWT`.  
**Cause:** The `cryptography` package required by allauth was not installed.  
**Fix:** Ran the following and updated `requirements.txt`:
```
pip install cryptography
```
 
---
 
### Bug 9 — Static Files Not Loading on Heroku
**Description:** CSS, images and JS were not being served on the deployed app.  
**Cause:** `whitenoise` was not installed, `STATIC_ROOT` was not set, and `DISABLE_COLLECTSTATIC` was not configured in Heroku config vars.  
**Fix:**
 
* Installed `whitenoise` and added it to `MIDDLEWARE`
* Added `STATIC_ROOT = BASE_DIR / 'staticfiles'` to `settings.py`
* Set `DISABLE_COLLECTSTATIC = 0` in Heroku config vars
---
 
### Bug 10 — Admin Login Failing With Correct Credentials
**Description:** Could not log in to the Django admin panel despite using the correct superuser credentials.  
**Cause:** The superuser was created before `django-allauth` was installed. Allauth changes the authentication backend which caused a mismatch with the existing superuser.  
**Fix:** Reset the superuser password via CLI:
```
python manage.py changepassword AshRoberts
```
 
---

### Bug 11 — Duplicate CSS Rules in `style.css`
**Description:** Navbar and burger menu styles were duplicated in `style.css` causing potential style conflicts.  
**Cause:** CSS was appended multiple times during iterative development without removing previous versions.  
**Fix:** Audited and rewrote `style.css` removing all duplicate rules.

---

### Bug 12 — `ConnectionRefusedError` on Google OAuth Callback
**Description:** After completing Google sign in, the app returned a `ConnectionRefusedError` at `/accounts/google/login/callback/`.  
**Cause:** Allauth was attempting to send an email verification to a user who had previously registered with email/password, but no email backend was configured.  
**Fix:** Added email backend configuration to `settings.py`:
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
```
And set `ACCOUNT_EMAIL_VERIFICATION = 'none'` temporarily during development.
 
---

### Bug 13 — `MultipleObjectsReturned` on Google Login
**Description:** Clicking "Continue with Google" returned a `MultipleObjectsReturned` error.  
**Cause:** Two Google Social Application entries existed in the database — one for local development and one for Heroku — both linked to the same site.  
**Fix:** Removed the duplicate entry in the Django admin under Social Applications and ensured each entry was linked to the correct site.
 
---

### Bug 14 — `InvalidRequestError: No such price` on Stripe Checkout
**Description:** Clicking a package CTA button returned a Stripe `InvalidRequestError`.  
**Cause:** The `stripe_price_id` field in the Django admin had the Stripe **Product ID** (`prod_...`) instead of the **Price ID** (`price_...`).  
**Fix:** Updated the `stripe_price_id` field in the Django admin with the correct Price ID from the Stripe dashboard.
 
---

### Bug 15 — Stripe Checkout 500 Error on Heroku
**Description:** Stripe checkout returned a 500 error on the deployed Heroku app but worked locally.  
**Cause:** `STRIPE_SECRET_KEY` and `STRIPE_PUBLIC_KEY` config vars were not set on Heroku.  
**Fix:**
```
heroku config:set STRIPE_SECRET_KEY=sk_test_... --app forefront-hq
heroku config:set STRIPE_PUBLIC_KEY=pk_test_... --app forefront-hq
```
Packages also needed to be re-added to the Heroku database with their Stripe price IDs.
 
---
 
### Bug 16 — Webhook `UserProfile matching query does not exist`
**Description:** The Stripe webhook handler returned a 500 error when processing `checkout.session.completed`.  
**Cause:** Existing user accounts did not have a `UserProfile` record as they were created before the model was added.  
**Fix:** Updated the webhook view to use `get_or_create` instead of `get`:
```python
profile, created = UserProfile.objects.get_or_create(user=user)
```
 
---
 
### Bug 17 — `AttributeError: get` in Stripe Webhook
**Description:** The webhook handler raised an `AttributeError` when trying to access session data.  
**Cause:** Stripe objects don't support Python's `.get()` method — they require direct dictionary access with `[]`.  
**Fix:** Replaced all `.get()` calls with direct key access:
```python
email = session['customer_email'] or ''
payment_intent = session['payment_intent'] or ''
```
 
---
 
### Bug 18 — Login Page CSS Not Applying
**Description:** The login page rendered without any custom styling — the auth card, form fields and layout were unstyled.  
**Cause:** The browser was serving a cached version of `style.css` that did not include the auth page styles.  
**Fix:** Performed a hard refresh using `Cmd + Shift + R` and cleared the browser cache via DevTools → Right-click refresh → Empty Cache and Hard Reload.
 
---
 
### Bug 19 — Portfolio Image Not Displaying
**Description:** The portfolio project image showed a "Missing key" placeholder despite an image URL being set in the admin.  
**Cause:** The imgbb **Viewer link** was used instead of the **Direct link**. The viewer link is a webpage, not a direct image URL.  
**Fix:** Updated the `image_url` field in the Django admin with the imgbb **Direct link** ending in `.jpg`.
 
---
 
### Bug 20 — Custom Package Summary Page Not Showing All Items
**Description:** The summary page only showed the Additional Pages line item, not the other selected addons.  
**Cause:** The `{% for addon in addons %}` loop in `custom_summary.html` was opened but never displayed any content — the Additional Pages block and the total were inside the loop incorrectly.  
**Fix:** Restructured the template to render the Additional Pages block and addon loop separately, with the total outside both.

---

### Bug 21 — Heroku App Flagged as "Dangerous Site" by Google Safe Browsing
**Description:** The deployed app showed a full red "Dangerous site" warning in Chrome, blocking all users from accessing it.
**Cause:** The `.herokuapp.com` subdomain (`forefront-hq-cd14dedc71a3.herokuapp.com`) had been previously assigned to another app by Heroku before being allocated to this project. That prior app had been flagged by Google Safe Browsing for phishing/malware, and the flag remained attached to the hostname.
**Fix:** Renamed the Heroku app to get a fresh, unflagged subdomain:

`heroku apps:rename forefront-hq-new`

New hostname: `forefront-hq-new-a54ac6718d65.herokuapp.com`. 
Updated `ALLOWED_HOSTS` in `settings.py` accordingly.

![Dangerous Site Screenshot](./static/images/dangerous-site-img.webp)

---

### Bug 22 — Email Confirmation and Verification Pages Unstyled
**Description:** After registering, the `/accounts/confirm-email/` page rendered without any site styling — no navbar, no dark theme, no layout. It showed raw allauth default markup with "Messages:" and "Menu:" labels.
**Cause:** No custom template overrides existed for allauth's `verification_sent.html` or `email_confirm.html`. Django was falling back to allauth's built-in templates which extend `account/base_entrance.html` instead of the project's `base.html`. The `templates/account/` directory did not exist in the project.
**Fix:** Created `templates/account/` inside the project's root templates directory and added two override templates:
- `templates/account/verification_sent.html` — styled "check your inbox" page shown after registration
- `templates/account/email_confirm.html` — styled confirmation page shown when clicking the email link

Both templates extend `base.html` and use the existing `.auth-wrapper`, `.auth-card`, `.auth-title`, `.auth-sub`, and `.btn` classes to match the login and register pages.

![Email Confirmation Page](./static/images/unstyled-confirm-email-img.webp)

# Deployment 

## Deploying to Heroku

The project was deployed to Heroku by connecting the GitHub repository through the Heroku dashboard. The following steps were followed:

1. Log in to [Heroku](https://www.heroku.com/) and click **New → Create new app**
2. Give the app a unique name and select your region, then click **Create app**
3. In the **Resources** tab, search for **Heroku Postgres** and add it as an add-on to provision the database
4. In the **Settings** tab, click **Reveal Config Vars** and add the following environment variables:

| Key | Value |
|-----|-------|
| `DATABASE_URL` | Your Heroku PostgreSQL URL (added automatically) |
| `SECRET_KEY` | Your Django secret key |
| `DEBUG` | `False` |

5. In the **Deploy** tab, select **GitHub** as the deployment method
6. Search for your repository name and click **Connect**
7. Scroll down to **Manual Deploy**, select the `main` branch and click **Deploy Branch**
8. Once the build completes, click **Open App** to view the live site

---

## How To Run The Project Locally

To clone this project from GitHub:

1. Follow this link to the [GitHub Repository](https://github.com/Ash-39284/forefront-hq)
2. Under the repository name, click the green **Code** button to reveal a dropdown menu
3. Select the **HTTPS** tab and copy the URL
4. In your local IDE open **Git Bash**
5. Change the current working directory to the location where you want the cloned directory
6. Type `git clone` followed by the URL you copied, then press **Enter**:
    ```bash
    git clone https://github.com/Ash-39284/forefront-hq
    ```
7. Navigate into the cloned directory:
    ```bash
    cd forefront_hq
    ```
8. Create and activate a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```
9. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```
10. Create an `env.py` file in the root directory and add your environment variables:
    ```python
    import os
    os.environ["SECRET_KEY"] = "your-secret-key"
    os.environ["DATABASE_URL"] = "your-database-url"
    ```
11. Run the database migrations:
    ```bash
    python manage.py migrate
    ```
12. Create a superuser to access the admin panel:
    ```bash
    python manage.py createsuperuser
    ```
13. Start the development server:
    ```bash
    python manage.py runserver
    ```
14. Open your browser and navigate to `http://127.0.0.1:8000/`



---

## Acknowledgdements

This project was developed and coded by Ashley Roberts in 2026.