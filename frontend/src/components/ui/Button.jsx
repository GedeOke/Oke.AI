const base =
  "inline-flex items-center justify-center rounded-lg px-4 py-2 text-sm font-medium transition focus:outline-none focus:ring-2 focus:ring-indigo-400 disabled:opacity-50 disabled:cursor-not-allowed";

const variants = {
  primary: "bg-indigo-600 text-white hover:bg-indigo-700",
  secondary: "bg-white border border-gray-300 text-gray-800 hover:bg-gray-50",
};

export default function Button({ children, variant = "primary", className = "", ...props }) {
  const classes = `${base} ${variants[variant]} ${className}`;
  return (
    <button className={classes} {...props}>
      {children}
    </button>
  );
}
