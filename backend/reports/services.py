"""
Report Generation Service
"""
import os
import json
import io
from datetime import datetime
from django.conf import settings
from django.core.files.base import ContentFile
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.barcharts import VerticalBarChart
import logging

logger = logging.getLogger(__name__)

class ReportService:
    """
    Service for generating reports
    """
    
    @staticmethod
    def generate_pdf_report(report_data):
        """
        Generate PDF report from data
        """
        buffer = io.BytesIO()
        
        # Create PDF document
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72,
        )
        
        # Styles
        styles = getSampleStyleSheet()
        
        # Custom styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#0a0a0a'),
            alignment=TA_CENTER,
            spaceAfter=30,
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#1a1a2e'),
            spaceBefore=20,
            spaceAfter=10,
        )
        
        body_style = ParagraphStyle(
            'CustomBody',
            parent=styles['Normal'],
            fontSize=11,
            textColor=colors.HexColor('#333333'),
            spaceAfter=6,
        )
        
        # Build content
        story = []
        
        # Title
        story.append(Paragraph(f"AI Code Review Report", title_style))
        story.append(Spacer(1, 0.2 * inch))
        
        # Report Info
        story.append(Paragraph(f"<b>Generated:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", body_style))
        story.append(Paragraph(f"<b>User:</b> {report_data.get('username', 'N/A')}", body_style))
        story.append(Paragraph(f"<b>Submission:</b> {report_data.get('submission_title', 'N/A')}", body_style))
        story.append(Spacer(1, 0.3 * inch))
        
        # Quality Score
        quality_score = report_data.get('quality_score', 0)
        story.append(Paragraph(f"<b>Quality Score:</b> {quality_score}%", heading_style))
        story.append(Spacer(1, 0.1 * inch))
        
        # Summary Stats
        stats = report_data.get('stats', {})
        data = [
            ['Metric', 'Count'],
            ['Total Bugs', str(stats.get('bug_count', 0))],
            ['Issues', str(stats.get('issue_count', 0))],
            ['Suggestions', str(stats.get('suggestion_count', 0))],
        ]
        
        table = Table(data, colWidths=[2 * inch, 2 * inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (1, 0), colors.HexColor('#64ffda')),
            ('TEXTCOLOR', (0, 0), (1, 0), colors.HexColor('#000000')),
            ('ALIGN', (0, 0), (1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (1, 0), 12),
            ('BACKGROUND', (0, 1), (1, -1), colors.HexColor('#f5f5f5')),
            ('GRID', (0, 0), (1, -1), 1, colors.HexColor('#dddddd')),
        ]))
        story.append(table)
        story.append(Spacer(1, 0.3 * inch))
        
        # Bugs Section
        bugs = report_data.get('bugs', [])
        if bugs:
            story.append(Paragraph("Bugs Found", heading_style))
            for bug in bugs:
                severity_color = {
                    'low': colors.HexColor('#4caf50'),
                    'medium': colors.HexColor('#ff9800'),
                    'high': colors.HexColor('#f44336'),
                    'critical': colors.HexColor('#d32f2f'),
                }.get(bug.get('severity', 'low'), colors.HexColor('#4caf50'))
                
                story.append(Paragraph(f"<b>Line {bug.get('line', 'N/A')}</b> - <font color='{severity_color}'>{bug.get('severity', '').upper()}</font>", body_style))
                story.append(Paragraph(f"<i>{bug.get('description', '')}</i>", body_style))
                if bug.get('suggestion'):
                    story.append(Paragraph(f"Suggestion: {bug.get('suggestion', '')}", body_style))
                story.append(Spacer(1, 0.1 * inch))
        
        # Suggestions Section
        suggestions = report_data.get('suggestions', [])
        if suggestions:
            story.append(Paragraph("Suggestions", heading_style))
            for suggestion in suggestions:
                story.append(Paragraph(f"<b>{suggestion.get('description', '')}</b>", body_style))
                if suggestion.get('recommendation'):
                    story.append(Paragraph(f"<i>Recommendation: {suggestion.get('recommendation', '')}</i>", body_style))
                if suggestion.get('code_example'):
                    story.append(Paragraph(f"<i>Example: {suggestion.get('code_example', '')}</i>", body_style))
                story.append(Spacer(1, 0.1 * inch))
        
        # Explanation Section
        if report_data.get('explanation'):
            story.append(Paragraph("Code Explanation", heading_style))
            story.append(Paragraph(report_data.get('explanation', ''), body_style))
            story.append(Spacer(1, 0.1 * inch))
        
        # Test Cases Section
        test_cases = report_data.get('test_cases', [])
        if test_cases:
            story.append(Paragraph("Test Cases", heading_style))
            for test_case in test_cases:
                story.append(Paragraph(f"<b>{test_case.get('name', 'Test Case')}</b>", body_style))
                story.append(Paragraph(f"Input: {test_case.get('input', 'N/A')}", body_style))
                story.append(Paragraph(f"Expected: {test_case.get('expected', 'N/A')}", body_style))
                story.append(Paragraph(f"Description: {test_case.get('description', '')}", body_style))
                story.append(Spacer(1, 0.1 * inch))
        
        # Build PDF
        doc.build(story)
        buffer.seek(0)
        
        return buffer

    @staticmethod
    def generate_html_report(report_data):
        """
        Generate HTML report from data
        """
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>AI Code Review Report</title>
            <style>
                body {{ font-family: Arial, sans-serif; padding: 40px; background: #f5f5f5; }}
                .container {{ max-width: 900px; margin: 0 auto; background: white; padding: 40px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
                h1 {{ color: #1a1a2e; text-align: center; border-bottom: 3px solid #64ffda; padding-bottom: 20px; }}
                .header {{ text-align: center; margin-bottom: 30px; }}
                .meta {{ color: #666; font-size: 14px; }}
                .section {{ margin: 30px 0; }}
                .section-title {{ color: #1a1a2e; border-left: 4px solid #64ffda; padding-left: 15px; }}
                .score {{ font-size: 48px; text-align: center; color: #64ffda; font-weight: bold; }}
                .stats-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin: 20px 0; }}
                .stat-box {{ background: #f8f9fa; padding: 20px; border-radius: 8px; text-align: center; }}
                .stat-value {{ font-size: 28px; font-weight: bold; color: #1a1a2e; }}
                .bug-item {{ background: #fff5f5; padding: 15px; border-radius: 8px; margin: 10px 0; border-left: 4px solid #ff6b6b; }}
                .suggestion-item {{ background: #f0f9ff; padding: 15px; border-radius: 8px; margin: 10px 0; border-left: 4px solid #4ecdc4; }}
                .test-case {{ background: #f8f9fa; padding: 15px; border-radius: 8px; margin: 10px 0; }}
                .severity-low {{ color: #4caf50; }}
                .severity-medium {{ color: #ff9800; }}
                .severity-high {{ color: #f44336; }}
                .severity-critical {{ color: #d32f2f; }}
                .footer {{ text-align: center; margin-top: 40px; color: #999; font-size: 12px; border-top: 1px solid #eee; padding-top: 20px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🤖 AI Code Review Report</h1>
                <div class="header">
                    <div class="meta">Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</div>
                    <div class="meta">User: {report_data.get('username', 'N/A')}</div>
                    <div class="meta">Submission: {report_data.get('submission_title', 'N/A')}</div>
                </div>
                
                <div class="section">
                    <div class="score">{report_data.get('quality_score', 0)}%</div>
                    <p style="text-align:center;">Quality Score</p>
                </div>
                
                <div class="stats-grid">
                    <div class="stat-box">
                        <div class="stat-value">{report_data.get('stats', {}).get('bug_count', 0)}</div>
                        <div>Total Bugs</div>
                    </div>
                    <div class="stat-box">
                        <div class="stat-value">{report_data.get('stats', {}).get('issue_count', 0)}</div>
                        <div>Issues</div>
                    </div>
                    <div class="stat-box">
                        <div class="stat-value">{report_data.get('stats', {}).get('suggestion_count', 0)}</div>
                        <div>Suggestions</div>
                    </div>
                </div>
        """
        
        # Bugs
        bugs = report_data.get('bugs', [])
        if bugs:
            html += '<div class="section"><h2 class="section-title">🐛 Bugs Found</h2>'
            for bug in bugs:
                severity_class = f"severity-{bug.get('severity', 'low')}"
                html += f'''
                    <div class="bug-item">
                        <strong>Line {bug.get('line', 'N/A')}</strong> 
                        <span class="{severity_class}">[{bug.get('severity', '').upper()}]</span>
                        <p>{bug.get('description', '')}</p>
                        <p><em>Suggestion: {bug.get('suggestion', 'N/A')}</em></p>
                    </div>
                '''
            html += '</div>'
        
        # Suggestions
        suggestions = report_data.get('suggestions', [])
        if suggestions:
            html += '<div class="section"><h2 class="section-title">💡 Suggestions</h2>'
            for suggestion in suggestions:
                html += f'''
                    <div class="suggestion-item">
                        <strong>{suggestion.get('description', '')}</strong>
                        <p><em>Recommendation: {suggestion.get('recommendation', 'N/A')}</em></p>
                        {f'<p><code>{suggestion.get("code_example", "")}</code></p>' if suggestion.get('code_example') else ''}
                    </div>
                '''
            html += '</div>'
        
        # Explanation
        if report_data.get('explanation'):
            html += f'''
                <div class="section">
                    <h2 class="section-title">📖 Code Explanation</h2>
                    <p style="line-height:1.6;">{report_data.get('explanation', '')}</p>
                </div>
            '''
        
        # Test Cases
        test_cases = report_data.get('test_cases', [])
        if test_cases:
            html += '<div class="section"><h2 class="section-title">🧪 Test Cases</h2>'
            for test_case in test_cases:
                html += f'''
                    <div class="test-case">
                        <strong>{test_case.get('name', 'Test Case')}</strong>
                        <p><strong>Input:</strong> {test_case.get('input', 'N/A')}</p>
                        <p><strong>Expected:</strong> {test_case.get('expected', 'N/A')}</p>
                        <p><em>{test_case.get('description', '')}</em></p>
                    </div>
                '''
            html += '</div>'
        
        html += '''
                <div class="footer">
                    Generated by AI Code Review Platform © 2026
                </div>
            </div>
        </body>
        </html>
        '''
        
        return html

    @staticmethod
    def generate_report(report_data, format='pdf'):
        """
        Generate report in specified format
        """
        if format == 'pdf':
            return ReportService.generate_pdf_report(report_data)
        elif format == 'html':
            return ReportService.generate_html_report(report_data)
        else:
            raise ValueError(f"Unsupported format: {format}")