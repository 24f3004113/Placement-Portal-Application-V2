import smtplib
from email.message import EmailMessage

from celery_worker import celery_app

from datetime import datetime, timedelta


@celery_app.task
def send_email(to, subject, body):

    import smtplib
    from email.message import EmailMessage

    msg = EmailMessage()

    msg["From"] = "mail@placement.com"
    msg["To"] = to
    msg["Subject"] = subject

    msg.set_content(body)

    with smtplib.SMTP("localhost", 1025) as server:
        server.send_message(msg)

    return "Email sent successfully"



@celery_app.task
def interview_reminders():

    from app import app
    from db import Interview

    with app.app_context():

        tomorrow = datetime.now().date() + timedelta(days=1)

        interviews = Interview.query.filter_by(
            interview_date=tomorrow
        ).all()

        for interview in interviews:

            application = interview.application
            student = application.student
            company = application.drive.company

            send_email.delay(
                student.user.email,
                "Interview Reminder",
                f"""Hello {student.name},

This is a reminder that you have an interview scheduled tomorrow.

Company: {company.company_name}
Position: {application.drive.job_title}
Date: {interview.interview_date.strftime("%d %b %Y")}
Time: {interview.interview_time}
Mode: {interview.interview_mode}
Link: {interview.interview_link or "N/A"}
Location: {interview.interview_location or "N/A"}
Remarks: {interview.remarks or "N/A"}

Please be prepared for your interview.

Regards,
Placement Portal"""
            )

        return f"{len(interviews)} reminder(s) queued"
    


@celery_app.task
def monthly_placement_report():

    from app import app
    from db import Company, Application, ApplicationHistory, Placement, Drive
    from sqlalchemy import func
    from datetime import datetime

    with app.app_context():

        now = datetime.now()
        month, year = now.month, now.year

        for company in Company.query.all():

            applications = (
                Application.query.join(Drive)
                .filter(
                    Drive.company_id == company.cid,
                    func.strftime("%m", Application.application_date) == f"{month:02d}",
                    func.strftime("%Y", Application.application_date) == str(year)
                ).all()
            )

            history = (
                ApplicationHistory.query.join(Application).join(Drive)
                .filter(
                    Drive.company_id == company.cid,
                    func.strftime("%m", ApplicationHistory.updated_at) == f"{month:02d}",
                    func.strftime("%Y", ApplicationHistory.updated_at) == str(year)
                ).all()
            )

            status_counts = {}

            for h in history:
                status_counts[h.status] = status_counts.get(h.status, 0) + 1

            status_text = "\n".join(
                f"{status}: {count}"
                for status, count in status_counts.items()
            ) or "No status changes"

            placements = Placement.query.filter_by(
                company_id=company.cid
            ).all()

            send_email.delay(
                company.user.email,
                "Monthly Placement Report",
                f"""Hello {company.company_name},

Monthly Placement Report - {month:02d}/{year}

Total Applications: {len(applications)}

Application Status Changes:
{status_text}

Total Placements: {len(placements)}

Regards,
Placement Portal"""
            )

        return "Monthly reports sent successfully"
    

@celery_app.task
def admin_monthly_report():

    from app import app
    from db import User, Application, ApplicationHistory, Placement
    from sqlalchemy import func
    from datetime import datetime

    with app.app_context():

        admin = User.query.filter_by(role="admin").first()

        if not admin:
            return "Admin not found"

        now = datetime.now()
        month, year = now.month, now.year

        applications = Application.query.filter(
            func.strftime("%m", Application.application_date) == f"{month:02d}",
            func.strftime("%Y", Application.application_date) == str(year)
        ).all()

        history = ApplicationHistory.query.filter(
            func.strftime("%m", ApplicationHistory.updated_at) == f"{month:02d}",
            func.strftime("%Y", ApplicationHistory.updated_at) == str(year)
        ).all()

        placements = Placement.query.all()

        status_counts = {}

        for h in history:
            status_counts[h.status] = status_counts.get(h.status, 0) + 1

        status_text = "\n".join(
            f"{status}: {count}"
            for status, count in status_counts.items()
        ) or "No status changes"

        send_email.delay(
            admin.email,
            "Monthly Placement Report",
            f"""Hello Admin,

Monthly Placement Report - {month:02d}/{year}

Total Applications: {len(applications)}
Total Placements: {len(placements)}

Application Status Changes:

{status_text}

Regards,
Placement Portal"""
        )

        return "Admin monthly report sent successfully"

@celery_app.task
def send_email_with_attachment(to, subject, body, filename):

    import smtplib
    from email.message import EmailMessage

    msg = EmailMessage()

    msg["From"] = "placement@localhost"
    msg["To"] = to
    msg["Subject"] = subject

    msg.set_content(body)

    with open(filename, "rb") as file:

        msg.add_attachment(
            file.read(),
            maintype="text",
            subtype="csv",
            filename="applications.csv"
        )

    with smtplib.SMTP("localhost", 1025) as server:
        server.send_message(msg)

    
@celery_app.task
def export_student_applications(sid):

    from app import app
    from db import Student
    import csv
    import os

    with app.app_context():

        student = Student.query.get(sid)

        if not student:
            return

        os.makedirs("exports", exist_ok=True)

        filename = f"exports/student_{sid}.csv"

        with open(filename, "w", newline="", encoding="utf-8") as file:

            writer = csv.writer(file)

            writer.writerow([
                "Application No",
                "Company",
                "Position",
                "Application Date",
                "Status"
            ])

            for a in student.applications:

                writer.writerow([
                    a.aid,
                    a.drive.company.company_name,
                    a.drive.job_title,
                    a.application_date,
                    a.status
                ])

        send_email_with_attachment.delay(
            student.user.email,
            "Application Export",
            "Your application history CSV has been generated.",
            filename
        )

        return filename