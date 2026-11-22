
const stats = [
  { label: "Interview Completed", value: "12", change: "+3 this week", icon: "◫" },
  { label: "Average Score", value: "78%", change: "+8% improvement", icon: "↗" },
  { label: "Practice Hours", value: "8.5h", change: "This month", icon: "◷" },
  { label: "Skills Improved", value: "06", change: "Across 4 topics", icon: "✧" },
];

const interview = [
  { role: "Python Developer", date: "Today · 10:30 AM", score: "82%", status: "Completed" },
  { role: "Machine Learning Engineer", date: "Yesterday · 4:15 PM", score: "76%", status: "Completed" },
  { role: "Data Analyst", date: "18 Nov · 11:00 AM", score: "71%", status: "Completed" },
];

const skills = [
  { name: "Python", score: 85 },
  { name: "Machine Learning", score: 72 },
  { name: "Data Structures", score: 68 },
  { name: "Communication", score: 80 },
];

export default function Home() {
  return (
    <main className="dashboard">
      <aside className="sidebar">
        <div className="brand">
          <div className="brand-icon">AI</div>
          <div>
            <strong>Interview Coach</strong>
            <span>INTELLIGENCE PLATFORM</span>
          </div>
        </div>

        <div className="nav-label">WORKSPACE</div>
        <nav className="navigation">
          <a className="nav-item active" href="/">▦ <span>Dashboard</span></a>
          <a className="nav-item" href="interview">◉ <span>My Interview</span></a>
          <a className="nav-item" href="#resume">▤ <span>My Resume</span></a>
          <a className="nav-item" href="#analytics">⌁ <span>Performance</span></a>
        </nav>

        <div className="nav-label">PREFERENCES</div>
        <nav className="navigation">
          <a className="nav-item" href="#settings">⚙ <span>Settings</span></a>
          <a className="nav-item" href="#help">? <span>Help & Support</span></a>
        </nav>

        <div className="sidebar-bottom">
          <div className="upgrade-card">
            <div className="upgrade-icon">✦</div>
            <strong>Unlock your potential</strong>
            <p>Keep practicing and improve your interview readiness.</p>
            <a href="interview">Explore practice →</a>
          </div>
          <div className="profile">
            <div className="avatar">SG</div>
            <div className="profile-info">
              <strong>Candidate</strong>
              <span>Free account</span>
            </div>
            <span className="profile-menu">···</span>
          </div>
        </div>
      </aside>

      <section className="main-content">
        <header className="topbar">
          <div>
            <span className="breadcrumb">Workspace / Dashboard</span>
          </div>
          <div className="topbar-right">
            <span className="system-status"><i /> AI Engine Ready</span>
            <button className="notification" aria-label="Notifications">♧</button>
            <div className="avatar">SG</div>
          </div>
        </header>

        <div className="content">
          <section className="welcome">
            <div>
              <div className="eyebrow">YOUR PERSONAL AI INTERVIEW PARTNER</div>
              <h1>Good to see you again, <span>Candidate.</span></h1>
              <p>Build confidence, sharpen your skills, and get interview-ready with AI.</p>
            </div>
            <div className="welcome-date">NOVEMBER 2026</div>
          </section>

          <section className="stats-grid">
            {stats.map((stat) => (
              <article className="stat-card" key={stat.label}>
                <div className="stat-top">
                  <span>{stat.label}</span>
                  <div className="stat-icon">{stat.icon}</div>
                </div>
                <strong className="stat-value">{stat.value}</strong>
                <span className="stat-change">{stat.change}</span>
              </article>
            ))}
          </section>

          <section className="hero-card">
            <div className="hero-copy">
              <div className="hero-tag"><span /> AI-POWERED PRACTICE</div>
              <h2>Your next opportunity<br />starts with <span>preparation.</span></h2>
              <p>Experience realistic interview tailored to your resume, skills, and career goals.</p>
              <a href="interview" className="primary-button">Start an Interview <span>→</span></a>
              <div className="hero-note">✦ Personalized questions · Real-time feedback</div>
            </div>
            <div className="hero-visual">
              <div className="orbit orbit-one" />
              <div className="orbit orbit-two" />
              <div className="ai-core">
                <div className="core-glow" />
                <span>AI</span>
              </div>
              <div className="floating-chip chip-top">✦ Smart Questions</div>
              <div className="floating-chip chip-bottom">↗ Performance Insights</div>
            </div>
          </section>

          <section className="lower-grid">
            <div className="panel" id="interview">
              <div className="panel-heading">
                <div>
                  <h3>Recent Interview</h3>
                  <p>Your latest practice sessions</p>
                </div>
                <a href="interview">View all →</a>
              </div>
              <div className="interview-list">
                {interview.map((interview) => (
                  <div className="interview-row" key={interview.role}>
                    <div className="interview-symbol">◈</div>
                    <div className="interview-details">
                      <strong>{interview.role}</strong>
                      <span>{interview.date}</span>
                    </div>
                    <div className="interview-result">
                      <strong>{interview.score}</strong>
                      <span>{interview.status}</span>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            <div className="panel" id="analytics">
              <div className="panel-heading">
                <div>
                  <h3>Skill Overview</h3>
                  <p>Your current performance</p>
                </div>
                <a href="#analytics">Details →</a>
              </div>
              <div className="skill-list">
                {skills.map((skill) => (
                  <div className="skill" key={skill.name}>
                    <div className="skill-heading">
                      <span>{skill.name}</span>
                      <strong>{skill.score}%</strong>
                    </div>
                    <div className="progress-track">
                      <div className="progress-fill" style={{ width: `${skill.score}%` }} />
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </section>

          <section className="resume-banner" id="resume">
            <div className="resume-icon">▤</div>
            <div>
              <strong>Make your interview personal</strong>
              <p>Upload your resume to generate questions based on your skills and projects.</p>
            </div>
            <a href="#resume">Upload Resume <span>→</span></a>
          </section>

          <footer className="footer">
            <span>© 2026 AI Interview Coach</span>
            <span>Built to help you perform at your best. ✦</span>
          </footer>
        </div>
      </section>
    </main>
  );
}
