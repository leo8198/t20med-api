### Kubernetes Configuration Environment

In production we use AWS EKS to manage the kubernetes cluster. We also use
the fully self-managed AWS RDS for the PostgreeSQL database

### Canary deployment

For canary deployment we use AWS route 53 to route 50% of the traffic
for the new API version. The canary subdomain is canary.api.t20med.com

