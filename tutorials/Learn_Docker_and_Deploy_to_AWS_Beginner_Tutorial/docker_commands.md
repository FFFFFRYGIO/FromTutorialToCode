# Docker commands

This project demonstrates basic Docker usage, including:

- building a Docker image
- running a container
- exposing a web app on localhost
- using bind mounts
- using Docker named volumes
- checking whether files from a shared folder are visible inside the container

---

## 1. Build the Docker Image

From the project directory, run:

```powershell
docker build -t test_container .
```

This builds a Docker image named `test_container` using the `Dockerfile` in the current directory.

---

## 2. Run the Container with Port Mapping

Run the container and expose it on localhost:

```powershell
docker run -p 127.0.0.1:8080:8080 test_container
```

This maps:

```text
host:      127.0.0.1:8080
container:          8080
```

After starting the container, open:

```text
http://127.0.0.1:8080
```

---

## 3. Use a Shared Folder with a Bind Mount

A bind mount allows the container to access a folder from your computer.

Example host folder:

```text
D:\github\FromTutorialToCode\tutorials\Learn_Docker_and_Deploy_to_AWS_-_Beginner_Tutorial\shared_folder
```

Run the container with the shared folder mounted into `/app/shared_folder` inside the container:

```powershell
docker run --rm `
  -v "D:\github\FromTutorialToCode\tutorials\Learn_Docker_and_Deploy_to_AWS_-_Beginner_Tutorial\shared_folder:/app/shared_folder" `
  test_container
```

Inside the container, the folder will be available here:

```text
/app/shared_folder
```

---

## 4. Test Whether a Shared File Is Visible

Create a test file on your host machine:

```powershell
echo "Hello from shared folder!" > shared_folder\test.txt
```

Then run this command to print the file content from inside the container:

```powershell
docker run --rm `
  -v "D:\github\FromTutorialToCode\tutorials\Learn_Docker_and_Deploy_to_AWS_-_Beginner_Tutorial\shared_folder:/app/shared_folder" `
  test_container `
  python -c "print(open('/app/shared_folder/shared_file.txt').read())"
```

Expected output:

```text
Shared content!
```

If you see this text, the shared folder is correctly mounted into the container.

---

## 5. Create a Docker Named Volume

Docker volumes are managed by Docker and are useful for persistent data.

Create a named volume:

```powershell
docker volume create shared_volume
```

Check existing volumes:

```powershell
docker volume ls
```

---

## 6. Run the Container with a Named Volume

Mount the named volume into the container:

```powershell
docker run --rm `
  -v shared_volume:/app/shared_folder `
  test_container
```

The named volume is now available inside the container at:

```text
/app/shared_folder
```

---

## 7. Test Writing to the Named Volume

Write a file into the Docker volume:

```powershell
docker run --rm `
  -v shared_volume:/app/shared_folder `
  test_container `
  python -c "open('/app/shared_folder/volume_test.txt', 'w').write('Hello from Docker volume!')"
```

Now read the file from another container run:

```powershell
docker run --rm `
  -v shared_volume:/app/shared_folder `
  test_container `
  python -c "print(open('/app/shared_folder/volume_test.txt').read())"
```

Expected output:

```text
Hello from Docker volume!
```

This confirms that the Docker volume persists data between container runs.

---

## Important Notes

### Bind Mount vs Named Volume

A bind mount uses a real folder from your computer:

```powershell
-v "D:\path\to\shared_folder:/app/shared_folder"
```

A named volume is managed by Docker:

```powershell
-v shared_volume:/app/shared_folder
```

### Container Paths

Because this image uses Linux-based Python, container paths should use Linux-style paths, for example:

```text
/app/shared_folder
```

Do not use a Windows path as the container path, for example:

```powershell
-v shared_volume:D:\some\windows\path
```

That is incorrect for Linux containers.

---

## Useful Commands

Stop all running containers:

```powershell
docker stop $(docker ps -q)
```

List running containers:

```powershell
docker ps
```

List all containers:

```powershell
docker ps -a
```

Remove the image:

```powershell
docker rmi test_container
```

Remove the named volume:

```powershell
docker volume rm shared_volume
```

```

One important correction: this command from your notes is incomplete/incorrect:

```powershell id="c75dgj"
docker run -v D:\github\FromTutorialToCode\tutorials\Learn_Docker_and_Deploy_to_AWS_-_Beginner_Tutorial/shared_folder test_container
```

It should include both the **host path** and the **container path**:

```powershell id="kgahx9"
docker run -v "D:\github\FromTutorialToCode\tutorials\Learn_Docker_and_Deploy_to_AWS_-_Beginner_Tutorial\shared_folder:/app/shared_folder" test_container
```

