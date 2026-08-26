"use client";
import { useRef } from "react";
import { useRouter } from "next/navigation";
import { Header } from "../../components/ui/Header";
export default function PopupModulePage() {
  const refs = useRef<Array<HTMLInputElement | null>>([]);
  const router = useRouter();
  const returnToCheckout = () => router.push("/checkout");
  return (
    <main className="site-shell inner-page popup-page">
      <Header />
      <section className="popup-checkout">
        <span className="design-label">Checkout</span>
        <div className="popup-checkout-card">
          <div className="checkout-heading">
            <span className="bag-icon">♙</span>
            <div>
              <h1>Checkout</h1>
              <p>Complete your order in 3 simple steps</p>
            </div>
            <span className="secure-badge">
              ♥ Secure Checkout
              <br />
              <small>Your information is safe</small>
            </span>
          </div>
          <div className="progress">
            <span className="active">
              <b>1</b>Your Details
            </span>
            <i />
            <span>
              <b>2</b>Review Order
            </span>
            <i />
            <span>
              <b>3</b>Confirmation
            </span>
          </div>
          <div className="checkout-form">
            <div className="field-pair">
              <label>
                Email Address
                <div className="input-with-icon">
                  <span>♙</span>
                  <input placeholder="you@example.com" />
                </div>
              </label>
              <label>
                Phone Number
                <div className="input-with-icon">
                  <span>⌕</span>
                  <input placeholder="8965390841" />
                </div>
              </label>
            </div>
            <label>
              Shipping Address
              <div className="input-with-icon address">
                <span>⌖</span>
                <textarea placeholder="123 Main Street, City, State, PIN" />
              </div>
            </label>
            <div className="checkout-actions">
              <button className="back-link">← Back to Cart</button>
              <button className="continue-button">
                ♙ &nbsp; Continue to Review
              </button>
            </div>
          </div>
        </div>
      </section>
      <div className="modal-backdrop popup-preview">
        <section className="otp-modal">
          <button
            className="modal-close"
            onClick={returnToCheckout}
            aria-label="Close"
          >
            ×
          </button>
          <div className="mail-art">♙</div>
          <h2>Welcome Back!</h2>
          <p>
            We found an existing account
            <br />
            with this email address.
          </p>
          <h3>Please enter your 6-digit login code</h3>
          <div className="otp-row">
            {Array.from({ length: 6 }, (_, index) => (
              <input
                key={index}
                ref={(element) => {
                  refs.current[index] = element;
                }}
                maxLength={1}
                inputMode="numeric"
                autoFocus={index === 0}
                onChange={(event) => {
                  if (event.target.value && index < 5)
                    refs.current[index + 1]?.focus();
                }}
              />
            ))}
          </div>
          <button className="verify-button" onClick={returnToCheckout}>
            Verify Code
          </button>
          <button className="guest-button" onClick={returnToCheckout}>
            ♙{" "}
            <span>
              Continue as Guest
              <small>You can checkout without logging in.</small>
            </span>
          </button>
          <footer>♢ &nbsp; Secure • Private • Encrypted</footer>
        </section>
      </div>
    </main>
  );
}
