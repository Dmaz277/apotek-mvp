# Barbershop MVP

Sistem manajemen barbershop dengan dashboard, inventory, dan transaksi.

## Fitur Utama

### Dashboard
- Total pelanggan & transaksi
- Revenue tracking (Rp format)
- Stok produk menipis (alert)
- Product mendekati expired (alert)

### Manajemen Produk
- CRUD produk & jasa
- Search & filter
- Stock tracking dengan badge warning
- Input validation (min 3 char, min price 1)

### Manajemen Pelanggan
- CRUD pelanggan
- Phone validation (min 10 digit)
- Member tracking

### Transaksi
- Layanan potong rambut
- Product sales
- Auto-deduct stock
- Walk-in support

## Tech Stack

- **Backend:** FastAPI (Python)
- **Frontend:** HTML/JS/CSS
- **Database:** SQLite
- **Deploy:** Vercel (frontend) + Railway (backend)

## Setup & Run

### Backend
```bash
cd backend
uvicorn main:app --reload
```

### Frontend
Buka `frontend/login.html` di browser

### Login
- Username: admin
- Password: apotek12

## Demo
Live: https://apotek-mvp.vercel.app
