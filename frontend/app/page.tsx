import Link from "next/link";
import { Header } from "../components/ui/Header";

const benefits = [
  ["◉", "Easy Registration", "Create your account in a few seconds"],
  ["♙", "6-Digit Login Code", "Secure code for quick and safe login"],
  ["🛒", "Guest Checkout", "Checkout as guest at any time"],
  ["◇", "Safe & Secure", "Your data is encrypted and protected"],
];

export default function HomePage() {
  return (
    <main className="site-shell landing-page">
      <Header />
      <section className="hero">
        <div className="hero-copy">
          <span className="trust-pill">
            <span>✓</span> Secure&nbsp; • &nbsp;Fast&nbsp; • &nbsp;Reliable
          </span>
          <h1>
            Checkout Faster.
            <br />
            Login <span>Smarter.</span>
          </h1>
          <p>
            Recognize your account, login with a 6-digit code, and complete your
            checkout in seconds.
          </p>
          <div className="hero-actions">
            <Link className="primary-button" href="/register">
              ♙ &nbsp; Register
            </Link>
            <Link className="secondary-button" href="/checkout">
              🛒 &nbsp; Go to Checkout
            </Link>
          </div>
        </div>
        <div className="hero-visual" aria-hidden="true">
          <div className="dot-grid" />
          <div className="profile-card">
            <div className="avatar">
              <i />
            </div>
            <div className="line long" />
            <div className="line short" />
            <div className="code-row">
              {[1, 2, 3, 4, 5, 6].map((n) => (
                <b key={n}>{n}</b>
              ))}
            </div>
            <div className="card-rule" />
            <div className="lock">♙</div>
          </div>
        </div>
      </section>
      <section className="benefit-grid">
        {benefits.map(([icon, title, description]) => (
          <article className="benefit" key={title}>
            <span
              className={`benefit-icon ${title === "6-Digit Login Code" ? "login-code-icon" : ""}`}
            >
              {icon}
            </span>
            <div>
              <h2>{title}</h2>
              <p>{description}</p>
            </div>
          </article>
        ))}
      </section>
      <section className="promise-grid">
        <article>
          <span className="green">♢</span>
          <div>
            <h2>Your Security is Our Priority</h2>
            <p>We use industry-standard encryption to keep your data safe.</p>
          </div>
        </article>
        <article>
          <span className="purple">ϟ</span>
          <div>
            <h2>Built for Speed</h2>
            <p>Fast, seamless and optimized for the best experience.</p>
          </div>
        </article>
        <article>
          <span className="orange">◷</span>
          <div>
            <h2>Always Available</h2>
            <p>Our system is available 24/7 for you.</p>
          </div>
        </article>
        <article>
          <span className="pink">♡</span>
          <div>
            <h2>Made for You</h2>
            <p>Simple, intuitive and designed to save you time.</p>
          </div>
        </article>
      </section>
    </main>
  );
}
