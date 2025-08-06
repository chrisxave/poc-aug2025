# PoC: FastAPI with PostgreSQL on OpenShift

This Proof of Concept demonstrates how to deploy a **FastAPI** application that connects to a **PostgreSQL** database on **OpenShift**, using the **CloudNativePG Operator** to provision the database instance.

---

## 📌 Prerequisites

1. A running **OpenShift cluster**.
2. **CloudNativePG Operator** must be installed:
   - Go to **OperatorHub** in OpenShift Web Console.
   - Search for **CloudNativePG**.
   - Click **Install** (either cluster-wide or namespace-specific).
3. A working **StorageClass** (e.g., `ocs-external-storagecluster-ceph-rbd`).
4. Your OpenShift cluster can access this GitHub repository (public or with credentials configured).
