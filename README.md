# ☁️ AWS Core Services in Action: A Hands-on Demo 

This project is your gateway to understanding and experiencing the core services that power the AWS cloud. Whether you're an absolute beginner or looking for a refresher, this hands-on demonstration will guide you through essential concepts and workflows.

**What you'll learn:**

* How to launch and manage an **EC2** instance, your virtual server in the cloud.
* Efficiently store and retrieve files using **S3**, Amazon's scalable storage solution.
* Organize file information using an **RDS** database, ensuring data persistence and easy access.
* Make your application accessible to the world with a custom domain name using **Route 53**.

## The Project: A File Upload and Download Application

This project showcases the following AWS services in action:

* **EC2 (Elastic Compute Cloud):**  The virtual server where our application runs. Think of it as a remote computer you can access and control.
* **S3 (Simple Storage Service):** A scalable storage solution for the cloud. We'll use it to store the files uploaded by users.
* **RDS (Relational Database Service):** A managed database service. We'll utilize it to store metadata about uploaded files (like filename, size, upload date).
* **Route 53:** AWS's DNS (Domain Name System) service. It'll allow us to map a custom domain name to our EC2 instance, making the application accessible via a friendly URL.

## Setting Up the Project

### Prerequisites

* **An AWS Account:** You'll need an active AWS account to create and manage the necessary resources.
* **Basic Linux Command Line Knowledge:** You'll be working on a Linux-based EC2 instance, so familiarity with basic commands is helpful.
* **A Text Editor or IDE:** Any text editor or IDE will do for working with the code files.

### Step-by-Step Guide

1. **Launch an EC2 Instance:**
    * In the AWS Management Console, navigate to the EC2 service.
    * Click on "Launch Instance."
    * Choose an ** **Ubuntu Server** **.
    * Select an instance type. For this demo, a `t2.micro` instance should suffice.
    * Configure the instance details:
        * **Network:** Choose your default VPC.
        * **Security Groups:** Create a new security group or use an existing one. Ensure it allows inbound traffic on ports 22 (SSH), 80 (HTTP), and 443 (HTTPS).
        * **Key Pair (Optional):** Create a new key pair or select an existing one if you want to connect to the instance via SSH.
    * Click "Launch Instance."
    * <img width="1139" alt="Screenshot 2024-09-05 at 7 36 40 PM" src="https://github.com/user-attachments/assets/be67ed5f-3c43-4fc3-b5f8-3635c68aa3b8">


2. **Connect to your EC2 Instance:**
    * If you used a key pair:
        ```bash
        ssh -i <your-key-pair.pem> ec2-user@<your-ec2-public-ip>
        ```
    * If you're using EC2 Instance Connect:
        * Open the EC2 console, select your instance, and click "Connect."

3. **Update the Instance:**

    ```bash
    sudo apt update && sudo apt upgrade -y
    ```
    This ensures your instance has the latest software packages.

4. **Install Python and Required Tools:**

    ```bash
    sudo apt install python3 python3-venv git mysql-client -y
    ```
    * `python3`: The programming language we'll use.
    * `python3-venv`: Creates isolated virtual environments for Python projects.
    * `git`: For version control and cloning the project repository.
    * `mysql-client`: To interact with the RDS database from the command line.

5. **Create and Activate a Virtual Environment:**

    ```bash
    python3 -m venv aws-demo-env
    source aws-demo-env/bin/activate
    ```
    Virtual environments help keep project dependencies organized and avoid conflicts.

6. **Clone the Project Repository:**

    ```bash
    git clone [https://github.com/](https://github.com/)<your-username>/aws-demo.git
    cd aws-demo
    ```
    This downloads the project files to your EC2 instance.

7. **Install Project Dependencies:**

    ```bash
    pip install -r requirements.txt
    ```
    This installs the necessary Python libraries listed in the `requirements.txt` file.

8. **Set Up AWS Resources:**

    * **S3 Bucket:**
        * In the AWS console, navigate to the S3 service.
        * Click "Create bucket."
        * Choose a unique name for your bucket and select a region.
        * Keep the default settings for now.
        * Create the bucket.
    * **RDS Instance (MySQL):**
        * In the AWS console, navigate to the RDS service.
        * Click "Create database."
        * Choose "MySQL" as the engine type.
        * Select a template (e.g., "Free tier").
        * Configure the database instance settings:
            * **DB instance identifier:** Choose a name for your RDS instance.
            * **Master username:** Set a username (e.g., 'admin').
            * **Master password:** Set a strong password.
        * Keep other settings as default for this demo.
        * Create the database.
    * **Create the Database and Table:**
        * Once the RDS instance is created, connect to it using the mysql client:

            ```bash
            mysql -h <your-rds-endpoint> -u <your-rds-username> -p
            ```

            * You'll be prompted for the password you set earlier.

        * Create a database and a table named `files`:

            ```sql
            CREATE DATABASE <your-database-name>;
            USE <your-database-name>;
            CREATE TABLE files (
                id INT AUTO_INCREMENT PRIMARY KEY,
                file_name VARCHAR(255) NOT NULL,
                file_size INT NOT NULL,
                upload_date DATETIME NOT NULL,
                s3_url VARCHAR(255) NOT NULL
            );
            ```

