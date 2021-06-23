# ------------------------------
# Data Resource Group
# ------------------------------

# Create a data resource group if it doesn't exist
resource "azurerm_resource_group" "data" {
  name     = "${var.RESOURCE_GROUP_NAME}data"
  location = var.location

  tags = {}
}

# Generate random text for a unique storage account name
resource "random_id" "randomId" {
  keepers = {
    # Generate a new ID only when a new resource group is defined
    resource_group = azurerm_resource_group.vm.name
  }
  
  byte_length = 3
}

# Create server table storage account if it doesn't exist
resource "azurerm_storage_account" "serverTablesName" {
  name                      = "${var.serverTablesName}${random_id.randomId.hex}"
  resource_group_name       = azurerm_resource_group.data.name
  location                  = azurerm_resource_group.data.location
  account_kind              = "Storage"
  account_tier              = "Standard"
  account_replication_type  = "GRS"
}

# Create server blob storage account if it doesn't exist
resource "azurerm_storage_account" "serverBlobsName" {
  name                      = "${var.serverBlobsName}${random_id.randomId.hex}"
  resource_group_name       = azurerm_resource_group.data.name
  location                  = azurerm_resource_group.data.location
  account_kind              = "Storage"
  account_tier              = "Standard"
  account_replication_type  = "GRS"
}

# Create client blob storage account if it doesn't exist
resource "azurerm_storage_account" "clientBlobsName" {
  name                      = "${var.clientBlobsName}${random_id.randomId.hex}"
  resource_group_name       = azurerm_resource_group.data.name
  location                  = azurerm_resource_group.data.location
  account_kind              = "Storage"
  account_tier              = "Standard"
  account_replication_type  = "GRS"
}

resource "azurerm_storage_container" "clientsauth" {
  name                  = "clientsauth"
  storage_account_name  = azurerm_storage_account.serverTablesName.name
  container_access_type = "private"
}

resource "azurerm_storage_container" "pendingemails" {
  name                  = "pendingemails"
  storage_account_name  = azurerm_storage_account.serverTablesName.name
  container_access_type = "private"
}

resource "azurerm_storage_container" "users" {
  name                  = "users"
  storage_account_name  = azurerm_storage_account.serverTablesName.name
  container_access_type = "private"
}

resource "azurerm_storage_container" "emails" {
  name                  = "emails"
  storage_account_name  = azurerm_storage_account.serverBlobsName.name
  container_access_type = "private"
}

resource "azurerm_storage_container" "mailbox" {
  name                  = "mailbox"
  storage_account_name  = azurerm_storage_account.serverBlobsName.name
  container_access_type = "private"
}

resource "azurerm_storage_container" "secretsopwencluster" {
  name                  = "secretsopwencluster"
  storage_account_name  = azurerm_storage_account.serverBlobsName.name
  container_access_type = "private"
}

resource "azurerm_storage_container" "sendgridinboundemails" {
  name                  = "sendgridinboundemails"
  storage_account_name  = azurerm_storage_account.serverBlobsName.name
  container_access_type = "private"
}

resource "azurerm_storage_container" "compressedpackages" {
  name                  = "compressedpackages"
  storage_account_name  = azurerm_storage_account.clientBlobsName.name
  container_access_type = "private"
}

# Create a server queue if it doesn't exist
resource "azurerm_servicebus_namespace" "data" {
  name                = var.serverQueuesName
  location            = azurerm_resource_group.data.location
  resource_group_name = azurerm_resource_group.data.name
  sku                 = "Standard"
  zone_redundant      = false
}

resource "azurerm_servicebus_namespace_authorization_rule" "data" {
  name                = var.serverQueuesSasName
  namespace_name      = azurerm_servicebus_namespace.data.name
  resource_group_name = azurerm_resource_group.data.name
  send                = true
  listen              = true
  manage              = true
}

resource "azurerm_servicebus_queue" "serverQueueSendgridMime" {
  name                = var.serverQueueSendgridMime
  resource_group_name = azurerm_resource_group.data.name
  namespace_name      = azurerm_servicebus_namespace.data.name
  max_size_in_megabytes = 512
}

resource "azurerm_servicebus_queue" "serverQueueEmailSend" {
  name                = var.serverQueueEmailSend
  resource_group_name = azurerm_resource_group.data.name
  namespace_name      = azurerm_servicebus_namespace.data.name
  max_size_in_megabytes = 5120
}

resource "azurerm_servicebus_queue" "serverQueueClientPackage" {
  name                = var.serverQueueClientPackage
  resource_group_name = azurerm_resource_group.data.name
  namespace_name      = azurerm_servicebus_namespace.data.name
  max_size_in_megabytes = 5120
}

resource "azurerm_servicebus_queue" "mailboxreceived" {
  name                = "mailboxreceived"
  resource_group_name = azurerm_resource_group.data.name
  namespace_name      = azurerm_servicebus_namespace.data.name
  max_size_in_megabytes = 1024
}

resource "azurerm_servicebus_queue" "mailboxsent" {
  name                = "mailboxsent"
  resource_group_name = azurerm_resource_group.data.name
  namespace_name      = azurerm_servicebus_namespace.data.name
  max_size_in_megabytes = 1024
}

resource "azurerm_servicebus_queue" "register" {
  name                = "register"
  resource_group_name = azurerm_resource_group.data.name
  namespace_name      = azurerm_servicebus_namespace.data.name
  max_size_in_megabytes = 1024
}

resource "azurerm_servicebus_queue" "service" {
  name                = "service"
  resource_group_name = azurerm_resource_group.data.name
  namespace_name      = azurerm_servicebus_namespace.data.name
  max_size_in_megabytes = 1024
}
