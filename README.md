# 🛒 DEEStore
### Cloud-Native Serverless E-Commerce Platform on AWS
---

## 🌐 Live Demo

🔗 **URL:** https://dr6mr82mn4hj9.cloudfront.net

Experience the DEEStore — blazing fast, elegantly designed, and globally delivered via AWS CloudFront CDN.

---

## 🎯 Project Overview

DEEStore is a **fully serverless, cloud-native e-commerce platform** built on AWS. Designed with a microservice-inspired AWS Lambda architecture, every business capability is its own independent, deployable service.

The platform supports:

- 🛍️ **Full shopping experience** for customers — browse, cart, and order
- 🔐 **Amazon Cognito authentication** — secure signup, login, and session management
- 📦 **Real-time order management** — place and track orders with history
- ⭐ **Product review system** — submit and view reviews per product
- 📊 **Comprehensive observability** via CloudWatch Logs, Dashboards, and Alarms
- 🔄 **CI/CD pipeline** via GitHub Actions for automated deployments

All infrastructure is managed via **Terraform (Infrastructure as Code)**, with the frontend served globally through **AWS CloudFront + S3**.

---

## 🏗️ System Architecture

```
                     ┌──────────────────────────────────────────┐
                     │             User Browser                  │
                     └──────────────────┬───────────────────────┘
                                        │ HTTPS
                     ┌──────────────────▼───────────────────────┐
                     │           AWS CloudFront CDN              │
                     │   https://dr6mr82mn4hj9.cloudfront.net    │
                     └──────────────────┬───────────────────────┘
                                        │
                     ┌──────────────────▼───────────────────────┐
                     │      Amazon S3 — Static Frontend          │
                     │     (HTML / CSS / JS Hosting + Assets)    │
                     └──────────────────┬───────────────────────┘
                                        │
                     ┌──────────────────▼───────────────────────┐
                     │        Amazon Cognito Hosted UI           │
                     │   (Signup · Login · Session Management)   │
                     └──────────────────┬───────────────────────┘
                                        │
                     ┌──────────────────▼───────────────────────┐
                     │           API Gateway HTTP API            │
                     └───┬──────────┬───────────┬───────────┬───┘
                         │          │           │           │
            ┌────────────▼──┐  ┌────▼──────┐  ┌▼────────┐ ┌▼──────────────┐
            │ Product Svc   │  │ Cart Svc  │  │Order Svc│ │  Review Svc   │
            │ Catalog &     │  │ Add/Remove│  │Place &  │ │ Submit &      │
            │ Listings      │  │ Update    │  │ History │ │ View Reviews  │
            └───────┬───────┘  └─────┬─────┘  └────┬────┘ └──────┬────────┘
                    │               │              │              │
                    └───────────────┴──────────────┴──────────────┘
                                          │
                     ┌────────────────────▼─────────────────────┐
                     │              Amazon DynamoDB              │
                     │  ┌──────────┐ ┌─────────┐ ┌──────────┐  │
                     │  │dee-products│ │dee-cart│ │dee-orders│  │
                     │  └──────────┘ └─────────┘ └──────────┘  │
                     │              ┌──────────┐                │
                     │              │dee-reviews│               │
                     │              └──────────┘                │
                     └──────────────────────────────────────────┘
                                          │
                     ┌────────────────────▼─────────────────────┐
                     │           Observability Layer             │
                     │  CloudWatch Logs · Dashboard · Alarms     │
                     └──────────────────────────────────────────┘
                                          │
                     ┌────────────────────▼─────────────────────┐
                     │        CI/CD & IaC Layer                  │
                     │  GitHub Actions · Terraform-Managed Infra │
                     └──────────────────────────────────────────┘
```

---

## 🔐 Authentication — Amazon Cognito

DEEStore uses **Amazon Cognito** as its identity provider, offering a secure and managed authentication layer.

