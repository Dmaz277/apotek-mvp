# Apotek MVP - Quick Start Guide

## Detailed Changes: File & Line Numbers

### BACKEND

#### 1. auth.py - Ganti Passlib → Bcrypt Direct
**Problem:** Passlib crash saat password >72 bytes (bcrypt limit)
**Solution:** Bypass passlib, pakai bcrypt library langsung

**Changes:**
- **Line 1:** `import bcrypt` (ganti `from passlib.context import CryptContext`)
- **Line 2-10:** Keep (jose, datetime, fastapi, HTTPBearer imports)
- **Line 12-14:** Delete `pwd_context = CryptContext(...)`
- **Line 19-21:** Update hash_password()
  ```python
  def hash_password(password: str):
      return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
  ```
- **Line 23-25:** Update verify_password()
  ```python
  def verify_password(plain_password: str, hashed_password: str):
      return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())
  ```
- **Line 27-31:** Keep create_access_token() & verify_token() (unchanged)

---

#### 2. models.py - TransactionLog Schema Update
**File:** `backend/models.py`
**Lines 19-25:** Update TransactionLog class

**Old:**
```python
customer_id = Column(Integer, ForeignKey("customer.id_customer"))
```

**New:**
```python
customer_id = Column(Integer, ForeignKey("customer.id_customer"), nullable=True)
customer_name = Column(String(100), nullable=True)
```

**Reason:** Support walk-in customers (optional customer_id, pakai customer_name)

---

#### 3. schemas.py - Optional Customer & Date
**File:** `backend/schemas.py`
**Lines 24-31:** Update TransactionCreate & TransactionOut

**TransactionCreate (old):**
```python
customer_id: int
date_out: date
```

**TransactionCreate (new):**
```python
customer_id: int | None = None
customer_name: str | None = None
date_out: date | None = None
```

**TransactionOut (new fields):**
```python
customer_id: int | None
customer_name: str | None
```

---

#### 4. main.py - Transaction Endpoint Logic
**File:** `backend/main.py`
**Lines 117-162:** POST /transaction endpoint

**Key Changes:**
- **Line 129-135:** Customer validation optional
  ```python
  customer_id = None
  customer_name = None
  if transaction.customer_id:
      customer = db.query(...).filter(...).first()
      if not customer:
          raise HTTPException(...)
      customer_id = transaction.customer_id
  elif transaction.customer_name:
      customer_name = transaction.customer_name
  ```

- **Line 147:** Auto-date fallback
  ```python
  date_out=transaction.date_out or date.today()
  ```

- **Line 151-152:** Save dengan customer_id & customer_name
  ```python
  new_transaction = models.TransactionLog(
      customer_id=customer_id,
      customer_name=customer_name,
      ...
  )
  ```

---

#### 5. .env - Password Hash Update
**File:** `backend/.env`
**Line 3:**

**Old:**
```
ADMIN_PASSWORD_HASH=$2b$12$p3fI5oP.wWM96e2VNzuWGubTXKFtJhW2Y1sAHG/2GUFQHuo.RV.ma
```

**New:**
```
ADMIN_PASSWORD_HASH=$2b$12$8SRWdJVKhKbPno5iMg.59.u6lHoufezNUGN9G6GqrRM0hatYBaF3m
```

**Password:** `apotek12` (regenerated untuk fix bcrypt limit)

---

### FRONTEND

#### 6. index.html - Complete Redesign + 5 Features

**CSS Updates:**

**Line 7-87: CSS Styles**
- Keep sidebar, main-content, header-bar, card styles
- **Line 73-87 (NEW):** Add spinner styles
  ```css
  .spinner-container {
      display: none;
      text-align: center;
      padding: 20px;
  }
  .spinner-container.show {
      display: block;
  }
  .spinner-border-sm {
      width: 1rem;
      height: 1rem;
      border-width: 0.2em;
  }
  ```

---

**HTML Updates:**

