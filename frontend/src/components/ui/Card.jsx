export default function Card({ children, className = "" }) {
  return (
    <div className={`card-border ${className}`}>
      <div className="rounded-2xl p-5 glass-card">
        {children}
      </div>
    </div>
  );
}
