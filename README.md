# Developing and Deploying a Flask Web Application on AWS with Prometheus Monitoring

I developed an simple web application using flask framework and exposes endpoint at api/v1/hello
that responds to get requests
Prometheus metrics is imported from the prometheus flask_exporter module for metrics collection.
The responses include a simulated random delay and a 10% chance of returning an Internal Server Error response. Additionally, Prometheus metrics are configured to track various aspects of the application's HTTP requests and responses.

**AWS Deployment**
For deployment, I utilized AWS and Kubernetes:

![Image Alt Text](https://github.com/purna16/Jsp1/blob/main/images/Screenshot%20from%202023-09-01%2012-32-29.png)


**Virtual Private Cloud (VPC) Setup**

- Created a Virtual Private Cloud (VPC).
- Within the VPC, established two public subnets and two private subnets across different availability zones.

![Screenshot from 2023-09-01 11-59-41.png](https://github.com/purna16/Jsp1/blob/main/images/Screenshot%20from%202023-09-01%2011-59-41.png)

**Bastion Host and EC2 Instances**

- Deployed a bastion host in the public subnet.
- Set up two EC2 instances in the private subnets, configured without public IP addresses

**NAT Gateway**

Created a Network Address Translation (NAT) gateway to facilitate private instances in downloading packages from the internet.

**Load Balancer**
Attached a load balancer to the public subnet, routing traffic to both private instances using target groups.

![Screenshot from 2023-09-01 12-06-04.png](https://github.com/purna16/Jsp1/blob/main/images/Screenshot%20from%202023-09-01%2012-06-04.png)

**Kubernetes and Docker**

- Connected the private instances in the private subnet through the bastion host.
- Installed Kubernetes and Docker on these instances
- Time taken for VPC setup and tool installation: 1 hour

**Docker Image**

Created a Docker image for the web application and pushed it to DockerHub.
********

```jsx
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python", "worker_app.py"]
```

****Created a Kubernetes Deployment YAML file to deploy  worker pods.****

• Developed a Kubernetes Deployment YAML file to deploy worker pods.

• Time taken for Kubernetes deployment: 15 minutes.

```jsx
apiVersion: apps/v1
kind: Deployment
metadata:
  name: worker-deployment
spec:
  replicas: 2  
  selector:
    matchLabels:
      app: worker
  template:
    metadata:
      labels:
        app: worker
    spec:
      containers:
        - name: worker-app
          image: purna16/worker-app:latest
          ports:
            - containerPort: 5000
```

****Setting Up Prometheus Server****

• Utilized Helm charts to download and manage the Prometheus server.
• Configured Prometheus to use NodePort for access from a web browser.

• Installed Grafana to visualize data collected from Prometheus
********

```jsx
helm repo add Prometheus-community https://prometheus-community.github.io/helm-charts
helm install prometheus prometheus-community/kube-prometheus-stack
helm repo add grafana https://grafana.github.io/helm-charts
helm install grafana grafana/grafana
```

****Configured ServiceMonitor for Prometheus****

![Screenshot from 2023-09-01 12-27-29.png](https://github.com/purna16/Jsp1/blob/main/images/Screenshot%20from%202023-09-01%2012-27-29.png)

• Configured a ServiceMonitor for Prometheus to scrape metrics from the web application.

• This step is Important as Prometheus needs this configuration to collect metrics.

********

```jsx
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: worker-service-monitor
  labels:
    release: prometheus
    app: worker
spec:
  jobLabel: job
  selector:
    matchLabels:
      app: worker
  endpoints:
    - port: web
      path: /metrics
      interval: 15s  
  namespaceSelector:
    matchNames:
      - default
```

**Grafana dashboard after fetching metrics from prometheus datasource**

![Screenshot from 2023-09-01 14-06-03.png](https://github.com/purna16/Jsp1/blob/main/images/Screenshot%20from%202023-09-01%2014-06-03.png)

• Set up a Grafana dashboard to display various metrics related to the web application.
• Metrics include successful and failed requests, total requests, and request response times.

• Additional metrics cover CPU health, cluster health, memory usage, and disk utilization.

• Time taken for Grafana dashboard configuration: 1 day.

**SUMMARY**

In this project, I undertook the development and deployment of a Flask web application, coupled with the implementation of Prometheus monitoring, all hosted on Amazon Web Services (AWS) through Kubernetes.

**Web Application Development:**
I began by creating a simple web application using Flask, exposing an endpoint at **`/api/v1/hello`** to respond to HTTP GET requests. To enhance its robustness, I integrated Prometheus metrics, which provided invaluable insights into its performance.

**AWS Deployment:**
To deploy the application securely and efficiently on AWS, I embarked on a comprehensive setup process:

**Virtual Private Cloud (VPC):**
I established a Virtual Private Cloud (VPC). Within the VPC, I carefully designed two public subnets and two private subnets, ensuring that they spanned different availability zones to bolster fault tolerance and high availability.

**Bastion Host and EC2 Instances:**
For secure remote access to the private instances, I deployed a bastion host within the public subnet. Furthermore, I set up two EC2 instances in the private subnets, configuring them without public IP addresses to enhance security.

**NAT Gateway and Load Balancer:**
To facilitate these private instances in downloading essential packages from the internet, I judiciously established a Network Address Translation (NAT) gateway. Moreover, I attached a load balancer to the public subnet, enabling the efficient routing of incoming traffic to both private instances through defined target groups.

**Kubernetes and Docker:**
With the networking infrastructure in place, I connected the private instances through the bastion host. Subsequently, I installed Kubernetes and Docker on these instances.The entire process of setting up the VPC and installing the necessary tools consumed approximately 1 hour.

**Docker Image and Kubernetes Deployment:**
To encapsulate the application, I Created a Dockerfile and Created image and Pushed into DockerHub. This Docker image served as the foundation for deploying the application on Kubernetes, a process that I streamlined by crafting a Kubernetes Deployment YAML file. This deployment task was efficiently completed in just 15 minutes.

**Prometheus Server and Grafana Integration:**
With the application up and running. I leveraged Helm charts to procure and manage the Prometheus server. This robust monitoring tool was later configured to use a NodePort, enabling convenient access through web browsers. To visualize the rich data provided by Prometheus, I installed Grafana.

**ServiceMonitor Configuration:**
An essential part of the setup involved configuring a ServiceMonitor for Prometheus. This configuration step was important as it facilitated Prometheus in collecting the necessary metrics from the web application.

**Grafana Dashboard:**
Finally, I invested considerable effort into crafting a comprehensive Grafana dashboard. This dashboard was designed to present an array of metrics related to the web application, ranging from successful and failed requests to total requests and response times. Additional metrics encompassed crucial aspects such as CPU health, cluster health, memory utilization, and disk usage. This intricate dashboard configuration task spanned a day to ensure its completeness and effectiveness.

In summary, this project showcases a carefully orchestrated journey from web application development to its secure and robust deployment on AWS via Kubernetes using load balancer. The incorporation of Prometheus monitoring and Grafana visualization provided a robust foundation for monitoring and maintaining the application's performance and health.

In this project, I undertook the development and deployment of a Flask web application using load balancer, coupled with the implementation of Prometheus monitoring, all hosted on Amazon Web Services (AWS) through Kubernetes.
