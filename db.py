import pymysql
from config import DB_CONFIG


def get_connection():
    return pymysql.connect(**DB_CONFIG)


def get_expiring_installations(days, notification_type):

    sql = """
    SELECT
        i.id,
        e.name AS employee_name,
        e.email,
        d.device_name,
        s.name AS software_name,
        i.expires_at

    FROM installations i

    JOIN devices d
        ON d.id = i.device_id

    JOIN employees e
        ON e.id = d.employee_id

    JOIN security_softwares s
        ON s.id = i.software_id

    LEFT JOIN notification_history nh
        ON nh.installation_id = i.id
       AND nh.notification_type = %s

    WHERE i.expires_at BETWEEN CURDATE()
                          AND DATE_ADD(CURDATE(), INTERVAL %s DAY)

      AND nh.id IS NULL

    ORDER BY i.expires_at
    """

    conn = get_connection()

    try:
        with conn.cursor() as cursor:
            cursor.execute(
                sql,
                (
                    notification_type,
                    days
                )
            )

            return cursor.fetchall()

    finally:
        conn.close()


def insert_notification_history(
        installation_id,
        notification_type="expire_30"
):

    sql = """
    INSERT INTO notification_history
    (
        id,
        installation_id,
        notification_type
    )
    VALUES
    (
        UUID(),
        %s,
        %s
    )
    """

    conn = get_connection()

    try:
        with conn.cursor() as cursor:
            cursor.execute(
                sql,
                (
                    installation_id,
                    notification_type
                )
            )

        conn.commit()

    finally:
        conn.close()


def insert_failed_history(
    installation_id,
    notification_type,
    error
):

    sql = """
    INSERT INTO notification_history
    (
        id,
        installation_id,
        notification_type,
        result,
        error_message
    )
    VALUES
    (
        UUID(),
        %s,
        %s,
        'FAILED',
        %s
    )
    """

    conn = get_connection()

    try:
        with conn.cursor() as cursor:
            cursor.execute(
                sql,
                (
                    installation_id,
                    notification_type,
                    str(error)
                )
            )

        conn.commit()

    finally:
        conn.close()