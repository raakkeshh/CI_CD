import os
from datetime import datetime
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

# Enterprise CI/CD State Simulation (in-memory for demo, non-blocking)
PIPELINE_STATE = {
    "current_build_id": "cb-94821-prod",
    "gate_status": "Waiting for Manager Approval",
    "deployment_status": "Pending Approval",
    "approved_by": None,
    "approval_timestamp": None,
    "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC"),
    "target_env": "Production",
    "image_tag": "us-central1-docker.pkg.dev/cloudbuild-pro-prod/apps/web-app:v2.4.1",
    "commit_hash": "7f9b2a1",
    "branch": "main",
    "author": "Alex Chen (Lead DevOps)",
    "commit_msg": "feat(security): implement strict manual approval gate before Cloud Run prod rollout"
}

# 15+ Comprehensive Sample Build History Records
SAMPLE_BUILDS = [
    {
        "id": "cb-94821-prod",
        "commit": "7f9b2a1",
        "commit_msg": "feat(security): implement strict manual approval gate before Cloud Run prod rollout",
        "developer": "Alex Chen",
        "developer_email": "alex.chen@enterprise.gcp",
        "status": "Running",
        "duration": "2m 45s",
        "date": "2026-10-10 09:42 AM",
        "environment": "Production",
        "branch": "main",
        "approval_required": True,
        "logs": [
            "[09:42:01] Step 0: Starting Git checkout revision 7f9b2a1",
            "[09:42:15] Step 1: Running unit tests & flake8 linting (100% passed)",
            "[09:42:48] Step 2: Building multi-stage Docker image with Kaniko cache",
            "[09:43:20] Step 3: Pushing artifact to us-central1-docker.pkg.dev/cloudbuild-pro-prod/apps/web-app:v2.4.1",
            "[09:43:55] Step 4: Vulnerability scanning completed: 0 Critical, 0 High CVEs",
            "[09:44:10] Step 5: [APPROVAL_GATE] Paused waiting for approval from Cloud Build Approvers IAM group..."
        ]
    },
    {
        "id": "cb-94820-stg",
        "commit": "3d8c119",
        "commit_msg": "chore(deps): bump gunicorn to 21.2.0 and optimize python slim base",
        "developer": "Priya Sharma",
        "developer_email": "priya.s@enterprise.gcp",
        "status": "Success",
        "duration": "2m 14s",
        "date": "2026-10-10 08:30 AM",
        "environment": "Staging",
        "branch": "staging",
        "approval_required": False,
        "logs": [
            "[08:30:02] Checkout revision 3d8c119",
            "[08:30:45] Docker multi-stage build completed in 43s (cache hit 88%)",
            "[08:31:30] Vulnerability scan: clean",
            "[08:32:16] Cloud Run deployed revision cloudbuild-pro-stg-00041 (100% traffic routed)"
        ]
    },
    {
        "id": "cb-94819-dev",
        "commit": "e4a7092",
        "commit_msg": "feat(dashboard): add circular progress gauge for pipeline health metrics",
        "developer": "David Miller",
        "developer_email": "david.m@enterprise.gcp",
        "status": "Success",
        "duration": "1m 58s",
        "date": "2026-10-10 07:15 AM",
        "environment": "Development",
        "branch": "feat/circular-gauge",
        "approval_required": False,
        "logs": [
            "[07:15:01] Automated trigger on branch feat/circular-gauge",
            "[07:16:10] Container image tagged with git SHA e4a7092",
            "[07:16:59] Cloud Run dev instance updated successfully"
        ]
    },
    {
        "id": "cb-94818-prod",
        "commit": "9b12f67",
        "commit_msg": "fix(config): adjust autoscaling min-instances to 2 to eliminate cold starts",
        "developer": "Elena Rostova",
        "developer_email": "elena.r@enterprise.gcp",
        "status": "Success",
        "duration": "3m 05s",
        "date": "2026-10-09 11:45 PM",
        "environment": "Production",
        "branch": "main",
        "approval_required": True,
        "logs": [
            "[23:45:00] Triggered by production release tag v2.4.0",
            "[23:46:12] Approval Gate granted by Director of Infrastructure (elena.r@enterprise.gcp)",
            "[23:48:05] Production revision deployed: 100% green traffic healthy"
        ]
    },
    {
        "id": "cb-94817-stg",
        "commit": "5a22de1",
        "commit_msg": "refactor(api): streamline JSON endpoints for build status telemetry",
        "developer": "Marcus Brody",
        "developer_email": "marcus.b@enterprise.gcp",
        "status": "Success",
        "duration": "2m 02s",
        "date": "2026-10-09 06:12 PM",
        "environment": "Staging",
        "branch": "staging",
        "approval_required": False,
        "logs": [
            "[18:12:00] Staging pipeline execution",
            "[18:13:30] Tests: 42 passed in 1.4s",
            "[18:14:02] Staging revision healthy"
        ]
    },
    {
        "id": "cb-94816-dev",
        "commit": "1c88bb3",
        "commit_msg": "test(unit): add regression suite for approval state machine transitions",
        "developer": "Priya Sharma",
        "developer_email": "priya.s@enterprise.gcp",
        "status": "Success",
        "duration": "1m 45s",
        "date": "2026-10-09 03:22 PM",
        "environment": "Development",
        "branch": "test/approval-state",
        "approval_required": False,
        "logs": [
            "[15:22:00] Run unit tests with pytest",
            "[15:23:15] Code coverage: 96.4%",
            "[15:23:45] Fast-build completed"
        ]
    },
    {
        "id": "cb-94815-prod",
        "commit": "80ff43a",
        "commit_msg": "feat(secrets): integrate Secret Manager for encrypted runtime environment variables",
        "developer": "Alex Chen",
        "developer_email": "alex.chen@enterprise.gcp",
        "status": "Cancelled",
        "duration": "1m 10s",
        "date": "2026-10-09 01:05 PM",
        "environment": "Production",
        "branch": "main",
        "approval_required": True,
        "logs": [
            "[13:05:00] Build queued for production",
            "[13:05:45] Approval Gate: Pending approval",
            "[13:06:10] Build cancelled by user (Alex Chen) - requested re-review of IAM roles"
        ]
    },
    {
        "id": "cb-94814-stg",
        "commit": "21e4a99",
        "commit_msg": "fix(docker): resolve base image vulnerability in OpenSSL library",
        "developer": "David Miller",
        "developer_email": "david.m@enterprise.gcp",
        "status": "Success",
        "duration": "2m 30s",
        "date": "2026-10-09 10:40 AM",
        "environment": "Staging",
        "branch": "hotfix/openssl-patch",
        "approval_required": False,
        "logs": [
            "[10:40:00] Container security scan trigger",
            "[10:41:20] OpenSSL patch validated: 0 vulnerable packages found",
            "[10:42:30] Deployed to staging verification environment"
        ]
    },
    {
        "id": "cb-94813-dev",
        "commit": "4f18c20",
        "commit_msg": "wip(ui): initial wireframes for Cloud Build architecture breakdown card",
        "developer": "Marcus Brody",
        "developer_email": "marcus.b@enterprise.gcp",
        "status": "Failed",
        "duration": "0m 52s",
        "date": "2026-10-09 08:15 AM",
        "environment": "Development",
        "branch": "wip/ui-cards",
        "approval_required": False,
        "logs": [
            "[08:15:00] Running npm linter and syntax checks",
            "[08:15:42] ERROR: Missing closing tag in template component at line 142",
            "[08:15:52] Build failed with exit code 1"
        ]
    },
    {
        "id": "cb-94812-prod",
        "commit": "7a35e88",
        "commit_msg": "release: CloudBuild Pro v2.3.9 with enhanced Cloud Monitoring dashboards",
        "developer": "Elena Rostova",
        "developer_email": "elena.r@enterprise.gcp",
        "status": "Success",
        "duration": "3m 18s",
        "date": "2026-10-08 05:50 PM",
        "environment": "Production",
        "branch": "release/v2.3",
        "approval_required": True,
        "logs": [
            "[17:50:00] Release tag v2.3.9 detected",
            "[17:51:30] Approval Gate: Approved by VP of Engineering",
            "[17:53:18] Production deployment complete. Traffic shifted to 100% on new revision"
        ]
    },
    {
        "id": "cb-94811-stg",
        "commit": "90d12e4",
        "commit_msg": "perf(assets): enable brotli compression and cache-control headers on static files",
        "developer": "Alex Chen",
        "developer_email": "alex.chen@enterprise.gcp",
        "status": "Success",
        "duration": "2m 11s",
        "date": "2026-10-08 02:15 PM",
        "environment": "Staging",
        "branch": "staging",
        "approval_required": False,
        "logs": [
            "[14:15:00] Asset optimization build step",
            "[14:16:30] Lighthouse score: Performance 99, Best Practices 100",
            "[14:17:11] Staging release verified"
        ]
    },
    {
        "id": "cb-94810-dev",
        "commit": "6e319bf",
        "commit_msg": "docs(readme): add detailed enterprise approval gate architecture diagrams",
        "developer": "Priya Sharma",
        "developer_email": "priya.s@enterprise.gcp",
        "status": "Success",
        "duration": "1m 32s",
        "date": "2026-10-08 11:30 AM",
        "environment": "Development",
        "branch": "docs/architecture-update",
        "approval_required": False,
        "logs": [
            "[11:30:00] Markdown lint and documentation checks",
            "[11:31:00] Validation clean",
            "[11:31:32] Preview documentation deployment created"
        ]
    },
    {
        "id": "cb-94809-prod",
        "commit": "55b89a1",
        "commit_msg": "feat(iam): enforce Principle of Least Privilege on Cloud Build service account",
        "developer": "Elena Rostova",
        "developer_email": "elena.r@enterprise.gcp",
        "status": "Success",
        "duration": "2m 55s",
        "date": "2026-10-07 04:45 PM",
        "environment": "Production",
        "branch": "main",
        "approval_required": True,
        "logs": [
            "[16:45:00] Production security compliance build",
            "[16:46:20] Approval Gate: Approved by Security Officer (elena.r@enterprise.gcp)",
            "[16:47:55] Production rollout verified across all regions"
        ]
    },
    {
        "id": "cb-94808-stg",
        "commit": "38aa410",
        "commit_msg": "test(load): simulate 10,000 req/sec load test on Cloud Run service revision",
        "developer": "David Miller",
        "developer_email": "david.m@enterprise.gcp",
        "status": "Success",
        "duration": "4m 20s",
        "date": "2026-10-07 01:10 PM",
        "environment": "Staging",
        "branch": "load-test/10k-qps",
        "approval_required": False,
        "logs": [
            "[13:10:00] Locust load testing container started",
            "[13:13:30] Peak latency: 42ms p99 at 10,200 QPS",
            "[13:14:20] Load test passed with zero 5xx errors"
        ]
    },
    {
        "id": "cb-94807-dev",
        "commit": "1198fbc",
        "commit_msg": "fix(routes): correct 404 handler redirection on undefined API endpoints",
        "developer": "Marcus Brody",
        "developer_email": "marcus.b@enterprise.gcp",
        "status": "Success",
        "duration": "1m 40s",
        "date": "2026-10-07 09:20 AM",
        "environment": "Development",
        "branch": "fix/api-404",
        "approval_required": False,
        "logs": [
            "[09:20:00] Run test suite",
            "[09:21:00] All unit tests passing",
            "[09:21:40] Deployed to dev sandbox"
        ]
    },
    {
        "id": "cb-94806-prod",
        "commit": "890ef14",
        "commit_msg": "feat(telemetry): add OpenTelemetry tracing spans to pipeline gate handler",
        "developer": "Alex Chen",
        "developer_email": "alex.chen@enterprise.gcp",
        "status": "Success",
        "duration": "3m 10s",
        "date": "2026-10-06 03:40 PM",
        "environment": "Production",
        "branch": "main",
        "approval_required": True,
        "logs": [
            "[15:40:00] Triggered production build",
            "[15:41:40] Approval Gate: Approved by alex.chen@enterprise.gcp",
            "[15:43:10] Tracing enabled on production Cloud Run revision"
        ]
    }
]

