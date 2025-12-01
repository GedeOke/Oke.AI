export default function Textarea({ className = "", ...props }) {
  return (
    <textarea
      className={`w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500 ${className}`}
      {...props}
    />
  );
}
