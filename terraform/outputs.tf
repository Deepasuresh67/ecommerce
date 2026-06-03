output "product_api" {
  value = "https://8h0awzpfti.execute-api.ap-southeast-1.amazonaws.com/v1/products"
}

output "cart_api" {
  value = "https://8h0awzpfti.execute-api.ap-southeast-1.amazonaws.com/v1/cart"
}

output "orders_api" {
  value = "https://8h0awzpfti.execute-api.ap-southeast-1.amazonaws.com/v1/orders"
}

output "frontend_s3" {
  value = "http://deepa-ecommerce-frontend.s3-website-ap-southeast-1.amazonaws.com"
}

output "cloudfront_url" {
  value = "https://d1zro28al7bpzb.cloudfront.net"
}

output "cognito_user_pool_id" {
  value = aws_cognito_user_pool.deestore_users.id
}

output "cognito_client_id" {
  value = aws_cognito_user_pool_client.deestore_client.id
}

output "cognito_domain" {
  value = aws_cognito_user_pool_domain.deestore_domain.domain
}
