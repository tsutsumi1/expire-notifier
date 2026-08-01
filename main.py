from db import (
    get_expiring_installations,
    insert_notification_history,
    insert_failed_history
)

from mail import send_mail
import logging


logging.basicConfig(
    filename="logs/app.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)

notifications = [
    (30, "expire_30"),
    (7, "expire_7"),
    (1, "expire_1")
]


def main():

    for days, notification_type in notifications:

        rows = get_expiring_installations(
            days,
            notification_type
        )

        if not rows:
            continue

        for row in rows:

            try:

                body = f"""
{row['employee_name']} 様

ライセンス期限のお知らせです。

PC:
{row['device_name']}

ソフト:
{row['software_name']}

期限:
{row['expires_at']}

残り:
約{days}日
"""


                send_mail(
                    row["email"],
                    f"期限通知（残り{days}日）",
                    body
                )


                insert_notification_history(
                    row["id"],
                    notification_type
                )


                logging.info(
                    f"送信成功: {row['email']} {row['device_name']}"
                )


                print(
                    f"{row['email']} 送信成功"
                )


            except Exception as e:


                insert_failed_history(
                    row["id"],
                    notification_type,
                    e
                )


                print(
                    f"{row['email']} 送信失敗"
                )


                logging.error(
                    f"送信失敗: {row['email']} {e}"
                )


if __name__ == "__main__":
    main()