resource "aws_cloudwatch_log_group" "product_logs" {
  name              = "/aws/lambda/Deepa-product-service"
  retention_in_days = 7
}

resource "aws_cloudwatch_log_group" "cart_logs" {
  name              = "/aws/lambda/Deepa-cart-service"
  retention_in_days = 7
}

resource "aws_cloudwatch_log_group" "orders_logs" {
  name              = "/aws/lambda/Deepa-order-service"
  retention_in_days = 7
}