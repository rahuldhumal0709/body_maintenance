import psycopg2
from psycopg2.extras import RealDictCursor
from django.conf import settings

def load_email_configuration():
    try:
        # Get database connection settings from Django's settings
        db_settings = settings.DATABASES['default']
        conn = psycopg2.connect(
            dbname=db_settings['NAME'],
            user=db_settings['USER'],
            password=db_settings['PASSWORD'],
            host=db_settings['HOST'],
            port=db_settings['PORT'],
        )
        
        # Execute the query to fetch email configuration
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT * FROM djangoapp_emailconfiguration LIMIT 1;")
            config = cursor.fetchone()
        
        if config:
            # Dynamically update Django's email settings
            settings.EMAIL_HOST = config['smtp_host']
            settings.EMAIL_PORT = config['smtp_port']
            settings.EMAIL_HOST_USER = config['smtp_user']
            settings.EMAIL_HOST_PASSWORD = config['smtp_password']
            settings.EMAIL_USE_TLS = config['use_tls']
            settings.EMAIL_USE_SSL = config['use_ssl']
            print("Email configuration loaded successfully.")
        else:
            print("No email configuration found in the database.")

    except Exception as e:
        print(f"Error loading email configuration: {e}")
    finally:
        if 'conn' in locals():
            conn.close()