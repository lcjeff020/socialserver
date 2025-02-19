from typing import List
from fastapi_mail import FastMail, MessageSchema
from app.core.config import settings
from app.services.analytics_service import AnalyticsService

class ReportService:
    def __init__(self):
        self.analytics = AnalyticsService()
        self.mail = FastMail(settings.MAIL_CONFIG)
        
    async def send_weekly_report(self, user_id: int, team_id: int):
        """发送每周报告"""
        analytics_data = await self.analytics.get_team_analytics(team_id)
        
        # 生成报告内容
        report_content = self._generate_report_html(analytics_data)
        
        # 发送邮件
        message = MessageSchema(
            subject="Your Weekly Social Media Report",
            recipients=[user.email],
            body=report_content,
            subtype="html"
        )
        
        await self.mail.send_message(message) 