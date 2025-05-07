# 🔗 Serverless URL Shortener

A fully serverless, scalable URL shortener application built using AWS services. The project allows users to generate short URLs for any valid web address and automatically redirects them when accessed. The frontend is hosted on S3, and backend logic is powered by AWS Lambda and API Gateway with persistent storage in DynamoDB.

---

## 🛠️ Features

- Generate short URLs for long web addresses
- Automatically redirect users from short URL to the original destination
- Real-time request handling using AWS Lambda
- Scalable architecture with global CDN via Amazon CloudFront
- Domain-secured with HTTPS using AWS Certificate Manager (ACM)
- DNS management through Amazon Route 53
- Clean and responsive frontend hosted on Amazon S3

---

## 🧱 Architecture

![Architecture Diagram](./architecture.png)

**Tech Stack:**

- **Frontend:** HTML/CSS/JavaScript hosted on Amazon S3
- **Backend:** Python (AWS Lambda)
- **API Gateway:** HTTP API to connect frontend and Lambda functions
- **Database:** DynamoDB (NoSQL) to store short code to URL mappings
- **Routing & CDN:** Amazon Route 53 and CloudFront
- **Security:** HTTPS enabled with ACM

---

## 📁 Project Structure

url-shortener/
├── backend/
│   ├── CreateShortURL.py
│   ├── RedirectShortURL.py
│   └── requirements.txt
├── frontend/
│   ├── index.html
├── architecture-diagram.png
├── README.md


## 🚀 Getting Started

### 1. Deploy Infrastructure (Manually via AWS Console or IaC like CDK/Terraform)

- Create two Lambda functions:
  - `CreateShortURL`
  - `RedirectShortURL`
- Create an HTTP API in API Gateway with:
  - `POST /shorten → CreateShortURL`
  - `GET /{shortCode} → RedirectShortURL`
- Set up DynamoDB table `URLTable` with:
  - `shortCode` (Partition Key)
  - `longURL`
- Host the frontend using S3 static website hosting.
- Create a CloudFront distribution pointing to the S3 bucket.
- Use ACM to issue an HTTPS certificate.
- Point Route 53 domain to CloudFront.

### 2. Frontend Configuration

Update the API endpoint in `index.html` under the `fetch()` call:
```js
fetch("https://<your-api-id>.execute-api.<region>.amazonaws.com/shorten", {...})