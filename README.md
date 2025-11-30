# Patch: Fix Accept Invite (Token Only)

Alasan perbaikan: desain lama masih meminta `organization_id` dari klien saat menerima undangan, sehingga rawan manipulasi. Desain baru hanya memakai `invite_token` dan backend membaca `organization_id` dari tabel `organization_invites`.

## Desain Baru
- Endpoint `POST /organization/accept` hanya menerima:
  ```json
  { "invite_token": "<uuid>" }
  ```
- Backend memuat undangan dari `organization_invites`, memvalidasi status/expiry/email, dan menambahkan membership dengan role dari undangan.
- Klien tidak lagi mengirim `organization_id`.

## Flow Accept Invite
1) User login dengan email yang sesuai undangan.  
2) Panggil `POST /organization/accept` dengan body `{ "invite_token": "<uuid>" }`.  
3) Backend:
   - Cari undangan by token.
   - Validasi pending + belum expired.
   - Cocokkan email current user dengan `invite.email`.
   - Tolak jika sudah member.
   - Insert ke `organization_members` memakai `organization_id` & `role` dari undangan.
   - Update status undangan → `accepted`.
4) Respons sukses:
   ```json
   {
     "status": "success",
     "message": "Invitation accepted",
     "organization_id": "<uuid>",
     "role": "<role>"
   }
   ```

## Contoh Request
```
POST /organization/accept
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "invite_token": "09f9e0da-7a5d-4c1b-8a38-9d8f5b4e52c2"
}
```