# Shared Global Project Context
PROJECT_CONTEXT = {
    "project_name": "CloudBuild Pro – CI/CD Pipeline with Approval Gates",
    "gcp_project_id": "gcp-cloudbuild-pro-prod",
    "region": "us-central1 (Iowa)",
    "repository": "GoogleCloudPlatform/cloudbuild-pro",
    "branch": "main",
    "commit_hash": "7f9b2a1",
    "commit_message": "feat(security): implement strict manual approval gate before Cloud Run prod rollout",
    "author": "Alex Chen (Staff DevOps Architect)",
    "cloud_build_status": "WAITING_APPROVAL",
    "build_duration": "2m 45s",
    "worker_pool": "private-worker-pool-uscentral1 (e2-highcpu-8)",
    "artifact_registry_repo": "us-central1-docker.pkg.dev/cloudbuild-pro-prod/apps/web-app",
    "artifact_tag": "v2.4.1 (sha-7f9b2a1)",
    "artifact_size": "58.4 MB",
    "vulnerabilities": "0 Critical • 0 High • 2 Low",
    "approval_gate": {
        "status": "Waiting for Manager Approval",
        "required_role": "roles/cloudbuild.approver",
        "approvers": ["devops-lead@enterprise.gcp", "release-manager@enterprise.gcp"],
        "pending_since": "4 minutes ago",
        "environment": "Production"
    },
    "cloud_run": {
        "service_name": "cloudbuild-pro-web",
        "revision": "cloudbuild-pro-web-00042-prod",
        "active_instances": "3 / 10",
        "traffic_allocation": "100%",
        "url": "https://cloudbuild-pro-web-uc.a.run.app",
        "health": "HEALTHY (100%)",
        "latency": "38ms (p99)"
    },
    "environments": ["Development", "Staging", "Production"],
    "current_environment": "Production",
    "widgets": {
        "latest_build": "cb-94821-prod",
        "today_deployments": 14,
        "approval_requests": 1,
        "failed_builds": 1,
        "avg_build_time": "2m 18s",
        "total_repositories": 8,
        "success_rate": "98.6%"
    }
}

