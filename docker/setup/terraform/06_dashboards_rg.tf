# ------------------------------
# Dashboards Resource Group
# ------------------------------

# Create a resource group if it doesn't exist
resource "azurerm_resource_group" "dashboards" {
  name     = "dashboards"
  location = var.location

  tags = {}
}
