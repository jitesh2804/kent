import psycopg2
from datetime import datetime, timedelta
import logging

# Setup logging
logging.basicConfig(
    filename='update_status.log',  
    level=logging.INFO,  
    format='%(asctime)s - %(levelname)s - %(message)s'  
)

# Database connection configuration
db_config = {
    "host": "192.168.255.71",
    "port": "5433",
    "database": "verve",
    "user": "postgres",
    "password": "Sum#321"
}

connection = None  

try:
    logging.info("Starting the script to update list statuses.")

    # Connect to the PostgreSQL database
    connection = psycopg2.connect(**db_config)
    cursor = connection.cursor()
    logging.info("Connected to the database successfully.")

    # Define dates
    today = datetime.now().strftime("%Y%m%d")
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y%m%d")
    day_before_yesterday = (datetime.now() - timedelta(days=2)).strftime("%Y%m%d")
  
    # Generate dynamic list names
    today_names = [f"NPS_CALL_{today}", f"Incomplete_{today}", f"CALL_BACK_{today}", f"ABND_CALLBACK_{today}", f"AMC_{today}", f"ESC_CALLBACK_{today}", f"Yellow_Call_Back_{today}", f"UW_AMC_Calling_{today}"]
    yesterday_names = [f"NPS_CALL_{yesterday}", f"Incomplete_{yesterday}", f"CALL_BACK_{yesterday}", f"ABND_CALLBACK_{yesterday}", f"AMC_{yesterday}", f"ESC_CALLBACK_{yesterday}", f"Yellow_Call_Back_{yesterday}", f"UW_AMC_Calling_{yesterday}"]
    day_2_names = [f"NPS_CALL_{day_before_yesterday}", f"Incomplete_{day_before_yesterday}", f"CALL_BACK_{day_before_yesterday}", f"ABND_CALLBACK_{day_before_yesterday}", f"AMC_{day_before_yesterday}", f"ESC_CALLBACK_{day_before_yesterday}", f"Yellow_Call_Back_{day_before_yesterday}", f"UW_AMC_Calling_{day_before_yesterday}"]
  
    logging.info(f"Today names: {today_names}")
    logging.info(f"Yesterday names: {yesterday_names}")
    logging.info(f"Day-before-yesterday names: {day_2_names}")
  
    # Update today's and yesterday's lists to ACTIVE with priority and weightage
    cursor.execute("""
        UPDATE ct_list
        SET status = 'ACTIVE', priority = 9, weightage = 0.1
        WHERE name = ANY(%s)
    """, (today_names + yesterday_names,))
    logging.info("Updated today's and yesterday's lists to ACTIVE.")

    # Update day-2's lists to INACTIVE
    cursor.execute("""
        UPDATE ct_list
        SET status = 'INACTIVE'
        WHERE name = ANY(%s)
    """, (day_2_names,))
    logging.info("Updated day-before-yesterday's lists to INACTIVE.")

    # Commit the changes
    connection.commit()
    logging.info("Database changes committed successfully.")

except Exception as e:
    logging.error(f"An error occurred: {e}")

finally:
    if connection:
        connection.close()
        logging.info("Database connection closed.")
    else:
        logging.warning("No database connection to close.")
