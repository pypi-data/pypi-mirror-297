from fastapi import FastAPI
from fastapi_sqlalchemy import DBSessionMiddleware  # middleware helper
from fastapi_sqlalchemy import db  # an object to provide global access to a database session
from sample_test_sumit_50fin.example import addition

app = FastAPI()

app.add_middleware(DBSessionMiddleware, db_url="postgresql://kartikkumar:kartikkumar50fin@localhost:5432/postgres")

# once the middleware is applied, any route can then access the database session 
# from the global ``db``


app.get("/")
async def root():
    res= addition(2,4)
    


