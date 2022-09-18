#!/bin/bash

#alias k8prd='kubectl --kubeconfig ~/.kube/config'

# Deploy the database
k8prd apply -f postgres -n t20med

# Deploy the monolith
k8prd apply -f monolith -n t20med