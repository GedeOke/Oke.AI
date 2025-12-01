const base =
  "inline-flex items-center justify-center rounded-xl px-4 py-2 text-sm font-semibold transition focus:outline-none focus:ring-2 focus:ring-indigo-400 disabled:opacity-50 disabled:cursor-not-allowed shadow-lg shadow-indigo-500/10";

const variants = {
  primary: "bg-gradient-to-r from-indigo-500 to-sky-500 text-white hover:brightness-105",
  secondary: "bg-white border border-slate-200 text-slate-800 hover:bg-slate-50",
  ghost: "text-slate-700 hover:bg-slate-100",
};

export default function Button({ children, variant = "primary", className = "", ...props }) {
  const classes = `${base} ${variants[variant]} ${className}`;
  return (
    <button className={classes} {...props}>
      {children}
    </button>
  );
}
