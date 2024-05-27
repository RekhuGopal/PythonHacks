locals {
    domain = "exercise.io"
    #arecords = "replace the string literal local.arecords with an expression that builds a list of strings (FQDNs) from local.service_endpoints map values and suffixes each string in the list with local.domain. As an example: ['alertmanager.exercise.io', 'grafana.exercise.io, ...]"

    #arecords = [local.service_endpoints.list_a, local.service_endpoints.list_b]
    # records = [[alertmanager.exercise.io]]

    service_endpoints = {
        "list_a" = ["alertmanager","grafana","kibana","prometheus","audit","audit-service","docs","iam","iam-service"]
        "list_b" = ["test","test-agent","test-service","data-service","dbc-service"]
        "list_c" = ["tsdb-service","tsdb-ingestion-service","tsdb-configuration-service"]
        "list_d" = ["executor","executor-service"]
        "list_e" = ["example-service"]
        "list_f" = ["some-service"]
    }

   arecords = flatten([for key , value in local.service_endpoints :  [for endpoints in value : endpoints + local.domain ]])
  
}

output "arecords" {
    value = local.arecords
}