# 9 Detailed Pipeline Stages Specification
PIPELINE_STAGES = [
    {
        "id": 1,
        "name": "GitHub",
        "icon": "fa-brands fa-github",
        "color": "#6e5494",
        "status": "COMPLETED",
        "duration": "4s",
        "desc": "Git push webhook received on branch main. Commit SHA 7f9b2a1 verified with GPG signature.",
        "gcp_service": "GitHub Enterprise / Cloud Build GitHub App",
        "details": {
            "Trigger Type": "Push to main branch",
            "Commit": "7f9b2a1",
            "Author": "Alex Chen <alex.chen@enterprise.gcp>",
            "Payload Size": "18.4 KB",
            "Webhook Latency": "180ms"
        }
    },
    {
        "id": 2,
        "name": "Cloud Build Trigger",
        "icon": "fa-solid fa-bolt",
        "color": "#4285F4",
        "status": "COMPLETED",
        "duration": "8s",
        "desc": "Cloud Build Trigger activated via Cloud Pub/Sub. High-concurrency worker allocated in us-central1.",
        "gcp_service": "Google Cloud Build (Triggers)",
        "details": {
            "Trigger ID": "tr-77a8-prod-pipeline",
            "Worker Pool": "private-worker-pool-uscentral1",
            "Machine Type": "e2-highcpu-8 (8 vCPU, 8 GB RAM)",
            "Logging": "Google Cloud Logging (Direct Stream)",
            "Timeout": "1200s"
        }
    },
    {
        "id": 3,
        "name": "Unit Testing",
        "icon": "fa-solid fa-vial-circle-check",
        "color": "#34A853",
        "status": "COMPLETED",
        "duration": "35s",
        "desc": "Automated Python test suite and flake8 linter executed. 100% test pass rate with 96.4% code coverage.",
        "gcp_service": "Cloud Build Test Runner",
        "details": {
            "Test Framework": "pytest v8.1 + flake8",
            "Tests Passed": "42 / 42 (100%)",
            "Code Coverage": "96.4%",
            "Linting Violations": "0 warnings, 0 errors",
            "Execution Time": "35.2s"
        }
    },
    {
        "id": 4,
        "name": "Docker Build",
        "icon": "fa-brands fa-docker",
        "color": "#0db7ed",
        "status": "COMPLETED",
        "duration": "48s",
        "desc": "Multi-stage Dockerfile built with Kaniko layer caching. Optimized Python 3.11-slim runtime container created.",
        "gcp_service": "Google Cloud Build (Kaniko Engine)",
        "details": {
            "Base Image": "python:3.11-slim",
            "Build Engine": "Kaniko with Layer Caching",
            "Layer Cache Hit Rate": "85.7%",
            "Image Size": "58.4 MB (compressed)",
            "Security Flags": "Non-root user (appuser:1000)"
        }
    },
    {
        "id": 5,
        "name": "Artifact Registry",
        "icon": "fa-solid fa-cubes",
        "color": "#4285F4",
        "status": "COMPLETED",
        "duration": "22s",
        "desc": "OCI container image securely pushed and signed to Google Cloud Artifact Registry repository.",
        "gcp_service": "Google Cloud Artifact Registry",
        "details": {
            "Registry URI": "us-central1-docker.pkg.dev/cloudbuild-pro-prod/apps/web-app",
            "Tags": "v2.4.1, sha-7f9b2a1, latest",
            "Storage Location": "us-central1 (Regional standard)",
            "Encryption": "Google-managed encryption key (CMEK ready)",
            "Digest": "sha256:7f14b39a8c224e7512d90899ab4d129841f"
        }
    },
    {
        "id": 6,
        "name": "Security Scan",
        "icon": "fa-solid fa-shield-halved",
        "color": "#34A853",
        "status": "COMPLETED",
        "duration": "26s",
        "desc": "Container Analysis scanned OCI layers for CVE vulnerabilities. Compliance gate passed with zero Critical CVEs.",
        "gcp_service": "Google Container Analysis & Artifact Analysis",
        "details": {
            "Scanner Engine": "GCP Container Analysis API v1",
            "Critical CVEs": "0",
            "High CVEs": "0",
            "Medium CVEs": "0",
            "Low CVEs": "2 (Inconsequential base libc)",
            "Binary Authorization": "Attestation signed by security-bot@gcp"
        }
    },
    {
        "id": 7,
        "name": "Manual Approval Gate",
        "icon": "fa-solid fa-user-shield",
        "color": "#FBBC05",
        "status": "WAITING_APPROVAL",
        "duration": "Active",
        "desc": "Enterprise governance gate. Production deployment requires explicit manager authorization before proceeding.",
        "gcp_service": "Cloud Build Approval Gates & IAM",
        "details": {
            "Required IAM Role": "roles/cloudbuild.approver",
            "Approved Status": "Waiting for Manager Approval",
            "Target Environment": "Production (us-central1)",
            "Approval Policy": "Strict 1-of-N Approval Required",
            "Audit Logging": "Cloud Audit Logs (Admin Activity enabled)"
        }
    },
    {
        "id": 8,
        "name": "Cloud Run Deployment",
        "icon": "fa-solid fa-cloud-arrow-up",
        "color": "#4285F4",
        "status": "PENDING",
        "duration": "--",
        "desc": "Serverless container rollout with blue/green zero-downtime revision traffic migration and health checking.",
        "gcp_service": "Google Cloud Run (Fully Managed)",
        "details": {
            "Service Name": "cloudbuild-pro-web",
            "Target Revision": "cloudbuild-pro-web-00042-prod",
            "CPU / Memory": "2 vCPU / 2 GiB",
            "Scaling": "Min: 2, Max: 10 instances",
            "Traffic Strategy": "Canary verification (0% -> 100%)"
        }
    },
    {
        "id": 9,
        "name": "Application Live",
        "icon": "fa-solid fa-globe",
        "color": "#34A853",
        "status": "PENDING",
        "duration": "--",
        "desc": "Production revision serving 100% live traffic through Global HTTPS Load Balancing with Cloud CDN edge caching.",
        "gcp_service": "Cloud Run & Cloud Load Balancing",
        "details": {
            "Live URL": "https://cloudbuild-pro-web-uc.a.run.app",
            "SSL Status": "Google-managed HTTPS Certificate Active",
            "Health Check": "HTTP 200 OK (/api/health)",
            "CDN Caching": "Cloud CDN enabled for static assets",
            "SLA Target": "99.99% Uptime Guarantee"
        }
    }
]

