# FITUR 1 — Auth + Organization

Implementasi fitur otentikasi dan manajemen organisasi untuk OkeAI (backend FastAPI + Supabase).

## Ringkasan Fitur
- Registrasi dan login via Supabase Auth dengan JWT.
- Pembuatan profil pengguna (`users_profile`) dan organisasi default saat registrasi.
- Manajemen organisasi: mengambil organisasi aktif, melihat anggota, mengundang, dan menerima undangan.
- Endpoint profil: update profil dan avatar.

## Alur Register & Login
1. **Register** (`POST /auth/register`)
   - Daftarkan pengguna di Supabase Auth.
   - Buat `users_profile` dengan role `owner`.
   - Buat organisasi default dan membership `organization_members` sebagai `owner`.
   - Kembalikan `access_token`, `profile`, dan `organization`.
2. **Login** (`POST /auth/login`)
   - Autentikasi via Supabase.
   - Kembalikan `access_token` dan `profile`.
3. **Logout** (`POST /auth/logout`)
   - Revoke sesi aktif.
4. **Me** (`GET /auth/me`)
   - Mengambil profil pengguna berdasarkan JWT.

## Alur Create Organization Otomatis
- Registrasi akan otomatis membuat organisasi default bernama `<full_name>'s Organization`.
- Membership pemilik disimpan di `organization_members` dengan role `owner`.

## Alur Invite Member
1. **Invite** (`POST /organization/invite`)
   - Pemilik/admin mengundang pengguna lain dengan mencatat record di `organization_members` (role default `agent`).
2. **Accept** (`POST /organization/accept`)
   - Pengguna menerima undangan dan menjadi anggota organisasi.

## Role User
- `owner`: Pemilik organisasi, memiliki izin penuh.
- `admin`: Dapat mengelola anggota dan konfigurasi.
- `agent`: Role operasional, akses terbatas sesuai kebijakan.

## Endpoint Ringkas
- Auth: `POST /auth/register`, `POST /auth/login`, `POST /auth/logout`, `GET /auth/me`
- Users: `PUT /users/me`, `POST /users/me/avatar`
- Organization: `GET /organization`, `GET /organization/members`, `POST /organization/invite`, `POST /organization/accept`

## Catatan Tabel Supabase
- `users_profile(id, full_name, phone, avatar_url, role, created_at, updated_at)`
- `organizations(id, name, owner_id, created_at)`
- `organization_members(id, organization_id, user_id, role, invited_by, created_at)`

Pastikan kredensial Supabase tersedia di `.env`, dan semua secrets dimuat lewat environment (tidak di-hardcode).
