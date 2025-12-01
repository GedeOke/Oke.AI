# WhatsApp Webhook Status (Paused)

Status: Pengembangan webhook WhatsApp ditunda sementara. Modul dasar sudah ada, tetapi butuh penyesuaian lanjutan saat dilanjutkan nanti.

## Yang Sudah Ada
- Router: `GET/POST /webhook/whatsapp/{organization_id}` (verifikasi + event).
- Signature validation: HMAC SHA256 dengan `WHATSAPP_APP_SECRET` (opsional, direkomendasikan).
- Normalizer payload (text/image/audio sederhana).
- Handler: dedup message_id, spam filter, resolve customer+conversation, simpan pesan, panggil AI Engine, kirim balasan via WhatsApp Cloud API.
- Test send: `POST /webhook/whatsapp/{organization_id}/test/send`.
- Env vars di `Settings`: `WHATSAPP_VERIFY_TOKEN`, `WHATSAPP_APP_SECRET`, `WHATSAPP_TOKEN`, `WHATSAPP_PHONE_NUMBER_ID`.

## Cara Tes Singkat (Manual)
- Verifikasi:
  `/webhook/whatsapp/{org_id}?hub.mode=subscribe&hub.verify_token=<token>&hub.challenge=123`
  (token harus sama dengan `WHATSAPP_VERIFY_TOKEN`).
- Event simulasi: kirim payload WA contoh ke `POST /webhook/whatsapp/{org_id}` (header signature jika secret diisi).
- Test kirim: `POST /webhook/whatsapp/{org_id}/test/send` dengan body `{ "organization_id": "...", "phone": "...", "text": "..." }` (butuh `WHATSAPP_TOKEN` dan `WHATSAPP_PHONE_NUMBER_ID`).

## Catatan & Pending
- Pastikan `organization_id` valid (tabel `organizations`); jika kosong akan 400.
- Dedup tabel `whatsapp_message_log` diperlukan (SQL ada di README).
- Belum ada dokumentasi lengkap/polish; akan dilanjutkan setelah fokus ke AI Engine.
- RLS/keamanan per tenant perlu ditinjau ketika produksi.
