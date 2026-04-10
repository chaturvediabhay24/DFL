**Cloud & DevOps --- Deep Dive**

*Interview Q&A*

**Kubernetes Internals**

1.  **Explain the Kubernetes architecture --- control plane and data
    plane.**

> Control plane: API Server (single entry point, validates requests,
> updates etcd), etcd (distributed key-value store of all cluster
> state), Scheduler (assigns pods to nodes based on resource requests,
> taints/tolerations, affinity rules), Controller Manager (runs
> controllers: ReplicaSet, Deployment, Node). Data plane: Kubelet (node
> agent --- pulls pod spec, manages containers), Kube-proxy (maintains
> iptables/IPVS rules for Service networking), Container Runtime
> (containerd/CRI-O). When you kubectl apply, the API server stores the
> desired state in etcd; controllers reconcile actual to desired state.

2.  **What are resource requests vs limits in Kubernetes? Why do they
    matter for ML?**

> Requests: guaranteed resources the scheduler uses for pod placement
> --- a node must have at least this much free. Limits: maximum
> resources a container can use --- exceeding CPU limit throttles the
> process; exceeding memory limit OOMKills it. For ML inference pods:
> set CPU/memory requests accurately to ensure pods land on nodes with
> sufficient capacity; set limits to prevent a runaway model from
> starving other pods. For GPU workloads: nvidia.com/gpu resource must
> be requested exactly (GPUs are not shared by default in K8s).

3.  **What are readiness and liveness probes?**

> Liveness probe: checks if the container is alive; failure triggers a
> restart. Use for deadlock detection. Readiness probe: checks if the
> container is ready to receive traffic; failure removes the pod from
> Service endpoints. Critical for ML inference: during model loading
> (which can take 30--60s for large models), the readiness probe should
> fail until the model is fully loaded --- preventing requests from
> hitting an uninitialized server. Startup probe: for slow-starting
> containers, delays liveness checks to avoid premature restarts.

4.  **What is a Kubernetes HPA (Horizontal Pod Autoscaler)?**

> HPA automatically adjusts the number of pod replicas based on observed
> metrics (CPU utilisation, memory, or custom metrics via the Metrics
> API). For ML inference: scale on GPU utilisation or request queue
> depth (via Prometheus custom metrics adapter). Key parameters:
> minReplicas, maxReplicas, targetAverageUtilisation. Scale-up is fast;
> scale-down has a stabilisation window (default 5 min) to avoid
> flapping. For LLM serving with variable request sizes, scaling on
> token throughput is more meaningful than CPU.

**AWS Services Deep Dive**

5.  **What is AWS IAM and how do IRSA (IAM Roles for Service Accounts)
    work?**

> IAM controls authentication (who) and authorisation (what) for AWS
> resources via users, groups, roles, and policies (JSON documents
> defining Allow/Deny on actions/resources). IRSA allows Kubernetes pods
> to assume AWS IAM roles without storing credentials --- the pod\'s
> service account is annotated with an IAM role ARN; the pod receives a
> projected OIDC token; AWS STS exchanges it for temporary credentials.
> This is the secure way for ML pods on EKS to access S3 (training
> data), ECR (images), or SageMaker --- no hardcoded AWS keys.

6.  **Explain the difference between SQS and Kafka. When to use each?**

> SQS is a managed message queue: messages are consumed once (deleted
> after receipt), no ordering guarantee in standard queues (FIFO queues
> add ordering), max retention 14 days, no consumer groups concept.
> Kafka is a distributed log: messages are retained for a configurable
> period (consumed by multiple consumer groups independently), ordered
> within partitions, supports replay. Use SQS for simple task queues
> (trigger Lambda, decouple microservices). Use Kafka when: multiple
> consumers need the same events, replay is needed, high throughput
> streaming analytics, or ML feature pipelines.

7.  **What is AWS Lambda and where does it fit in ML architectures?**

> Lambda is serverless compute --- executes code in response to events
> (S3 upload, API Gateway request, SQS message) without managing
> servers. In ML: use Lambda for lightweight preprocessing triggered on
> S3 data uploads, model result post-processing, scheduled feature
> computation, or API Gateway → Lambda → SageMaker inference proxy
> patterns. Limits: 15 min max execution, 10GB memory, 512MB--10GB
> ephemeral storage. Not suitable for heavy training or large model
> inference --- use EKS or SageMaker for those.

**Infrastructure as Code**

8.  **What is Terraform and how does it work?**

> Terraform is a declarative IaC tool: you describe desired
> infrastructure state in HCL files; Terraform computes a diff (plan)
> between desired and actual state and applies changes. Key concepts:
> providers (AWS, GCP plugins), resources (aws_eks_cluster,
> aws_s3_bucket), state file (tracks what Terraform manages --- store
> remotely in S3+DynamoDB for teams), modules (reusable infrastructure
> components). For ML: use Terraform to provision EKS clusters, GPU node
> groups, S3 buckets, and IAM roles reproducibly across dev/staging/prod
> environments.

**Networking**

9.  **Explain VPC, subnets, security groups, and NAT gateway in AWS.**

> VPC (Virtual Private Cloud): isolated network in AWS with a defined
> CIDR block. Subnets: subdivisions --- public subnets (Internet Gateway
> route) for load balancers, private subnets (no direct internet) for
> app/ML pods. Security Groups: stateful firewall at the instance/ENI
> level --- define inbound/outbound rules by port/protocol/CIDR. NACLs:
> stateless firewall at the subnet level. NAT Gateway: allows private
> subnet resources to initiate outbound internet connections (e.g.,
> download model weights) without being publicly reachable. For ML on
> EKS: run inference pods in private subnets behind an ALB in the public
> subnet.
