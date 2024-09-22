import os
import openai

class AI2SQL:
    def __init__(self, username=None, password=None):
        self.username = username or os.getenv("AI2SQL_USERNAME")
        self.password = password or os.getenv("AI2SQL_PASSWORD")
        if not self._validate_credentials():
            raise ValueError("Invalid credentials")

    def generate_sql(self, prompt, dialect="mysql"):
        return self._call_ai_service(prompt, dialect)

    def _validate_credentials(self):
        # In a real implementation, this would validate against an auth service
        return bool(self.username and self.password)

    def _call_ai_service(self, prompt, dialect):
        openai.api_key = os.getenv("OPENAI_API_KEY")
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": f"You are a SQL generator for {dialect}. Respond with only the SQL query."},
                    {"role": "user", "content": prompt}
                ]
            )
            return response.choices[0].message['content'].strip()
        except AttributeError:
            # If the above fails, try the new API style
            client = openai.OpenAI(api_key=openai.api_key)
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": f"You are a SQL generator for {dialect}. Respond with only the SQL query."},
                    {"role": "user", "content": prompt}
                ]
            )
            return response.choices[0].message.content.strip()
