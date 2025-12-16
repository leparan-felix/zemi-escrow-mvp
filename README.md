Instructions
1️⃣Clone the Repository
git clone https://github.com/leparan-felix/zemi-escrow-mvp.git

cd zemi-escrow-mvp

2️⃣ Create & Activate Virtual Environment
python -m venv venv
source venv/bin/activate

3️⃣ Install Dependencies
pip install -r requirements.txt

4️⃣ Run Migrations
python manage.py migrate

5️⃣ Start Server
python manage.py runserver



Server runs at: `http://127.0.0.1:8000`


## API Endpoints

| Endpoint | Method | Request Body | Description |

| `/api/create_order/` | POST | `phone`, `amount`, `product_description` | Creates a new order, returns order_reference and delivery code |
| `/api/payment_webhook/` | POST | `order_reference`, `transaction_id` | Marks order as paid and records payment |
| `/api/confirm_delivery/` | POST | `order_reference`, `delivery_code` | Confirms delivery and releases funds to seller |
| `/api/stk_push/` | POST | `buyer_phone`, `amount` | Simulates M-Pesa STK Push initiation |
| `/api/confirm_stk/` | POST | `transaction_ref` | Confirms simulated STK payment |
| `/api/release_funds/` | POST | `seller_phone`, `amount` | Simulates B2C disbursement |

---

## Database Models

- **Order**
  - `order_reference`: unique identifier
  - `phone_hashed`: buyer phone (hashed)
  - `amount`
  - `product_description`
  - `status`: `awaiting_payment`, `paid`, `completed`
  - `delivery_code`: 6-digit code for buyer confirmation

- **Payment**
  - `order`: FK to Order
  - `transaction_id`
  - `timestamp`

---

## Flow Logic

1. Buyer creates order → `awaiting_payment`  
2. Payment webhook updates order → `paid`  
3. Buyer confirms delivery → `completed` → funds released  

Error handling ensures:
- Orders cannot be paid twice
- Wrong delivery codes are rejected
- Missing fields return 400

---

## Design & Product Thinking

1️⃣ **Real M-Pesa Integration**
- Register a Safaricom Daraja App
- Use OAuth token
- Replace simulated services with real endpoints
- Implement callback URLs

2️⃣ **Failed Payments / Timeouts**
- Payment status: pending, failed, expired
- Track timeouts with background jobs
- Cancel unpaid orders after defined window

3️⃣ **Fraud / Abuse Prevention**
- Rate-limit payments
- Verify phone ownership
- Monitor repeated failed delivery confirmations
- Introduce buyer/seller reputation scoring

4️⃣ **Product Improvement**
- Buyer–Seller dispute resolution flow
- Increases trust and reduces abuse

---

## Author
- Name: Felix Leparan
- Shared with: CreatorOfGods
- Project: Zemi Escrow MVP
