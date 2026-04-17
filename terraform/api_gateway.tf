resource "aws_api_gateway_rest_api" "ecommerce_api" {
  name = "deepa-ecommerce-api"

  lifecycle {
    ignore_changes = all
  }
}