variable "RESOURCE_GROUP_NAME" {
  type        = string
  default     = "opwen"
  description = "The prefix which should be used for all resources in this application."
}

variable "location" {
  type        = string
  default     = "eastus"
  description = "The Azure Region in which all resources in this example should be created."
}

variable "vmName" {
  type        = string
  default     = "opwenvm"
  description = "The name of Virtual Machine resource group."
}

variable "appinsightsName" {
  type        = string
  default     = "opwenlogs"
}

variable "clientBlobsName" {
  type        = string
  default     = "opwenclient"
  description = "The name of the client Blobs storage account within the Data resource group."
}

variable "serverBlobsName" {
  type        = string
  default     = "opwenserverblobs"
  description = "The name of the server Blobs storage account within the Data resource group."
}

variable "serverTablesName" {
  type        = string
  default     = "opwenservertables"
  description = "The name of the server Tables storage account within the Data resource group."
}

variable "serverQueuesName" {
  type        = string
  default     = "opwenserverqueues"
  description = "The name of the server Queues Service Bus Namespace within the Data resource group."
}

variable "serverQueuesSasName" {
  type    = string
  default = "celery"
}

variable "serverQueueSendgridMime" {
  type    = string
  default = "inbound"
}

variable "serverQueueClientPackage" {
  type    = string
  default = "written"
}

variable "serverQueueEmailSend" {
  type    = string
  default = "send"
}
