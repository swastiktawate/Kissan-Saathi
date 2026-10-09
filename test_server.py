import subprocess
import time
import urllib.request
import sys

def test_server():
    print("Starting uvicorn...")
    server = subprocess.Popen([r".\venv\Scripts\uvicorn.exe", "backend.app.main:app", "--port", "8000"])
    time.sleep(3) # Wait for startup
    
    try:
        req = urllib.request.Request("http://localhost:8000/api/v1/health")
        with urllib.request.urlopen(req) as response:
            data = response.read().decode('utf-8')
            print(f"Response: {data}")
            if "ok" in data:
                print("Server health check passed.")
            else:
                print("Server health check failed.")
                sys.exit(1)
    except Exception as e:
        print(f"Failed to connect: {e}")
        sys.exit(1)
    finally:
        server.terminate()
        server.wait()

if __name__ == '__main__':
    test_server()
