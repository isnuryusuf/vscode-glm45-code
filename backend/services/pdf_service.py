import os
from datetime import datetime
from typing import List, Dict, Any
from jinja2 import Template
import weasyprint
from models import User, Item
from sqlalchemy.orm import Session
from database import get_db

class PDFReportService:
    def __init__(self):
        self.template_dir = os.path.join(os.path.dirname(__file__), '..', 'templates')
        self.ensure_template_dir()
    
    def ensure_template_dir(self):
        """Create templates directory if it doesn't exist"""
        if not os.path.exists(self.template_dir):
            os.makedirs(self.template_dir)
    
    def generate_users_report(self, users: List[User]) -> bytes:
        """Generate PDF report for users"""
        template_str = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Users Report</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        .header { text-align: center; margin-bottom: 30px; }
        .title { color: #2c3e50; font-size: 24px; margin-bottom: 10px; }
        .subtitle { color: #7f8c8d; font-size: 14px; margin-bottom: 20px; }
        table { width: 100%; border-collapse: collapse; margin-top: 20px; }
        th, td { border: 1px solid #ddd; padding: 12px; text-align: left; }
        th { background-color: #f8f9fa; font-weight: bold; color: #2c3e50; }
        tr:nth-child(even) { background-color: #f8f9fa; }
        .status-active { color: #28a745; font-weight: bold; }
        .status-inactive { color: #dc3545; font-weight: bold; }
        .footer { text-align: center; margin-top: 30px; font-size: 12px; color: #7f8c8d; }
    </style>
</head>
<body>
    <div class="header">
        <div class="title">Users Report</div>
        <div class="subtitle">Generated on {{ generation_date }}</div>
        <div class="subtitle">Total Users: {{ total_users }}</div>
    </div>
    
    <table>
        <thead>
            <tr>
                <th>ID</th>
                <th>Username</th>
                <th>Email</th>
                <th>Status</th>
                <th>Created At</th>
            </tr>
        </thead>
        <tbody>
            {% for user in users %}
            <tr>
                <td>{{ user.id }}</td>
                <td>{{ user.username }}</td>
                <td>{{ user.email }}</td>
                <td class="{% if user.is_active %}status-active{% else %}status-inactive{% endif %}">
                    {{ 'Active' if user.is_active else 'Inactive' }}
                </td>
                <td>{{ user.created_at.strftime('%Y-%m-%d %H:%M:%S') }}</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
    
    <div class="footer">
        FastAPI Vue Boilerplate - Users Report
    </div>
</body>
</html>
        """
        
        template = Template(template_str)
        html_content = template.render(
            users=users,
            total_users=len(users),
            generation_date=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        )
        
        return weasyprint.HTML(string=html_content).write_pdf()
    
    def generate_items_report(self, items: List[Item]) -> bytes:
        """Generate PDF report for items"""
        template_str = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Items Report</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        .header { text-align: center; margin-bottom: 30px; }
        .title { color: #2c3e50; font-size: 24px; margin-bottom: 10px; }
        .subtitle { color: #7f8c8d; font-size: 14px; margin-bottom: 20px; }
        .stats { display: flex; justify-content: space-around; margin: 20px 0; }
        .stat-box { text-align: center; padding: 15px; background-color: #f8f9fa; border-radius: 8px; min-width: 120px; }
        .stat-number { font-size: 24px; font-weight: bold; color: #42b983; }
        .stat-label { font-size: 12px; color: #7f8c8d; margin-top: 5px; }
        table { width: 100%; border-collapse: collapse; margin-top: 20px; }
        th, td { border: 1px solid #ddd; padding: 12px; text-align: left; }
        th { background-color: #f8f9fa; font-weight: bold; color: #2c3e50; }
        tr:nth-child(even) { background-color: #f8f9fa; }
        .status-completed { color: #28a745; font-weight: bold; }
        .status-pending { color: #ffc107; font-weight: bold; }
        .description { max-width: 300px; word-wrap: break-word; }
        .footer { text-align: center; margin-top: 30px; font-size: 12px; color: #7f8c8d; }
    </style>
</head>
<body>
    <div class="header">
        <div class="title">Items Report</div>
        <div class="subtitle">Generated on {{ generation_date }}</div>
    </div>
    
    <div class="stats">
        <div class="stat-box">
            <div class="stat-number">{{ total_items }}</div>
            <div class="stat-label">Total Items</div>
        </div>
        <div class="stat-box">
            <div class="stat-number">{{ completed_items }}</div>
            <div class="stat-label">Completed</div>
        </div>
        <div class="stat-box">
            <div class="stat-number">{{ pending_items }}</div>
            <div class="stat-label">Pending</div>
        </div>
    </div>
    
    <table>
        <thead>
            <tr>
                <th>ID</th>
                <th>Title</th>
                <th>Description</th>
                <th>Status</th>
                <th>Owner ID</th>
                <th>Created At</th>
            </tr>
        </thead>
        <tbody>
            {% for item in items %}
            <tr>
                <td>{{ item.id }}</td>
                <td>{{ item.title }}</td>
                <td class="description">{{ item.description or 'No description' }}</td>
                <td class="{% if item.completed %}status-completed{% else %}status-pending{% endif %}">
                    {{ 'Completed' if item.completed else 'Pending' }}
                </td>
                <td>{{ item.owner_id }}</td>
                <td>{{ item.created_at.strftime('%Y-%m-%d %H:%M:%S') }}</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
    
    <div class="footer">
        FastAPI Vue Boilerplate - Items Report
    </div>
</body>
</html>
        """
        
        completed_count = sum(1 for item in items if item.completed)
        pending_count = len(items) - completed_count
        
        template = Template(template_str)
        html_content = template.render(
            items=items,
            total_items=len(items),
            completed_items=completed_count,
            pending_items=pending_count,
            generation_date=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        )
        
        return weasyprint.HTML(string=html_content).write_pdf()
    
    def generate_comprehensive_report(self, users: List[User], items: List[Item]) -> bytes:
        """Generate comprehensive PDF report with both users and items"""
        template_str = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Comprehensive Report</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        .header { text-align: center; margin-bottom: 30px; }
        .title { color: #2c3e50; font-size: 28px; margin-bottom: 10px; }
        .subtitle { color: #7f8c8d; font-size: 14px; margin-bottom: 20px; }
        .section { margin-bottom: 40px; }
        .section-title { color: #42b983; font-size: 20px; margin-bottom: 15px; border-bottom: 2px solid #42b983; padding-bottom: 5px; }
        .stats { display: flex; justify-content: space-around; margin: 20px 0; }
        .stat-box { text-align: center; padding: 15px; background-color: #f8f9fa; border-radius: 8px; min-width: 120px; }
        .stat-number { font-size: 24px; font-weight: bold; color: #42b983; }
        .stat-label { font-size: 12px; color: #7f8c8d; margin-top: 5px; }
        table { width: 100%; border-collapse: collapse; margin-top: 20px; }
        th, td { border: 1px solid #ddd; padding: 12px; text-align: left; }
        th { background-color: #f8f9fa; font-weight: bold; color: #2c3e50; }
        tr:nth-child(even) { background-color: #f8f9fa; }
        .status-active { color: #28a745; font-weight: bold; }
        .status-inactive { color: #dc3545; font-weight: bold; }
        .status-completed { color: #28a745; font-weight: bold; }
        .status-pending { color: #ffc107; font-weight: bold; }
        .description { max-width: 300px; word-wrap: break-word; }
        .footer { text-align: center; margin-top: 30px; font-size: 12px; color: #7f8c8d; }
        .page-break { page-break-before: always; }
    </style>
</head>
<body>
    <div class="header">
        <div class="title">Comprehensive System Report</div>
        <div class="subtitle">Generated on {{ generation_date }}</div>
    </div>
    
    <div class="stats">
        <div class="stat-box">
            <div class="stat-number">{{ total_users }}</div>
            <div class="stat-label">Total Users</div>
        </div>
        <div class="stat-box">
            <div class="stat-number">{{ active_users }}</div>
            <div class="stat-label">Active Users</div>
        </div>
        <div class="stat-box">
            <div class="stat-number">{{ total_items }}</div>
            <div class="stat-label">Total Items</div>
        </div>
        <div class="stat-box">
            <div class="stat-number">{{ completed_items }}</div>
            <div class="stat-label">Completed Items</div>
        </div>
    </div>
    
    <div class="section">
        <div class="section-title">Users Overview</div>
        <table>
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Username</th>
                    <th>Email</th>
                    <th>Status</th>
                    <th>Created At</th>
                </tr>
            </thead>
            <tbody>
                {% for user in users %}
                <tr>
                    <td>{{ user.id }}</td>
                    <td>{{ user.username }}</td>
                    <td>{{ user.email }}</td>
                    <td class="{% if user.is_active %}status-active{% else %}status-inactive{% endif %}">
                        {{ 'Active' if user.is_active else 'Inactive' }}
                    </td>
                    <td>{{ user.created_at.strftime('%Y-%m-%d %H:%M:%S') }}</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>
    
    <div class="page-break"></div>
    
    <div class="section">
        <div class="section-title">Items Overview</div>
        <table>
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Title</th>
                    <th>Description</th>
                    <th>Status</th>
                    <th>Owner ID</th>
                    <th>Created At</th>
                </tr>
            </thead>
            <tbody>
                {% for item in items %}
                <tr>
                    <td>{{ item.id }}</td>
                    <td>{{ item.title }}</td>
                    <td class="description">{{ item.description or 'No description' }}</td>
                    <td class="{% if item.completed %}status-completed{% else %}status-pending{% endif %}">
                        {{ 'Completed' if item.completed else 'Pending' }}
                    </td>
                    <td>{{ item.owner_id }}</td>
                    <td>{{ item.created_at.strftime('%Y-%m-%d %H:%M:%S') }}</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>
    
    <div class="footer">
        FastAPI Vue Boilerplate - Comprehensive System Report
    </div>
</body>
</html>
        """
        
        active_users = sum(1 for user in users if user.is_active)
        completed_items = sum(1 for item in items if item.completed)
        
        template = Template(template_str)
        html_content = template.render(
            users=users,
            items=items,
            total_users=len(users),
            active_users=active_users,
            total_items=len(items),
            completed_items=completed_items,
            generation_date=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        )
        
        return weasyprint.HTML(string=html_content).write_pdf()

# Global instance
pdf_service = PDFReportService()