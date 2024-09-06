from flask import Flask, request, redirect, url_for, render_template, abort
import boto3
import os
import pymysql
from werkzeug.utils import secure_filename
from datetime import datetime

app = Flask(__name__)

# AWS S3 Configuration
S3_BUCKET = 'your-s3-bucket-name'  # Replace with your S3 bucket name
S3_REGION = 'your-s3-region'      # Replace with your S3 region

s3 = boto3.client('s3', region_name=S3_REGION)

# AWS RDS Configuration
DB_HOST = 'your-rds-endpoint'        # Replace with your RDS endpoint
DB_USER = 'your-rds-username'        # Replace with your RDS username
DB_PASSWORD = 'your-rds-password'    # Replace with your RDS password
DB_NAME = 'your-database-name'        # Replace with your database name

connection = pymysql.connect(host=DB_HOST,
                             user=DB_USER,
                             password=DB_PASSWORD,
                             db=DB_NAME,
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

# Set upload folder and allowed extensions
UPLOAD_FOLDER = '/home/ubuntu/uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def generate_presigned_url(bucket_name, object_key, expiration=3600):
    s3 = boto3.client('s3', region_name=S3_REGION)
    try:
        response = s3.generate_presigned_url('get_object',
                                             Params={'Bucket': bucket_name,
                                                     'Key': object_key},
                                             ExpiresIn=expiration,
                                             HttpMethod='GET')
    except Exception as e:
        print(e)
        return None
    return response

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'No file part'
        file = request.files['file']
        if file.filename == '':
            return 'No selected file'
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            # Upload file to S3 without ACL parameter
            try:
                s3.upload_file(file_path, S3_BUCKET, filename)
            except Exception as e:
                return str(e)

            # Save file metadata to RDS
            s3_url = generate_presigned_url(S3_BUCKET, filename)
            if s3_url is None:
                return 'Error generating download link'
            
            with connection.cursor() as cursor:
                sql = "INSERT INTO files (file_name, file_size, upload_date, s3_url) VALUES (%s, %s, %s, %s)"
                cursor.execute(sql, (filename, os.path.getsize(file_path), datetime.now(), s3_url))
                connection.commit()

            return redirect(url_for('upload_file'))

    # Fetch the list of files to display
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM files")
        files = cursor.fetchall()
    
    return render_template('index.html', files=files)

@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    # Generate presigned URL for download
    s3_url = generate_presigned_url(S3_BUCKET, filename)
    if s3_url:
        return redirect(s3_url)
    else:
        abort(404)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
