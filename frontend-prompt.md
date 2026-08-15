# Frontend Prompt History

This file records the frontend development prompts and requirements used for the QuickCheckout frontend. It is stored beside `prompt.md` as requested.

## 1. Frontend PRD and Initial UI Build

**User request:** Review the frontend code and, based on the Frontend PRD, create only the UI pages for the first phase. UI designs were supplied for the landing page, registration page, popup module, checkout page, checkout submission page, and success page.

**Requirements captured:**

- Build with Next.js, TypeScript, Tailwind CSS/Bootstrap-compatible styling, React Hooks, and Axios.
- Create the primary routes: `/`, `/register`, and `/checkout`.
- Use a responsive desktop and mobile layout.
- First phase is UI-focused; API integration follows later.
- Landing page includes product header, hero, registration/checkout actions, benefits, and security information.
- Registration includes email, first name, last name, submit state, registration success state, backend-generated 6-digit code display, and checkout navigation.
- Checkout includes email, phone, shipping address, OTP recognition modal, guest checkout, review/submission state, and checkout success state.
- Maintain checkout values while authentication is shown.

**UI result:** Implemented landing, registration, checkout, OTP modal, review, and success states.

## 2. Registration and Landing Design Refinement

**User request:** Update the registration page to match the supplied revised design, make a small landing-page change to match the checkout theme, and confirm whether a PopupModule page had been created.

**Requirements captured:**

- Registration card must use the updated two-column account-creation layout and illustration.
- The landing page needs visual alignment with the checkout theme.
- Add a dedicated PopupModule page if not already present.
- The 6-Digit Login Code feature should use the supplied lock-card design cue.

**UI result:** Added `/popup-module`, updated the login-code feature icon, and adjusted landing-page accents.

## 3. Popup Module Behavior and Theme Consistency

**User request:** Make the PopupModule popup appear over the checkout page. Clicking **Continue as Guest** or **Verify Code** must redirect to the checkout page. Make the theme consistent over all pages.

**Requirements captured:**

- `/popup-module` displays a checkout form behind an OTP popup overlay.
- Close, Verify Code, and Continue as Guest route the user to `/checkout`.
- Apply the checkout green palette consistently to primary actions, account/OTP accents, registration, landing, popup, and success UI.

**UI result:** Popup overlay and redirects were implemented; the shared green theme was applied.

## 4. Backend API Integration and Recognition Debounce

**User request:** Integrate all APIs correctly and implement a 2-second recognition debounce.

**API contracts used:**

| Feature | Method | Endpoint | Request payload |
| --- | --- | --- | --- |
| Register user | `POST` | `/api/users/register` | `{ email, first_name, last_name }` |
| Recognize email | `GET` | `/api/users/recognize` | Query parameter: `email` |
| Verify OTP | `POST` | `/api/auth/verify` | `{ email, code }` |
| Create checkout | `POST` | `/api/checkout/create` | `{ email, phone, shipping_address, idempotency_key }` |

**Requirements captured:**

- Use `first_name`, `last_name`, and `shipping_address` exactly as required by Django.
- Display the `code` returned by the registration endpoint; never generate it on the client.
- Validate email format before recognition.
- Debounce recognition by **2 seconds** after email input stops changing.
- Abort/cancel stale recognition requests so an older response cannot affect a newer email value.
- For a registered email, show the OTP modal; verification uses the current email and six entered digits.
- For an unregistered email, recognition must not block checkout; proceed as guest.
- Allow registered users to choose Continue as Guest without an API call.
- Preserve all checkout fields during the OTP flow.
- Display server/network errors and API loading states.
- Disable actions while registration, verification, or checkout submission is in progress.
- Include a client-generated idempotency UUID for checkout submissions to prevent accidental duplicates.

**Implementation result:** Registration, recognition, OTP verification, guest behavior, and checkout submission are wired through the shared Axios services. The production build passes.

## Current Frontend Routes

- `/` — Landing page
- `/register` — Registration and generated-code success state
- `/checkout` — API-backed checkout and OTP recognition flow
- `/popup-module` — Standalone visual popup-over-checkout preview
