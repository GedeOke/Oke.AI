export default function Card({ children, className = "" }) {
  return (
    <div className={`rounded-xl bg-white p-4 shadow-sm border border-gray-200 ${className}`}>
      {children}
    </div>
  );
}