```
                ┌─────────────────────────────────┐
                │          Login / Signup          │
                │        🛒  DEEStore              │
                └──────────────┬──────────────────┘
                               │
               ┌───────────────┴──────────────────┐
               │                                   │
     ┌─────────▼──────────┐             ┌──────────▼─────────┐
     │    🆕  SIGNUP      │             │    🔑  LOGIN       │
     │                    │             │                     │
     │  Register Account  │             │  Authenticate via   │
     │  Cognito Hosted UI │             │  Cognito Hosted UI  │
     └─────────┬──────────┘             └──────────┬─────────┘
               │                                   │
               └──────────────┬────────────────────┘
                              │
                  ┌───────────▼────────────┐
                  │  Authenticated Session  │
                  │  ───────────────────   │
                  │  ✅ Browse Products    │
                  │  ✅ Manage Cart        │
                  │  ✅ Place Orders       │
                  │  ✅ View Order History │
                  │  ✅ Submit Reviews     │
                  │  ✅ User-Scoped Data   │
                  └───────────┬────────────┘
                              │
                  ┌───────────▼────────────┐
                  │  API Gateway + Lambda  │
                  │       DynamoDB         │
                  └────────────────────────┘
```

### Cognito Features
- User Signup & Login via **Hosted UI**
- Secure **session management**
- **User-scoped data isolation** — each user sees only their own cart, orders, and reviews

---

## 🔄 System Flow

```
 1. 🧑  User visits DEEStore Platform
         │
         ▼
 2. 🌐  CloudFront CDN serves the static frontend (from S3)
         │
         ▼
 3. 🔐  Cognito Hosted UI — User signs up or logs in
         │
         ▼
 4. 📦  Product Service  → fetch product catalog and listings
         │
         ▼
 5. 🛒  Cart Service     → add, update, and remove cart items
         │
         ▼
 6. 📋  Order Service    → place order, view order history
         │
         ▼
 7. ⭐  Review Service   → submit and view product reviews
         │
         ▼
 8. 💾  DynamoDB         → persist all products, carts, orders, and reviews
         │
         ▼
 9. 📊  CloudWatch       → log, monitor, and alert on all service activity
         │
         ▼
10. 🔄  GitHub Actions   → CI/CD pipeline triggers Terraform deployment on push
         │
         ▼
11. ✅  All infrastructure deployed and managed via Terraform
```

---

## ✨ Core Features

| Feature | Description |
|---|---|
| 🛒 Product Catalog | Full product listings fetched dynamically from DynamoDB |
| 🔐 Cognito Auth | Secure signup, login, and session management via AWS Cognito |
| 🛍️ Cart Management | Add, increase/decrease quantity, and remove items — per user |
| 📦 Order Processing | Place orders, auto-generate order IDs, view full order history |
| ⭐ Product Reviews | Submit ratings and written reviews per product, view all reviews |
| ☁️ Global CDN | AWS CloudFront for ultra-fast worldwide delivery |
| 📡 Observability | CloudWatch Logs, Dashboard, Alarms for all Lambda services |
| ⚙️ Microservices | Four independently deployable, stateless Lambda services |
| 🧪 Tested Services | PyTest-based unit test suite for every Lambda function |
| 🏗️ IaC Deployments | Entire infrastructure declared and managed via Terraform |
| 🔄 CI/CD Pipeline | GitHub Actions for automated Terraform validation and deployment |

---

## 📁 Project Structure

```
deestore/
│
├── frontend/                   ← Static UI (S3 hosted)
│   └── index.html
│
├── backend/                    ← AWS Lambda functions
│   ├── products/
│   │   └── handler.py          ← Product service
│   ├── cart/
│   │   └── handler.py          ← Cart service
│   ├── orders/
│   │   └── handler.py          ← Order service
│   └── reviews/
│       └── handler.py          ← Review service
│
├── tests/                      ← PyTest unit tests
│   ├── test_products.py
│   ├── test_cart.py
│   ├── test_orders.py
│   └── test_reviews.py
│
├── terraform/                  ← Infrastructure as Code
│   ├── main.tf                 ← Core infra — Lambda, API GW, S3, CF, DynamoDB, Cognito, IAM
│   ├── variables.tf
│   └── outputs.tf
│
└── .github/
    └── workflows/              ← GitHub Actions CI/CD pipeline
```

