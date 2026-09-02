# This file is used to , contain all the api routes in one file , so that collective we can run run one server and 
# access all the routes 

from fastapi import FastAPI 
from api import auth,projects,proposals

app = FastAPI()

app.include_router(auth.router,prefix="/api/auth",tags=["auth"])
app.include_router(projects.router,prefix="/api",tags=["projects"])
app.include_router(proposals.router,prefix='/api',tags=["proposals"])


#TODO: Explore CORS , use case and why is it used for 

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)









































# Question whats this auth.router, and projects.router ?? 

'''
You're importing the entire auth.py file as a module named auth. Then, auth.router simply means: 
"the router variable that lives inside the auth module." It's no different conceptually than if auth.py 
had defined SECRET_KEY = "abc", and you accessed it elsewhere as auth.SECRET_KEY. router is just 
a name — you could've called it anything (my_router, r) — but router is the near-universal convention, 
so everyone recognizes it instantly.

'''



#! Confusion/Mistake ,: Dont misunderstand that 

'''
/api/auth/signup 
/api/auth/login
 is because  it follows any petter or anything like , folder/filename/endpoin

 is has nothing to do with all  of it ,....
 Its just a conincidence that it looks this way 

 It would have worked in similary fashion even if it had no /api/auth 
  just simply /signup , /login 

  --> this is the naming convention that it followed because of the requirements mentioned in the notion doc

--> All this prefix="/api and prefix="/api/auth"  are purely naming convention for humans readability no logic 

--> It would have worked exactly same even with anything random like 

--> prefix="/api", prefix="/api/auth", prefix="/xyz123", prefix="/banana" — all of these would work identically from a pure functionality standpoint.


#?The only two things that genuinely matter, functionally

1 Uniqueness — no two routes can have the identical final (method, path) combination,

2.Consistency between what you register and what you call
If you named your prefix /banana, you'd just need to call curl http://.../banana/signup instead 
of /api/auth/signup — equally functional, just a different (admittedly odd) string.

'''
















































# Consider Reading and Implementing 
'''

One more layer worth planning for: separate route logic from business logic

As your routes grow (especially the proposal-accept endpoint, which the doc calls "the most important 
business-logic endpoint" — multi-table transaction, rollback handling), you may eventually want a 
services/ or crud/ folder holding the actual DB-transaction logic, with your api/proposals.py route 
functions staying thin (just handling the HTTP layer — auth, validation, calling the service function, 
returning a response). Not something you need immediately for a mini project, but worth keeping in mind 
as proposals.py's accept-route logic grows — if it starts feeling bloated with raw DB queries mixed into 
the route function itself, that's the signal to consider this split.


'''