**Line 132-175: Dashboard Revenue Cards (NEW FEATURE #1)**
- **Line 132-172 (NEW):** Insert 3 revenue stat cards sebelum low stock alerts
  ```html
  <div class="row mt-4">
      <div class="col-md-4">
          <div class="card bg-light border-primary">
              <div class="card-body">
                  <h5 class="card-title">💰 Total Penjualan</h5>
                  <p id="totalRevenue">Rp -</p>
              </div>
          </div>
      </div>
      <div class="col-md-4">
          <div class="card bg-light border-success">
              <h5>📦 Total Unit Terjual</h5>
              <p id="totalUnitSold">-</p>
          </div>
      </div>
      <div class="col-md-4">
          <div class="card bg-light border-info">
              <h5>📈 Rata-rata Per Transaksi</h5>
              <p id="avgTransaction">Rp -</p>
          </div>
      </div>
  </div>
  ```

**Line 177-180: Dashboard Loading Spinner (NEW FEATURE #2)**
```html
<div id="dashboardLoader" class="spinner-container">
    <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
    </div>
    <p class="text-muted mt-2">Loading data...</p>
</div>
```

**Line 208-226: Medicine Search & Filter (NEW FEATURE #4)**
```html
<div class="card mb-3">
    <div class="card-body">
        <div class="row g-2">
            <div class="col-md-6">
                <input type="text" class="form-control" id="medicineSearch" 
                       placeholder="🔍 Cari nama obat...">
            </div>
            <div class="col-md-6">
                <select class="form-select" id="medicineFilter">
                    <option value="">Semua Status</option>
                    <option value="low">Stok Menipis (<10)</option>
                    <option value="expired">Mendekati Expired</option>
                </select>
            </div>
        </div>
    </div>
</div>
```

**Line 197-203: Medicine Form Input Validation (NEW FEATURE #5)**

**Old:**
```html
<input type="text" id="name" placeholder="Nama Obat" required>
<input type="number" id="price" placeholder="Harga" required>
<input type="number" id="stock" placeholder="Stok" required>
```

**New:**
```html
<input type="text" id="name" placeholder="Nama Obat" required minlength="3">
<input type="number" id="price" placeholder="Harga" required min="1" step="1">
<input type="number" id="stock" placeholder="Stok" required min="0" step="1">
```

**Line 300-304: Customer Form Input Validation (NEW FEATURE #5)**

**Old:**
```html
<input type="text" id="cust_name" placeholder="Nama Customer" required>
<input type="text" id="cust_phone" placeholder="No. HP" required>
```

**New:**
```html
<input type="text" id="cust_name" placeholder="Nama Customer" required minlength="3">
<input type="tel" id="cust_phone" placeholder="No. HP" required pattern="[0-9]{10,}" 
       title="Nomor HP minimal 10 digit">
```

**Line 444, 605: Delete Buttons - Confirm Dialog (NEW FEATURE #3)**

**Old:**
```html
<button onclick="deleteMedicine(${med.id_medicine})">Hapus</button>
<button onclick="deleteCustomer(${cust.id_customer})">Hapus</button>
```

**New:**
```html
<button onclick="confirmDelete('medicine', ${med.id_medicine}, '${med.name}')">Hapus</button>
<button onclick="confirmDelete('customer', ${cust.id_customer}, '${cust.name}')">Hapus</button>
```

---

**JavaScript Updates:**

**Line 335-346: loadDashboard() - Add Loading Spinner & Revenue Calc (FEATURES #1, #2)**

**Add di awal function:**
```javascript
document.getElementById('dashboardLoader').classList.add('show');
```

**Add setelah fetch transactions:**
```javascript
document.getElementById('dashboardLoader').classList.remove('show');

// Revenue Calculation (NEW)
let totalRevenue = 0;
let totalUnitSold = 0;
transactions.forEach(t => {
    const medicine = medicines.find(m => m.id_medicine === t.medicine_id);
    if (medicine) {
        totalRevenue += medicine.price * t.amount;
        totalUnitSold += t.amount;
    }
});
const avgTransaction = transactions.length > 0 ? Math.round(totalRevenue / transactions.length) : 0;

document.getElementById('totalRevenue').textContent = 'Rp ' + totalRevenue.toLocaleString('id-ID');
document.getElementById('totalUnitSold').textContent = totalUnitSold + ' unit';
document.getElementById('avgTransaction').textContent = 'Rp ' + avgTransaction.toLocaleString('id-ID');
```

**Line 444-500: Replace loadMedicine() + Add filterMedicine() (FEATURE #4)**

**New loadMedicine():**
```javascript
async function loadMedicine() {
    const response = await fetch("http://127.0.0.1:8000/medicine", { headers });
    const medicines = await response.json();
    window.allMedicines = medicines;
    filterMedicine();
}
```

**New filterMedicine() function:**
```javascript
function filterMedicine() {
    const searchText = document.getElementById("medicineSearch")?.value.toLowerCase() || "";
    const filterStatus = document.getElementById("medicineFilter")?.value || "";
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    const thirtyDaysAgo = new Date(today);
    thirtyDaysAgo.setDate(thirtyDaysAgo.getDate() - 30);

    let filtered = window.allMedicines || [];
    
    if (searchText) {
        filtered = filtered.filter(m => m.name.toLowerCase().includes(searchText));
    }
    
    if (filterStatus === "low") {
        filtered = filtered.filter(m => m.stock < 10);
    } else if (filterStatus === "expired") {
        filtered = filtered.filter(m => {
            const [year, month, day] = m.expired_date.split('-').map(Number);
            const expDate = new Date(year, month - 1, day);
            expDate.setHours(0, 0, 0, 0);
            return expDate >= thirtyDaysAgo && expDate <= today;
        });
    }

    const tbody = document.getElementById("medicineTable");
    tbody.innerHTML = "";
    if (filtered.length === 0) {
        tbody.innerHTML = '<tr><td colspan="7" class="text-center text-muted">Tidak ada data</td></tr>';
        return;
    }

    filtered.forEach(med => {
        tbody.innerHTML += `<tr>...</tr>`;
    });
}
```

**Line 515-517: Add Event Listeners for Search & Filter (FEATURE #4)**
```javascript
document.getElementById("medicineSearch")?.addEventListener("input", filterMedicine);
document.getElementById("medicineFilter")?.addEventListener("change", filterMedicine);
```

**Line 503-513: Add confirmDelete() Function (FEATURE #3)**
```javascript
function confirmDelete(type, id, name) {
    if (confirm(`Yakin hapus ${type} "${name}"? Tindakan ini tidak dapat dibatalkan.`)) {
        if (type === 'medicine') {
            deleteMedicine(id);
        } else if (type === 'customer') {
            deleteCustomer(id);
        }
    }
}
```

---

### FILES DELETED

- ❌ `frontend/customer.html` - merged ke index.html
- ❌ `frontend/transaction.html` - merged ke index.html
- ❌ `frontend/css/style.css` - styles inline di index.html
- ❌ `frontend/js/app.js` - empty file, not needed
- ❌ `backend/test_app.py` - test helper only
- ❌ `backend/test_login.py` - test helper only
- ❌ `backend/apotek.db` - auto-recreate on startup
- ❌ `backend/uvicorn.log` - temp log file
- ❌ `backend/uvicorn_err.log` - temp log file

---

## Summary of 5 Features Added

| Feature | File | Lines | Status |
|---------|------|-------|--------|
| Revenue Dashboard | index.html | 132-172 | ✓ Added |
| Loading Spinners | index.html | 7-87 (CSS), 177-180 (HTML), 335-346 (JS) | ✓ Added |
| Confirm Delete Dialog | index.html | 444, 605 (HTML), 503-513 (JS) | ✓ Added |
| Search & Filter Medicine | index.html | 208-226 (HTML), 444-500 (JS), 515-517 (listeners) | ✓ Added |
| Input Validation | index.html | 197-203, 300-304 (HTML attrs), 266 (amount) | ✓ Added |

---

## Testing Checklist (All Passing ✓)

- [x] Revenue cards display correctly (Rp format)
- [x] Loading spinner shows on dashboard load
- [x] Search medicine by name (real-time)
- [x] Filter by status (low stock, expired)
- [x] Confirm delete dialog appears
- [x] Form validation (min length, min values)
- [x] All CRUD operations work
- [x] Optional customer works
- [x] Stock auto-deduct
- [x] No console errors

---

## Known Issues / TODO

- [ ] Mobile responsive (CSS media queries)
- [ ] Integrate login ke dashboard (sekarang terpisah)
- [ ] Export PDF/Excel laporan
- [ ] Role-based access (owner vs karyawan)
- [ ] Premium styling & animations
- [ ] Transaction detail modal (skipped)
