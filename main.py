from fastapi import FastAPI
from dotenv import load_dotenv
from app.routes import user_routes, auth_route, job_routes , job_seeker_routes, admin_routes
from app.middleware.auth_middleware import auth_middleware
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.middleware("http")(auth_middleware)

app.include_router(auth_route.router, prefix="/auth", tags=["Authentication"])
app.include_router(user_routes.router, prefix="/users", tags=["Users"])
app.include_router(job_routes.router, prefix="/jobs", tags=["Jobs"]) 
app.include_router(job_seeker_routes.router,prefix="/job-seeker",tags=["Job Seeker"])
app.include_router(admin_routes.router, prefix="/admin", tags=["admin"])


@app.get("/")
async def root():
    return {"message": "Welcome to Tradala API"}