import Button from "../../ui/Button.jsx";

export default function SaveBar({ onSave, saving }) {
  return (
    <div className="fixed bottom-4 left-1/2 -translate-x-1/2 w-full max-w-3xl px-4">
      <div className="glass-card rounded-2xl p-3 flex items-center justify-between shadow-2xl">
        <p className="text-sm text-slate-700">Ada perubahan pada pengaturan AI.</p>
        <Button onClick={onSave} disabled={saving}>
          {saving ? "Menyimpan..." : "Save Changes"}
        </Button>
      </div>
    </div>
  );
}
