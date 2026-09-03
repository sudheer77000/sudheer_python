from pydantic import BaseModel, Field
from typing import Optional
def emp(name: str, age: int):
    print(f'Name: {name}, age : {age}')

emp("Sudheer","Ishitha")

class User(BaseModel):
    name: str = Field(min_length=2, max_length=5)
    age: Optional[int] = Field(default=None, gt=18, lt=40)

user1 = User(name="Gu",age = 20)

print(user1.name)
print(user1.age)