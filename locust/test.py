from locust import HttpUser, TaskSet, task, between, LoadTestShape

class UserBehavior(TaskSet):
    @task
    def access_main_page(self):
        self.client.get("/")

class WebsiteUser(HttpUser):
    tasks = [UserBehavior]
    wait_time = between(1, 1)  # Ensures a new user is spawned every second

class OneUserPerSecondShape(LoadTestShape):
    """
    A custom load test shape that ensures we have one user per second.
    """

    def tick(self):
        run_time = self.get_run_time()

        # Every second we start a new user
        user_count = run_time

        return (user_count, 1)

# Use the custom shape class for the load test
class WebsiteUser(HttpUser):
    tasks = [UserBehavior]
    wait_time = between(1, 1)  # Ensure each user waits exactly 1 second between tasks

class User(HttpUser):
    wait_time = between(1, 1)
    tasks = [UserBehavior]
