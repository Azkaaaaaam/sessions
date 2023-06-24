from flask import Flask
from sqlalchemy import create_engine, text

app = Flask(__name__)

conn_string = 'postgresql://Azza:123456@localhost/MyDB'
db = create_engine(conn_string)
conn = db.connect()

@app.route('/metrics/orders/General_Median_Visits')
def general_median_visits():
    # General Median Visits (NB)
    sessions_query = text("""
        WITH ordered_sessions AS (
            SELECT *,
                   CASE
                       WHEN type = 'placed_order' THEN ROW_NUMBER() OVER (PARTITION BY "customer-id" ORDER BY timestamp)
                   END AS order_number
            FROM public."My_Table"
        )
        SELECT percentile_cont(0.5) WITHIN GROUP (ORDER BY order_number) AS median_visits_before_order
        FROM ordered_sessions
        WHERE type = 'placed_order';
    """)

    median_visits_result = conn.execute(sessions_query).scalar()
    return str(median_visits_result)



@app.route('/metrics/orders/General_Duration_Median')
def general_duration_median():
    # General duration median (mns)
    duration_query = """
        WITH ordered_sessions AS (
            SELECT *,
                   LAG(timestamp) OVER (PARTITION BY "customer-id" ORDER BY timestamp) AS previous_timestamp,
                   CASE
                       WHEN ROW_NUMBER() OVER (PARTITION BY "customer-id" ORDER BY timestamp) = 1 THEN INTERVAL '0 minutes'
                       ELSE timestamp - LAG(timestamp) OVER (PARTITION BY "customer-id" ORDER BY timestamp)
                   END AS duration
            FROM public."My_Table"
            WHERE type = 'placed_order'
        )
        SELECT percentile_cont(0.5) WITHIN GROUP (ORDER BY EXTRACT(EPOCH FROM duration) / 60.0) AS median_session_duration_minutes
        FROM ordered_sessions
    """
    duration_result = conn.execute(text(duration_query))
    median_sessionduration_result = duration_result.scalar()
    return str(median_sessionduration_result)


@app.route('/metrics/orders/Customer_Duration_Median/<customer_id>', methods=['GET'])
def customer_duration_median(customer_id):
    # Customer's duration median (mns) query
    duration_query = """
        WITH ordered_sessions AS (
            SELECT *,
                   LAG(timestamp) OVER (PARTITION BY "customer-id" ORDER BY timestamp) AS previous_timestamp,
                   CASE
                       WHEN ROW_NUMBER() OVER (PARTITION BY "customer-id" ORDER BY timestamp) = 1 THEN INTERVAL '0 minutes'
                       ELSE timestamp - LAG(timestamp) OVER (PARTITION BY "customer-id" ORDER BY timestamp)
                   END AS duration
            FROM public."My_Table"
            WHERE type = 'placed_order'
        )
        SELECT percentile_cont(0.5) WITHIN GROUP (ORDER BY EXTRACT(EPOCH FROM duration) / 60.0) AS median_session_duration_minutes
        FROM ordered_sessions
        WHERE "customer-id" = :customer_id
    """

    result = conn.execute(text(duration_query).params(customer_id=customer_id))
    median_session_duration_result = result.scalar()

    return str(median_session_duration_result)  # Return the result as a string


@app.route('/metrics/orders/Customer_session_nb/<customer_id>', methods=['GET'])
def Customer_session_nb(customer_id):
    cust_sessions_query = """
        WITH ordered_sessions AS (
            SELECT *,
                   CASE
                       WHEN type = 'placed_order' THEN ROW_NUMBER() OVER (PARTITION BY "customer-id" ORDER BY timestamp)
                   END AS order_number
            FROM public."My_Table"
        )
        SELECT percentile_cont(0.5) WITHIN GROUP (ORDER BY order_number) AS median_visits_before_order
        FROM ordered_sessions
        WHERE type = 'placed_order' AND "customer-id" = :customer_id
    """

    result = conn.execute(text(cust_sessions_query).params(customer_id=customer_id))
    median_session_duration_result = result.scalar()
    return str(median_session_duration_result)

if __name__ == '__main__':
    app.run()
