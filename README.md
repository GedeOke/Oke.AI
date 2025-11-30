# Update — Invite by Email

Desain undangan organisasi OkeAI diubah agar berbasis email (mirip Slack/Notion). Pemilik atau admin dapat mengirim undangan ke email apa pun; penerima bisa mendaftar dulu lalu menerima undangan ketika sudah login.

## Mengapa Diubah
- Menghilangkan ketergantungan pada `user_id` saat mengundang.
- Memungkinkan mengundang calon pengguna yang belum terdaftar.
- Mengikat token undangan dengan email untuk keamanan.

## Skema Tabel Baru
Tambahkan tabel `organization_invites` di Supabase:
```sql
create table if not exists public.organization_invites (
  id uuid primary key,
  organization_id uuid not null references public.organizations(id) on delete cascade,
  email text not null,
  role text not null check (role in ('owner','admin','agent')),
  invited_by uuid references auth.users(id),
  status text not null default 'pending',
  created_at timestamp with time zone default now(),
  expires_at timestamp with time zone
);
create index if not exists idx_org_invites_org on public.organization_invites (organization_id);
create index if not exists idx_org_invites_email on public.organization_invites (email);
```

## Alur Invite → Accept
1) **Invite (owner/admin)**  
   - Endpoint: `POST /organization/invite`  
   - Body: `{"email": "user2@gmail.com", "role": "admin"}`  
   - Aksi: cek role inviter (owner/admin), validasi role target, buat token UUID di `organization_invites` (status pending), kembalikan `invite_token`.

2) **Accept (penerima login dengan email yang sama)**  
   - Endpoint: `POST /organization/accept`  
   - Body: `{"invite_token": "<uuid>"}`  
   - Aksi: cek token pending dan belum kadaluarsa, cocokan email token dengan email user saat ini, cek membership belum ada, tambahkan ke `organization_members`, update status undangan menjadi `accepted`.

## Contoh Request/Response
**Invite**
```
POST /organization/invite
Authorization: Bearer <token_owner>
{
  "email": "user2@gmail.com",
  "role": "admin"
}
```
Respons
```
{
  "invite_token": "09f9e0da-7a5d-4c1b-8a38-9d8f5b4e52c2",
  "status": "pending"
}
```

**Accept**
```
POST /organization/accept
Authorization: Bearer <token_user2>
{
  "invite_token": "09f9e0da-7a5d-4c1b-8a38-9d8f5b4e52c2"
}
```
Respons (ringkas)
```
{
  "organization": { "id": "...", "name": "...", "owner_id": "..." },
  "member": { "organization_id": "...", "user_id": "...", "role": "admin", ... }
}
```

## Keamanan & Validasi
- Hanya owner/admin yang bisa mengundang.
- Role terbatas ke `owner`, `admin`, `agent`.
- Token terikat email; email user saat accept harus sama dengan email pada undangan.
- Tidak boleh ada membership duplikat untuk org yang sama.
- Undangan bisa memakai `expires_at`; jika lewat, akan ditolak.

## Endpoint Aktif (terkait undangan)
- `POST /organization/invite`
- `POST /organization/accept`
- `GET /organization`
- `GET /organization/members`
