from locust import HttpUser, task


class User(HttpUser):
    @task
    def post_message(self):
        data = {
            "from": "string",
            "message": "string"
        }
        self.client.post("/messages", json=data, headers={"Content-Type": "application/json"})