# Architecture Components Explanation
ARCHITECTURE_COMPONENTS = [
    {
        "name": "GitHub Enterprise / Cloud Source Repositories",
        "icon": "fa-brands fa-github",
        "color": "#6e5494",
        "tag": "Source Control & Event Source",
        "summary": "Houses code repositories and emits cryptographically signed webhook push and pull request events to Google Cloud.",
        "role": "Developers commit code to feature branches and open pull requests. Merges into main or release tags automatically trigger Google Cloud Build webhooks.",
        "best_practice": "Enforce branch protection rules, require signed commits (GPG), and mandate unit test status checks before merge."
    },
    {
        "name": "Google Cloud Build",
        "icon": "fa-solid fa-screwdriver-wrench",
        "color": "#4285F4",
        "tag": "Serverless CI/CD Orchestration",
        "summary": "Fully managed, scalable serverless build platform that executes containerized pipeline steps with private worker pools.",
        "role": "Receives GitHub webhooks, provisions isolated build compute, checks out code, runs linting/tests, builds Docker images, and coordinates approvals.",
        "best_practice": "Use private worker pools inside VPC for internal VPC peering, enable Cloud Build caching, and apply custom service accounts with least privilege IAM."
    },
    {
        "name": "Docker & Kaniko Build Engine",
        "icon": "fa-brands fa-docker",
        "color": "#0db7ed",
        "tag": "Container Standardization",
        "summary": "Multi-stage container packaging tool that builds OCI-compliant container images safely without requiring privileged daemon access.",
        "role": "Packages the Flask application, installs pinned dependencies, strips build toolchains, and sets up non-root runtime users.",
        "best_practice": "Leverage python:3.11-slim base images, clean package caches, use .dockerignore, and isolate runtime user UID 1000."
    },
    {
        "name": "Google Artifact Registry",
        "icon": "fa-solid fa-cubes",
        "color": "#34A853",
        "tag": "Enterprise OCI Artifact Storage",
        "summary": "Next-generation universal package manager for OCI container images, Helm charts, and language packages.",
        "role": "Securely stores built container images tagged with semantic versions and git commit hashes. Automatically runs vulnerability scans on every upload.",
        "best_practice": "Implement artifact cleanup policies to manage storage costs, use regional repositories close to compute, and enforce CMEK encryption."
    },
    {
        "name": "Manual Approval Gate",
        "icon": "fa-solid fa-user-shield",
        "color": "#FBBC05",
        "tag": "Governance & Compliance Gate",
        "summary": "Enterprise human-in-the-loop authorization step that pauses production deployments until certified managers sign off.",
        "role": "Halts the automated pipeline after testing and scanning succeed. Sends Cloud Pub/Sub and email/Slack notifications to authorized DevOps managers to approve or reject.",
        "best_practice": "Enforce strict IAM roles (roles/cloudbuild.approver), log all approvals to Cloud Audit Logs for SOC2/HIPAA compliance, and set automatic expiration timers."
    },
    {
        "name": "Google Cloud Run",
        "icon": "fa-solid fa-cloud-arrow-up",
        "color": "#4285F4",
        "tag": "Serverless Container Execution",
        "summary": "Fully managed serverless compute platform that runs containers directly on top of Google's hardened infrastructure.",
        "role": "Instantiates container revisions, automatically scales from 0 to 1,000s of instances based on traffic, and performs traffic splitting for blue/green rollouts.",
        "best_practice": "Configure min-instances to prevent cold starts, set concurrency limits tuned to application memory, and assign dedicated service accounts."
    },
    {
        "name": "End Users & Global Cloud Load Balancer",
        "icon": "fa-solid fa-globe",
        "color": "#34A853",
        "tag": "Edge Delivery & Zero Downtime",
        "summary": "Worldwide Google Anycast IP network with Cloud Armor DDoS protection, SSL termination, and Cloud CDN edge caching.",
        "role": "Routes incoming user requests to the closest healthy Cloud Run region with single-digit millisecond latency.",
        "best_practice": "Attach Cloud Armor WAF security policies, enable HTTP/3, and route static assets through Cloud CDN."
    }
]

