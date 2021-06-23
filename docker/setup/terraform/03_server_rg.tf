# ------------------------------
# Server Resource Group
# ------------------------------

# Create the server resource group if it doesn't exist
resource "azurerm_resource_group" "server" {
  name     = "${var.RESOURCE_GROUP_NAME}server"
  location = var.location

  tags = {}
}
