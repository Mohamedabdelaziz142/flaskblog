from locust import HttpUser, task, between

class BlogUser(HttpUser):
    wait_time = between(1, 5)

    @task(weight=1) 
    def login(self):
        self.client.post('/login', data={
            'email': 'test@example.com',
            'password': 'testpassword'
        })

    @task(weight=2)  
    def create_post(self):
        data = {'title': f'Test Post {self.client.id}', 'content': '...'}
        response = self.client.post('/post/new', json=data)
        self.post_id = int(response.json['id'])  

    @task(weight=1) 
    def delete_post(self):
        if hasattr(self, 'post_id'):  
            self.client.post(f'/post/{self.post_id}/delete')
            del self.post_id  

    @task(weight=1)  
    def update_post(self):
        if hasattr(self, 'post_id'): 
            data = {'title': f'Updated Title {self.client.id}', 'content': '...'}
            self.client.post(f'/post/{self.post_id}/update', json=data)