# Flask Context Processor to inject global telemetry into all templates
@app.context_processor
def inject_global_context():
    return {
        "ctx": PROJECT_CONTEXT,
        "state": PIPELINE_STATE
    }

# Flask Routes
@app.route("/")
def dashboard():
    return render_template(
        "dashboard.html",
        ctx=PROJECT_CONTEXT,
        state=PIPELINE_STATE,
        builds=SAMPLE_BUILDS[:5],
        stages=PIPELINE_STAGES,
        active_page="dashboard"
    )

@app.route("/pipeline")
def pipeline():
    return render_template(
        "pipeline.html",
        ctx=PROJECT_CONTEXT,
        state=PIPELINE_STATE,
        stages=PIPELINE_STAGES,
        active_page="pipeline"
    )

@app.route("/history")
def history():
    return render_template(
        "history.html",
        ctx=PROJECT_CONTEXT,
        builds=SAMPLE_BUILDS,
        active_page="history"
    )

@app.route("/architecture")
def architecture():
    return render_template(
        "architecture.html",
        ctx=PROJECT_CONTEXT,
        components=ARCHITECTURE_COMPONENTS,
        active_page="architecture"
    )

@app.route("/about")
def about():
    return render_template(
        "about.html",
        ctx=PROJECT_CONTEXT,
        active_page="about"
    )

