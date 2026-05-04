variable "lambda_names" {
  default = [
    "Deepa-product-service",
    "Deepa-cart-service",
    "Deepa-orders-service",
    "Deepa-review-service"
  ]
}

variable "dynamodb_tables" {
  default = [
    "dee-products",
    "dee-cart",
    "dee-orders",
    "dee-reviews"
  ]
}

variable "s3_bucket_name" {
  default = "deepa-ecommerce-frontend"
}

variable "cloudfront_domain" {
  default = "d1zro28al7bpzb.cloudfront.net"
}