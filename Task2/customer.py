import requests
import time

def simulate_customer():
    print("--- Customer Simulation: Task 2 ---")
    res = requests.post("http://127.0.0.1:8000/recaptcha/in", json={}).json()
    tid = res["TaskID"]
    
    while True:
        status = requests.get(f"http://127.0.0.1:8000/recaptcha/res?task_id={tid}").json()
        
        if status["status"] == "completed":
            print("\n✅ Task Completed!")
            print(f"Score: {status.get('score')}")
            print(f"Action: {status.get('success_text')}")
            
            token = status.get('token_value')
            if token:
                print(f"Token Value: {token[:50]}...[TRUNCATED]")
            else:
                print("Token Value: [Not Captured - See Logs]")
            break
            
        elif status["status"] == "failed":
            print(f"❌ Failed: {status.get('error')}")
            break
            
        print("Waiting for solve...")
        time.sleep(3)

if __name__ == "__main__":
    simulate_customer()