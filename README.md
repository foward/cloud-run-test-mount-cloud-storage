# Google Cloud Run test mounting Google Cloud Storage Bucket

This project is a simple Flask application that manages directories and lists their contents in a specified mount path, to test the **"Beta"** functionality to mount a Google Cloud Storage Bucket in a Google Cloud Run service.

For more information, visit: [Google Cloud Storage Volume Mounts](https://cloud.google.com/run/docs/configuring/services/cloud-storage-volume-mounts#gcloud)


## Description

Simplifying Cloud Storage Management with Cloud Run Volume Mounts
Managing storage in a containerized environment can be complex, especially when dealing with cloud-native applications. Google Cloud Run, a fully managed platform that automatically scales your applications, recently introduced a feature that simplifies this process: Cloud Storage volume mounts. This feature allows you to mount a Cloud Storage bucket as a volume directly in your Cloud Run service, making it easier to manage files and data within your containers.

### What is Cloud Storage Volume Mounting?
Cloud Storage volume mounting in Cloud Run allows you to present the contents of a Cloud Storage bucket as files within your container’s file system. This means you can access and manage these files using standard file system operations, just like you would with local files, without needing to modify your application code to use cloud storage APIs.

### Why Use Cloud Storage Volume Mounts?
**Seamless Integration**: If your application expects data to be stored on a local file system, you can mount a Cloud Storage bucket and access it as if it were a local directory.
**No Additional Dependencies**: You don't need to install or configure any additional software like Cloud Storage FUSE in your container.
Simplified Codebase: Continue using your existing file operations without needing to integrate specific cloud storage APIs.
How to Set Up Cloud Storage Volume Mounts with gcloud
You can configure Cloud Storage volume mounts using the gcloud command-line tool. Here’s a quick guide:

Adding and Mounting a Volume:
Use the following command to add a Cloud Storage volume and mount it to your Cloud Run service:

   ```sh
gcloud beta run services update SERVICE_NAME \
--add-volume name=VOLUME_NAME,type=cloud-storage,bucket=BUCKET_NAME \
--add-volume-mount volume=VOLUME_NAME,mount-path=/mnt/my-volume
   ```
Replace SERVICE_NAME with your Cloud Run service's name, VOLUME_NAME with a name for your volume, and BUCKET_NAME with your Cloud Storage bucket's name.

Mounting as Read-Only:
If you want to mount the bucket as read-only, modify the volume addition command as follows:

   ```sh
gcloud beta run services update SERVICE_NAME \
--add-volume name=VOLUME_NAME,type=cloud-storage,bucket=BUCKET_NAME,readonly=true \
--add-volume-mount volume=VOLUME_NAME,mount-path=/mnt/my-volume
   ```
Multiple Containers:
If your service uses multiple containers, you need to specify the volume for each container:

   ```sh
gcloud beta run services update SERVICE_NAME \
--add-volume name=VOLUME_NAME,type=cloud-storage,bucket=BUCKET_NAME \
--container CONTAINER_1 \
--add-volume-mount volume=VOLUME_NAME,mount-path=/mnt/container1-volume \
--container CONTAINER_2 \
--add-volume-mount volume=VOLUME_NAME,mount-path=/mnt/container2-volume
   ```
Reading and Writing to a Mounted Volume
Once your volume is mounted, you can read from and write to it using standard file system commands in your preferred programming language. Here’s an example using Python:

Writing to a File:

```sh
with open("/mnt/my-volume/sample-logfile.txt", "a") as f:
    f.write("Hello, Cloud Storage volume!\n")
```

Reading from a File:

```sh
with open("/mnt/my-volume/sample-logfile.txt", "r") as f:
    content = f.read()
    print(content)
```

These operations work just like they would with local files, making it easier to integrate cloud storage into your existing applications.

Conclusion
Google Cloud Run's Cloud Storage volume mounts provide a simple yet powerful way to manage storage in your cloud-native applications. By mounting a Cloud Storage bucket directly to your container’s file system, you can access and manage files with ease, using the same tools and libraries you're already familiar with. This feature reduces complexity and allows for a more seamless transition to cloud-based storage, without the need for significant code changes.

For more detailed instructions and best practices, you can explore the Cloud Run documentation.
## Installation

1. Clone the repository:
    ```sh
    git clone <repository-url>
    cd <repository-directory>
    ```

2. Create a virtual environment and activate it:
    ```sh
    python3 -m venv venv
    source venv/bin/activate
    ```

3. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

1. Set the environment variable for the data file path (optional, defaults to `/mnt/data`):
    ```sh
    export DATA_FILE_PATH=/path/to/your/data
    ```

2. Run the Flask application:
    ```sh
    python main.py
    ```

3. Access the application in your web browser at `http://localhost:8080`.

## Environment Variables

- `DATA_FILE_PATH`: The path where the directories and files are managed. Defaults to `/mnt/data`.
- `PORT`: The port on which the Flask application runs. Defaults to `8080`.

## Endpoints

- `GET /`: Creates a folder named `FranciscoFolder` in the specified mount path and lists the contents of the directory.

## Docker

### Build and Push Docker Image

1. Build the Docker image:
    ```sh
    docker build -f Dockerfile -t "europe-west1-docker.pkg.dev/PROJECT_NAME/SERVICE_NAME/test-gcs-with-cloud-run" .
    ```

2. Push the Docker image:
    ```sh
    docker push "europe-west1-docker.pkg.dev/PROJECT_NAME/SERVICE_NAME/test-gcs-with-cloud-run"
    ```

### Deploy to Google Cloud Run

1. Deploy the service:
    ```sh
    gcloud run deploy test-cloud-run-gcs --source . --region=europe-west1 --platform=managed --timeout=3600 --allow-unauthenticated --session-affinity --max-instances=2
    ```

2. Update the service to add a Cloud Storage volume (change the BUCKET_NAME):
    ```sh
    BUCKET_NAME=raw-input-data-bucket
    gcloud beta run services update test-cloud-run-gcs \
    --add-volume name=VOLUME_NAME,type=cloud-storage,bucket=$BUCKET_NAME \
    --add-volume-mount volume=VOLUME_NAME,mount-path=/mnt/data
    ```

### Run Locally with Docker

1. Run the Docker container:
    ```sh
    docker run -p 8080:8080 europe-west1-docker.pkg.dev/PROJECT_NAME/SERVICE_NAME/test-gcs-with-cloud-run
    ```

2. Run the Docker container with a local volume:
    ```sh
    docker run -p 8080:8080 -v /Users/Francisco/InputImages:/mnt/data europe-west1-docker.pkg.dev/PROJECT_NAME/SERVICE_NAME/test-gcs-with-cloud-run
    ```

3. Access the application in your web browser at `http://localhost:8080`.

## Logging

The application uses basic logging to log info and error messages. Logs are printed to the console.

## Error Handling

Errors encountered during directory creation or listing are logged and returned as part of the response.

## License

This project is licensed under the MIT License.