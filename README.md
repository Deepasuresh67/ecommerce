# DeeStore – E-Commerce Application

A full-stack serverless e-commerce platform built on AWS — browse products, manage your cart, and place orders seamlessly.

## 🌐 Live Demo

Frontend (S3) -> http://deepa-ecommerce-frontend.s3-website-ap-southeast-1.amazonaws.com
CDN (CloudFront) ->  https://d1zro28al7bpzb.cloudfront.net
API Gateway -> https://8h0awzpfti.execute-api.ap-southeast-1.amazonaws.com/v1

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | HTML, CSS, JavaScript |
| Backend | AWS Lambda (Python) |
| API Layer | AWS API Gateway |
| Database | AWS DynamoDB (NoSQL) |
| Hosting | AWS S3 + CloudFront |
| IaC | Terraform|

## Architecture

┌─────────────────────────────────────────────────────────┐
│                        USER                             │
│                    (Web Browser)                        │
└─────────────────────┬───────────────────────────────────┘
                      │  HTTPS Request
                      ▼
┌─────────────────────────────────────────────────────────┐
│                   CLOUDFRONT                            │
│                (CDN / Edge Cache)                       │
└────────────┬──────────────────────┬─────────────────────┘
             │ Static Assets        │ API Requests
             ▼                      ▼
┌────────────────────┐   ┌──────────────────────────────┐
│     S3 BUCKET      │   │        API GATEWAY           │
│  (Frontend Hosting)│   │   (REST API - /v1 routes)    │
│  HTML / CSS / JS   │   └──────────────┬───────────────┘
└────────────────────┘                  │ Invoke
                                        ▼
                         ┌──────────────────────────────┐
                         │       AWS LAMBDA             │
                         │      (Python - boto3)        │
                         │  ┌──────────────────────┐    │
                         │  │  products/handler.py  │   │
                         │  │  cart/handler.py      │   │
                         │  │  orders/handler.py    │   │
                         │  └──────────────────────┘    │
                         └──────────────┬───────────────┘
                                        │ Read / Write
                                        ▼
                         ┌──────────────────────────────┐
                         │          DYNAMODB            │
                         │        (NoSQL Database)      │
                         │  ┌─────────────────────┐     │
                         │  │  dee-products        │    │
                         │  │  dee-cart            │    │
                         │  │  dee-orders          │    │
                         │  └─────────────────────┘     │
                         └──────────────────────────────┘

**Data Flow:**
Frontend → API Gateway → AWS Lambda → DynamoDB

## Project Structure

```
deestore/
├── frontend/               # Static UI (S3 hosted)
│   ├── index.html 
│
├── backend/                # AWS Lambda functions
│   ├── products/
│   │   └── handler.py      # Product service
│   ├── cart/
│   │   └── handler.py      # Cart service
│   └── orders/
│       └── handler.py      # Order service
│
├── tests/                  # pytest unit tests
│   ├── test_products.py
│   ├── test_cart.py
│   └── test_orders.py
│
└── terraform/              # Infrastructure as Code (WIP)
    ├── main.tf
    ├── variables.tf
    └── outputs.tf
```

##  Features

###  User System
- Username-based login *(no signup required)*
- Session stored via `localStorage`
- Isolated cart and orders per user

###  Product Service
- Fetch all products from DynamoDB
- Dynamic product rendering on UI

###  Cart Service
- Add products to cart
- Increase / decrease item quantity
- Remove individual items
- Cart is user-specific

###  Order Service
- Place orders from selected cart items
- Auto-generate unique `order_id` per order
- Fetch order history per user
- Cart items removed after order is placed

---

## API Reference

###  Products

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/products` | Fetch all products |

---

###  Cart

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/cart?user_id=xxx` | Get cart items for a user |
| `POST` | `/cart` | Add item to cart |
| `DELETE` | `/cart` | Remove item from cart |

**POST /cart — Request Body:**
```json
{
  "user_id": "deepa",
  "product_id": 101,
  "quantity": 2
}
```

---

### Orders

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/orders?user_id=xxx` | Get all orders for a user |
| `POST` | `/orders` | Place a new order |

**POST /orders — Request Body:**
```json
{
  "user_id": "deepa",
  "items": [
    { "product_id": 101, "quantity": 2, "price": 499 }
  ],
  "total": 998
}
```


##  Database Design

###  Cart Table — `dee-cart`

| Attribute | Type | Key |
|-----------|------|-----|
| `user_id` | String | Partition Key |
| `product_id` | Number | Sort Key |
| `quantity` | Number | — |

---

###  Orders Table — `dee-orders`

| Attribute | Type |
|-----------|------|
| `order_id` | String |
| `user_id` | String |
| `items` | List |
| `total` | Number |

---

### Products Table — `dee-products`

| Attribute | Type |
|-----------|------|
| `product_id` | Number |
| `name` | String |
| `price` | Number |


## Application Flow

1. User enters username → session stored in localStorage
        │
        ▼
2. Products fetched from DynamoDB → displayed on UI
        │
        ▼
3. User adds items to cart → stored in dee-cart (DynamoDB)
        │
        ▼
4. User selects items → clicks "Place Order"
        │
        ▼
5. Order saved to dee-orders → cart items removed
        │
        ▼
6. User can view order history
```

##  Infrastructure & Deployment

### Current Setup (AWS Console)
All resources were initially created manually via AWS Console:

- Lambda Functions (Python)
- DynamoDB Tables
- API Gateway
- S3 Bucket (static hosting)
- CloudFront Distribution

### Backend Implementation Notes
- Written in **Python** using `boto3`
- Uses **Query-based retrieval** for DynamoDB
- Handles `Decimal` → JSON conversion
- CORS enabled for frontend integration

---

### Terraform — Infrastructure as Code

Terraform configuration is being developed to:

- Automate full backend deployment
- Recreate all infrastructure programmatically
- Enable reproducible environments across stages (dev/prod)

```bash
# Planned commands
terraform init
terraform plan
terraform apply
```

---

## Testing

Tests are written using **pytest** and cover all three services.

### Run Tests

```bash
# Install dependencies
pip install pytest boto3

# Run all tests
pytest tests/

# Run specific service tests
pytest tests/test_products.py
pytest tests/test_cart.py
pytest tests/test_orders.py
```

### Test Coverage

| Service | Coverage Areas |
|---------|---------------|
| Products | API output validation, data format |
| Cart | Add/update/remove logic, user isolation |
| Orders | Order creation, cart cleanup, edge cases |

---

## Future Enhancements
| 🔐 JWT / AWS Cognito Authentication 
| 💳 Payment Integration (Stripe / Razorpay)
| 📊 Admin Dashboard
| 🔍 Search & Filtering 
| 📦 Order Status Tracking
