# # Database Connection Settings
# import psycopg2

# DB_CONFIG = {
#     "host": "localhost",
#     "database": "ecommerce",
#     "user": "postgres",
#     "password": "Harshit@123",
#     "port": "5432"
# }

# def get_conn():
#     """Always returns a fresh, live connection."""
#     return psycopg2.connect(**DB_CONFIG)


import psycopg2

NEON_URI = "postgresql://neondb_owner:npg_cOFkpY3MRtf6@ep-jolly-sound-ao5n4qw9-pooler.c-2.ap-southeast-1.aws.neon.tech/neondb?sslmode=require"

def get_conn():
    """Always returns a fresh, live connection to Neon DB."""
    return psycopg2.connect(NEON_URI)