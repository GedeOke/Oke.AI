export default function Card({ children, className = "" }) {
  return (
    <div className={`rounded-2xl p-5 glass-card ${className}`}>
      {children}
    </div>
  );
}