---

## 🧰 Tech Stack

### Frontend

| Technology | Purpose |
|---|---|
| HTML5 / CSS3 | Markup and styling |
| JavaScript (ES6+) | Application logic, dynamic rendering |
| Amazon S3 | Static site hosting |
| AWS CloudFront | Global CDN — fast, low-latency delivery |

### Backend

| Technology | Purpose |
|---|---|
| Python 3.11 | AWS Lambda service functions |
| boto3 | AWS SDK for DynamoDB interactions |
| Decimal → JSON | Custom serialization for DynamoDB responses |
| CORS | Enabled on all Lambda handlers for frontend integration |

### Infrastructure

| Technology | Purpose |
|---|---|
| Terraform | Infrastructure as Code — full AWS lifecycle management |
| AWS Lambda | Serverless compute for all microservices |
| API Gateway | Route and manage all REST API calls |
| Amazon DynamoDB | NoSQL database for products, carts, orders, and reviews |
| Amazon S3 | Frontend static hosting |
| AWS CloudFront | Global CDN for fast delivery |
| Amazon Cognito | Authentication — User Pool and Hosted UI |
| AWS CloudWatch | Logging, dashboards, and automated alarms |
| AWS IAM | Roles, policies, and permissions |
| GitHub Actions | CI/CD pipeline — automated deploy on push |

---

## 📡 API Reference

**Base URL:** API Gateway endpoint

### 📦 Product Service

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/products` | Fetch all products |

### 🛒 Cart Service

| Method | Endpoint | Description |
|---|---|---|
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

### 📋 Order Service

| Method | Endpoint | Description |
|---|---|---|
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

### ⭐ Review Service

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/reviews?product_id=xxx` | Get reviews for a product |
| `POST` | `/reviews` | Submit a new review |

---

## 🗄️ Database Design

### Products Table — `dee-products`

| Attribute | Type | Key |
|---|---|---|
| `product_id` | Number | Partition Key |
| `name` | String | — |
| `price` | Number | — |
| `description` | String | — |

### Cart Table — `dee-cart`

| Attribute | Type | Key |
|---|---|---|
| `user_id` | String | Partition Key |
| `product_id` | Number | Sort Key |
| `quantity` | Number | — |

### Orders Table — `dee-orders`

| Attribute | Type | Key |
|---|---|---|
| `order_id` | String | Partition Key |
| `user_id` | String | — |
| `items` | List | — |
| `total` | Number | — |

### Reviews Table — `dee-reviews`

| Attribute | Type | Key |
|---|---|---|
| `product_id` | String | Partition Key |
| `user_id` | String | Sort Key |
| `rating` | Number | — |
| `review` | String | — |

---

## 📊 Observability

### CloudWatch Logs

Logs are collected from all Lambda services:
- Product Service
- Cart Service
- Order Service
- Review Service
- API Gateway access logs

### CloudWatch Dashboard

The centralised dashboard monitors:

| Metric | Service |
|---|---|
| Lambda Invocations | All services |
| Lambda Duration | All services |
| Lambda Errors | All services |
| Lambda Throttles | All services |
| DynamoDB Read/Write | All tables |
| API Gateway Latency | API Gateway |

### CloudWatch Alarms

```
┌────────────────────────────────────────────────┐
│              CloudWatch Alarms                  │
│                                                 │
│  🔴 Product Service Errors  → Errors > 5       │
│  🔴 Review Service Errors   → Errors > 5       │
│  🔴 API Latency             → Latency > 2000ms │
│  🔴 DynamoDB Read Usage     → High utilization │
│  🔴 Lambda Invocation Spike → Unusual volume   │
└────────────────────────────────────────────────┘
```

