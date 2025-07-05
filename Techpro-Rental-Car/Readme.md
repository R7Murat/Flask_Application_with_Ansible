# Automated Deployment of a Flask Application with Ansible (AWS EC2)

This project automates the installation and configuration of a Python Flask application, MySQL database, and NGINX reverse proxy as Docker containers on AWS EC2 instances using Ansible.

---

## 🔧 Ansible Control Node

| Property      | Value             |
| ------------- | ----------------- |
| Port          | 22                |
| Instance Type | `t3a.medium`      |
| AMI           | Amazon Linux 2023 |

- Central management node with Ansible installed.
- Configuration is handled from this node using Ansible.

---

## 🖥️ Application Server (Flask)

| Property      | Value                  |
| ------------- | ---------------------- |
| Ports         | 22 (SSH), 8000 (Flask) |
| Instance Type | `t2.micro`             |
| AMI           | Amazon Linux 2023      |

- The Python-based Flask application runs inside a Docker container.

---

## 📂 MySQL Database Server

| Property      | Value                  |
| ------------- | ---------------------- |
| Ports         | 22 (SSH), 3306 (MySQL) |
| Instance Type | `t2.micro`             |
| AMI           | Amazon Linux 2023      |

- A database named `araba_kiralama` is configured inside a Docker container.

---

## 🌐 NGINX Reverse Proxy

| Property      | Value               |
| ------------- | ------------------- |
| Ports         | 22 (SSH), 80 (HTTP) |
| Instance Type | `t2.micro`          |
| AMI           | Amazon Linux 2023   |

- NGINX acts as a reverse proxy, directing incoming HTTP requests to the Flask application.
- A custom domain (e.g., `techprodevops.com`) is pointed to this server using Route 53.

---

## 📁 Project File Structure

```
ansible-flask-aws/
├── ansible.cfg
├── inventory_aws_ec2.yml
├── playbook.yml
├── Techpro-Rental-Car/
│   └── nginx.conf
└── README.md
```

---

## ⚙️ Configuration Files

### `ansible.cfg`

```ini
[defaults]
host_key_checking = False
inventory = inventory_aws_ec2.yml
deprecation_warnings = False
interpreter_python = auto_silent
private_key_file = /home/ec2-user/xxxxxxx.pem # replace this
remote_user = ec2-user
```

### `inventory_aws_ec2.yml`

```yaml
plugin: aws_ec2
regions:
  - "us-east-1"
filters:
  tag:Stack: Ansible_Project
keyed_groups:
  - key: tags.Name
  - key: tags.Environment
compose:
  ansible_host: public_ip_address
```

---

## ▶️ Ansible Playbook Flow

### 1. **Install Docker (All Servers)**

- Install Docker, start the service, and configure user permissions (applied to all nodes in the \_prod group).

### 2. **Set Up MySQL Database (\_Ansible\_Db)**

- Remove any existing containers and images.
- Start a new `mysql:latest` container.
- Database credentials:
  - `DB: araba_kiralama`
  - `User: admin`
  - `Password: admin123`

### 3. **Deploy Flask Application (\_Ansible\_App)**

- Copy application files to `/home/ec2-user/app/`.
- Build the Docker image and run it as `techpro/app`.
- Start the container with environment variables:
  - `DB_HOST`: Public IP of the MySQL server
  - `PORT`: 8000

### 4. **Configure NGINX Reverse Proxy (\_Ansible\_Nginx)**

- Update `nginx.conf` template using `envsubst` to include the public IP.
- Start the NGINX container as a reverse proxy for the Flask app.

---

## 🚀 Deployment Steps

1. **Manually Launch EC2 Instances on AWS**

   - Add appropriate tags to each instance:
     - `Stack: Ansible_Project`
     - `Name: _Ansible_App`, `_Ansible_Db`, `_Ansible_Nginx`, etc.

2. **Prepare Required Files on the Ansible Control Node**

   - Include `ansible.cfg`, `inventory_aws_ec2.yml`, `playbook.yml`, and application source code

3. **Run the Playbook**

```bash
ansible-playbook playbook.yml
```

---

## 🧪 Testing

1. Navigate to `http://<domain_name>` in your browser.
2. If the homepage is displayed, the entire setup is working properly.
3. You can check EC2, Docker, and Ansible logs to troubleshoot any issues.

---

## ✅ Requirements

- Ansible 2.14+
- AWS EC2 IAM permissions
- Python 3.x
- Boto3 and Ansible AWS plugins
- `community.docker` collection must be installed:

```bash
ansible-galaxy collection install community.docker
```

---

## 📌 Notes

- EC2 instances were created manually via the AWS Management Console.
- Auto-scaling, high availability, or CI/CD is **not** included in this project scope.
- For security, credentials and secrets should be encrypted or managed using Vault.

---

## 📜 License

This project is intended for educational and demo purposes. Review security and scalability aspects before using it in a production environment.

