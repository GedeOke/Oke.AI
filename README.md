# Patch: Register + Invite Flow (Final SaaS Model)

## Masalah Desain Lama
- Setiap register selalu membuat organisasi baru → user bisa punya banyak org tak perlu.
- User yang datang via undangan tetap dibuatkan org baru dan menjadi owner.
- `users_profile.role` membingungkan; role seharusnya hanya di `organization_members`.
- Penerimaan undangan tidak otomatis saat register via link.

## Desain Baru
- Register membedakan alur biasa vs via `invite_token`.
- Auto-create organisasi hanya untuk register tanpa undangan.
- Role organisasi hanya disimpan di `organization_members.role`; `users_profile.role` diabaikan.
- Accept invite otomatis saat register jika menyertakan `invite_token`.

## Flow Register
### Tanpa invite_token
1) Supabase Auth `sign_up`.
2) Buat `users_profile`.
3) Buat organisasi baru + membership `owner`.
4) Kembalikan token + profile + organisasi baru.

### Dengan invite_token
1) Supabase Auth `sign_up`.
2) Buat `users_profile` (tanpa role).
3) Validasi undangan: token ada, status `pending`, email cocok, belum expired, belum member.
4) Insert membership ke `organization_members` dengan `organization_id` & `role` dari undangan.
5) Update undangan → `accepted`.
6) Kembalikan token + profile + organisasi yang di-join (tidak membuat org baru).

## Contoh Request Register (with invite)
```
POST /auth/register
Content-Type: application/json
{
  "email": "user2@example.com",
  "password": "password123",
  "full_name": "User Two",
  "invite_token": "09f9e0da-7a5d-4c1b-8a38-9d8f5b4e52c2"
}
```
Respons ringkas:
```
{
  "access_token": "...",
  "profile": { "id": "...", "full_name": "User Two", ... },
  "organization": { "id": "<invite.org_id>", "name": "...", ... }
}
```

## Kenapa Tidak Otomatis Buat Dua Org
Model SaaS (Slack/Notion) memisahkan org sebagai ruang kolaborasi; user yang diundang harus langsung masuk ke org pengundang, bukan menjadi owner org baru. Hal ini menghindari fragmentasi dan role yang salah.