9. **Configure the Application:**
    * Open the `app.py` file in your text editor.
    * Replace the placeholders with your actual AWS credentials and database information:

    ```python
    # AWS S3 Configuration
    S3_BUCKET = 'your-s3-bucket-name' 
    S3_REGION = 'your-s3-region' 

    # AWS RDS Configuration
    DB_HOST = 'your-rds-endpoint'
    DB_USER = 'your-rds-username'
    DB_PASSWORD = 'your-rds-password'
    DB_NAME = 'your-database-name' 
    ```

10. **Create Necessary Directories:**

    ```bash
    mkdir uploads templates
    ```
    * `uploads`: This is where uploaded files will be temporarily stored on the EC2 instance before being transferred to S3.
    * `templates`: This will hold the HTML template for our application's web interface.

11. **Create the `index.html` File:**

    * Inside the `templates` directory, create a new file named `index.html`.
    * Copy and paste the provided `index.html` code into this file. This HTML code defines the look and feel of the file upload/download interface.

12. **Run the Application:**

    ```bash
    gunicorn --bind 0.0.0.0:80 app:app
    ```
    * `gunicorn`: A Python WSGI HTTP server that will handle incoming requests to our Flask application.
    * `--bind 0.0.0.0:80`: Tells gunicorn to listen for requests on all available network interfaces (0.0.0.0) on port 80 (the default HTTP port).
    * `app:app`: The name of our Flask application instance.

    * Make sure your EC2 security group allows inbound traffic on port 80.

13. **Access the Application:**
    * Open a web browser and enter your EC2 instance's public IP address. You should see the application's homepage, allowing you to upload and download files.
      
<img width="1417" alt="Screenshot 2024-09-05 at 7 40 41 PM" src="https://github.com/user-attachments/assets/4a321776-f557-47c5-8814-cf54b75b3d58">

   

14. **Set up a Custom Domain (Optional):**
    * In the AWS console, go to the Route 53 service.
    * Create a hosted zone for your domain name.
    * Create an A record that points your domain name to your EC2 instance's public IP address.
    * If your domain is registered with a third-party registrar, you'll need to update the nameservers at your registrar to the ones provided by Route 53.
    * 
 <img width="1067" alt="Screenshot 2024-09-05 at 7 42 51 PM" src="https://github.com/user-attachments/assets/baf4a8d5-049f-43ec-9ee4-5401923a28b7">



## Important Considerations

* **Security Best Practices:**
    * **This setup is for demonstration purposes only.** Do not use it for production environments as it has security vulnerabilities.
    * **Never hardcode credentials** in your code. In a real-world scenario, use AWS KMS (Key Management Service) or Secrets Manager to securely store and manage your credentials.
    * **Use HTTPS** to encrypt data in transit between the user'
    * **Encrypt Your Data:** Ensure data is encrypted in transit and at rest using AWS services like KMS.
    * **Secure Your Application:** Use HTTPS for secure communication between users and your application. Set up SSL/TLS certificates via AWS Certificate Manager or a similar service.
    * **Use IAM Roles:** Assign appropriate IAM roles to your EC2 instance for accessing S3 and RDS securely.
          
* **Cost Management:**
    * **Monitor Your AWS Usage:** Use AWS CloudWatch to monitor resource usage and set up billing alerts.
    * **Cleanup:** After your demo, ensure to terminate your EC2 instance and delete S3 buckets and RDS instances to avoid unexpected charges.

## 🎉 voilà! You've deployed an application on AWS using core services! 

From here, you can build and expand upon this foundation. Consider integrating additional services like:

* **CloudFront:** Place it in front of your S3 bucket for faster content delivery and improved user experience. Imagine your application serving users across the globe. CloudFront's edge locations cache your files, ensuring they're delivered lightning-fast, no matter where your users are. 

* **DynamoDB:** Explore a NoSQL database option for even better performance and scalability. If your application experiences sudden spikes in traffic or handles massive amounts of data, DynamoDB's flexible schema and on-demand scaling can handle the load with ease.

* **Lambda:** Leverage serverless functions for processing tasks and event-driven workflows.  Say goodbye to server management! With Lambda, you can trigger code execution in response to events like file uploads or database changes, automating tasks and streamlining your application's logic. 

The possibilities are endless! Keep learning and exploring the vast world of AWS!

---

**Connect with me:**

* **LinkedIn:** [(https://www.linkedin.com/in/lalit-sa)]

Feel free to reach out if you have any questions or would like to discuss further enhancements to this project!