---

## 🔄 CI/CD Pipeline — GitHub Actions

```
Developer Push
      │
      ▼
GitHub Repository
      │
      ▼
GitHub Actions Trigger
      │
      ▼
Terraform Validation  →  terraform validate
      │
      ▼
Terraform Plan        →  terraform plan
      │
      ▼
Terraform Apply       →  terraform apply
      │
      ▼
AWS Infrastructure Updated ✅
```

The pipeline ensures every push to `main` is validated and deployed automatically — zero manual steps required.

---

## ☁️ Infrastructure — Terraform

All AWS infrastructure is fully managed via Terraform:

| File | Purpose |
|---|---|
| `main.tf` | Core infrastructure — Lambda, API Gateway, S3, CloudFront, DynamoDB, Cognito, IAM |
| `variables.tf` | Configurable input parameters |
| `outputs.tf` | Infrastructure outputs — URLs, ARNs, table names |

Key benefits:
- ✅ Version-controlled infrastructure
- ✅ Fully repeatable deployments
- ✅ Automated resource provisioning
- ✅ Environment consistency

---

## 🧪 Testing

Every Lambda service has independent unit tests to ensure reliability in isolation.

```bash
# Install dependencies
pip install pytest boto3

# Run all backend tests
pytest tests/ -v

# Run individual service tests
pytest tests/test_products.py -v
pytest tests/test_cart.py -v
pytest tests/test_orders.py -v
pytest tests/test_reviews.py -v
```

### Test Coverage

| Service | Coverage Areas |
|---|---|
| Products | API output validation, data format |
| Cart | Add/update/remove logic, user isolation |
| Orders | Order creation, cart cleanup, edge cases |
| Reviews | Submit/retrieve logic, user-product scoping |

---

## 🚀 Getting Started

### Prerequisites
- Python 3.11
- Terraform
- AWS CLI configured
- Node.js (optional — for build tooling)

### 1. Clone the repository
```bash
git clone https://github.com/Deepasuresh67/ecommerce.git
cd ecommerce
```

### 2. Deploy infrastructure
```bash
cd terraform/
terraform init
terraform validate
terraform plan
terraform apply
```

### 3. Access the platform
Open the CloudFront URL output from Terraform — or visit the live demo directly:
🔗 https://dr6mr82mn4hj9.cloudfront.net

---

## 🔮 Future Improvements

- 💳 **Payment Integration** — Stripe / Razorpay checkout flow
- 📊 **Admin Dashboard** — product management, revenue analytics
- 🔍 **Smart Search & Filtering** — keyword, category, and price range filters
- 📦 **Order Status Tracking** — real-time status updates (processing → shipped → delivered)
- 📩 **Order Confirmation Emails** — via Amazon SES
- 🛡️ **API Rate Limiting** — API Gateway throttling and request authorization
- 🔔 **SNS Notifications** — email alerts on CloudWatch alarm triggers
- 💰 **Flash Sales** — time-limited deals with countdown timers and stock limits

---

## 🧠 What I Learned

- ⚡ **Serverless Architecture** — designing and deploying AWS Lambda-based microservices
- 🏗️ **Infrastructure as Code** — managing full cloud resources declaratively with Terraform
- 🧩 **Microservice Design** — loosely coupled, independently deployable Lambda services
- 🔐 **Cloud Authentication** — integrating Amazon Cognito with a hosted UI and session management
- 🔄 **Full-Stack System Design** — connecting a static frontend to Lambda backend via API Gateway
- 🧪 **Modular Testing** — writing reliable PyTest suites for each microservice
- 📊 **Observability Engineering** — structured logging, CloudWatch dashboards, and alarms
- 🔄 **CI/CD Pipelines** — automating infrastructure deployment with GitHub Actions