# REST API Endpoints
@app.route("/api/health")
def api_health():
    return jsonify({
        "status": "HEALTHY",
        "service": "CloudBuild Pro",
        "version": "v2.4.1",
        "timestamp": datetime.now().isoformat(),
        "region": "us-central1",
        "revision": "cloudbuild-pro-web-00042-prod"
    })

@app.route("/api/pipeline/status")
def api_pipeline_status():
    return jsonify(PIPELINE_STATE)

@app.route("/api/pipeline/approve", methods=["POST"])
def api_pipeline_approve():
    PIPELINE_STATE["gate_status"] = "Approved"
    PIPELINE_STATE["deployment_status"] = "Deployment Completed"
    PIPELINE_STATE["approved_by"] = "devops-manager@enterprise.gcp"
    PIPELINE_STATE["approval_timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")
    PIPELINE_STATE["last_updated"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")
    
    # Update stage status in memory
    for stage in PIPELINE_STAGES:
        if stage["id"] in [7, 8, 9]:
            stage["status"] = "COMPLETED"

    # Also update the latest running build in history to Success
    for b in SAMPLE_BUILDS:
        if b["id"] == PIPELINE_STATE["current_build_id"]:
            b["status"] = "Success"
            b["duration"] = "3m 12s"
            b["logs"].append(f"[{datetime.now().strftime('%H:%M:%S')}] Approval granted by devops-manager@enterprise.gcp")
            b["logs"].append(f"[{datetime.now().strftime('%H:%M:%S')}] Cloud Run deployment completed: 100% traffic live")

    return jsonify({
        "success": True,
        "gate_status": PIPELINE_STATE["gate_status"],
        "deployment_status": PIPELINE_STATE["deployment_status"],
        "message": "Approval Gate passed! Deployment initiated and completed successfully.",
        "state": PIPELINE_STATE
    })

@app.route("/api/pipeline/reject", methods=["POST"])
def api_pipeline_reject():
    PIPELINE_STATE["gate_status"] = "Rejected"
    PIPELINE_STATE["deployment_status"] = "Deployment Cancelled"
    PIPELINE_STATE["approved_by"] = "release-officer@enterprise.gcp (REJECTED)"
    PIPELINE_STATE["approval_timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")
    PIPELINE_STATE["last_updated"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")
    
    for stage in PIPELINE_STAGES:
        if stage["id"] == 7:
            stage["status"] = "REJECTED"
        elif stage["id"] in [8, 9]:
            stage["status"] = "CANCELLED"

    for b in SAMPLE_BUILDS:
        if b["id"] == PIPELINE_STATE["current_build_id"]:
            b["status"] = "Cancelled"
            b["logs"].append(f"[{datetime.now().strftime('%H:%M:%S')}] Deployment rejected by release-officer@enterprise.gcp")
            b["logs"].append(f"[{datetime.now().strftime('%H:%M:%S')}] Pipeline halted. Production roll-back safety verified.")

    return jsonify({
        "success": True,
        "gate_status": PIPELINE_STATE["gate_status"],
        "deployment_status": PIPELINE_STATE["deployment_status"],
        "message": "Deployment rejected. Rollout safely cancelled.",
        "state": PIPELINE_STATE
    })

@app.route("/api/pipeline/trigger", methods=["POST"])
def api_pipeline_trigger():
    new_id = f"cb-{int(datetime.now().timestamp()) % 100000}-prod"
    PIPELINE_STATE["current_build_id"] = new_id
    PIPELINE_STATE["gate_status"] = "Waiting for Manager Approval"
    PIPELINE_STATE["deployment_status"] = "Pending Approval"
    PIPELINE_STATE["approved_by"] = None
    PIPELINE_STATE["approval_timestamp"] = None
    PIPELINE_STATE["last_updated"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")

    for stage in PIPELINE_STAGES:
        if stage["id"] <= 6:
            stage["status"] = "COMPLETED"
        elif stage["id"] == 7:
            stage["status"] = "WAITING_APPROVAL"
        else:
            stage["status"] = "PENDING"

    return jsonify({
        "success": True,
        "message": f"New Cloud Build pipeline {new_id} triggered successfully!",
        "state": PIPELINE_STATE
    })

@app.route("/api/builds")
def api_builds():
    env_filter = request.args.get("env")
    status_filter = request.args.get("status")
    search_query = request.args.get("search", "").lower()

    filtered = SAMPLE_BUILDS
    if env_filter and env_filter.lower() != "all":
        filtered = [b for b in filtered if b["environment"].lower() == env_filter.lower()]
    if status_filter and status_filter.lower() != "all":
        filtered = [b for b in filtered if b["status"].lower() == status_filter.lower()]
    if search_query:
        filtered = [
            b for b in filtered
            if search_query in b["id"].lower()
            or search_query in b["commit"].lower()
            or search_query in b["commit_msg"].lower()
            or search_query in b["developer"].lower()
        ]

    return jsonify({
        "total": len(filtered),
        "builds": filtered
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=True)