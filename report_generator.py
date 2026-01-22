"""
Advanced Report Generation Module
Generates comprehensive PDF and CSV reports
"""

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.piecharts import Pie
import csv
from datetime import datetime
import os

def generate_advanced_pdf_report(user_name: str, user_email: str, 
                                comparison: dict, recommendations: dict) -> str:
    """
    Generate comprehensive PDF report with visualizations
    
    Args:
        user_name: User's name
        user_email: User's email
        comparison: Comparison results
        recommendations: Recommendation data
    
    Returns:
        str: Path to generated PDF
    """
    try:
        os.makedirs('reports', exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"reports/skillgap_integrated_report_{timestamp}.pdf"
        
        doc = SimpleDocTemplate(filename, pagesize=letter,
                               topMargin=0.75*inch, bottomMargin=0.75*inch)
        story = []
        styles = getSampleStyleSheet()
        
        # Custom Styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=26,
            textColor=colors.HexColor('#667eea'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#1f2937'),
            spaceAfter=12,
            spaceBefore=18,
            fontName='Helvetica-Bold'
        )
        
        subheading_style = ParagraphStyle(
            'CustomSubHeading',
            parent=styles['Heading3'],
            fontSize=13,
            textColor=colors.HexColor('#374151'),
            spaceAfter=8,
            spaceBefore=10,
            fontName='Helvetica-Bold'
        )
        
        # ===== TITLE PAGE =====
        story.append(Spacer(1, 0.5*inch))
        title = Paragraph("🎯 Skill Gap AI - Comprehensive Analysis Report", title_style)
        story.append(title)
        story.append(Spacer(1, 0.3*inch))
        
        subtitle = Paragraph(
            "<i>Advanced ML-Powered Career Analysis</i>",
            ParagraphStyle('subtitle', parent=styles['Normal'], 
                          fontSize=12, alignment=TA_CENTER, textColor=colors.grey)
        )
        story.append(subtitle)
        story.append(Spacer(1, 0.5*inch))
        
        # User Info Box
        user_data = [
            ['Report Generated:', datetime.now().strftime("%B %d, %Y at %H:%M:%S")],
            ['Candidate Name:', user_name],
            ['Email Address:', user_email],
            ['Analysis Type:', 'ML-Powered TF-IDF + Cosine Similarity']
        ]
        
        user_table = Table(user_data, colWidths=[2.2*inch, 4*inch])
        user_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e0e7ff')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
            ('TOPPADDING', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#c7d2fe')),
            ('ROWBACKGROUNDS', (1, 0), (1, -1), [colors.white, colors.HexColor('#f9fafb')])
        ]))
        story.append(user_table)
        story.append(Spacer(1, 0.4*inch))
        
        # ===== EXECUTIVE SUMMARY =====
        story.append(Paragraph("📊 Executive Summary", heading_style))
        
        summary_data = [
            ['Metric', 'Value', 'Interpretation'],
            ['Overall Match Score', f"{comparison['overall_match']:.1f}%", comparison['classification']],
            ['Matched Skills', str(comparison['total_matched']), '✅ Exact matches with job requirements'],
            ['Partial Matches', str(comparison['total_partial']), '⚡ Skills with 50-85% similarity'],
            ['Missing Skills', str(comparison['total_missing']), '❌ Skills to acquire'],
            ['Extra Skills', str(comparison['total_extra']), '💎 Bonus skills you possess'],
            ['AI Gap Score', f"{comparison['avg_gap']:.1f}%", 'Lower is better']
        ]
        
        summary_table = Table(summary_data, colWidths=[2*inch, 1.3*inch, 3*inch])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#667eea')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f9fafb')),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f3f4f6')])
        ]))
        story.append(summary_table)
        story.append(Spacer(1, 0.3*inch))
        
        # Recommendation Badge
        match_pct = comparison['overall_match']
        if match_pct >= 75:
            rec_text = "✅ <b>STRONG CANDIDATE</b> - You are well-qualified for this position!"
            rec_color = colors.HexColor('#10b981')
        elif match_pct >= 60:
            rec_text = "⚡ <b>GOOD FIT</b> - Focus on key missing skills to strengthen your candidacy."
            rec_color = colors.HexColor('#f59e0b')
        else:
            rec_text = "📚 <b>UPSKILLING NEEDED</b> - Invest time in acquiring critical skills."
            rec_color = colors.HexColor('#ef4444')
        
        rec_para = Paragraph(rec_text, ParagraphStyle('rec', parent=styles['Normal'],
                                                      fontSize=11, textColor=rec_color,
                                                      alignment=TA_CENTER, spaceAfter=20))
        story.append(rec_para)
        
        # ===== MATCHED SKILLS =====
        story.append(PageBreak())
        story.append(Paragraph("✅ Matched Skills (Exact Matches)", heading_style))
        
        if comparison['matched_skills']:
            matched_text = ", ".join(comparison['matched_skills'])
            story.append(Paragraph(matched_text, styles['Normal']))
        else:
            story.append(Paragraph("<i>No exact matches found.</i>", styles['Normal']))
        
        story.append(Spacer(1, 0.2*inch))
        
        # ===== PARTIAL MATCHES =====
        story.append(Paragraph("⚡ Partial Matches (50-85% Similarity)", heading_style))
        
        if comparison.get('partial_skills'):
            partial_data = [['JD Skill', 'Your Closest Match', 'Similarity']]
            for item in comparison['partial_skills']:
                partial_data.append([
                    item['skill'],
                    item['closest_match'].title(),
                    f"{item['similarity']*100:.0f}%"
                ])
            
            partial_table = Table(partial_data, colWidths=[2.5*inch, 2.5*inch, 1.3*inch])
            partial_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#fbbf24')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('GRID', (0, 0), (-1, -1), 1, colors.grey),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#fffbeb')])
            ]))
            story.append(partial_table)
        else:
            story.append(Paragraph("<i>No partial matches identified.</i>", styles['Normal']))
        
        story.append(Spacer(1, 0.2*inch))
        
        # ===== MISSING SKILLS =====
        story.append(Paragraph("❌ Missing Skills (Priority Focus Areas)", heading_style))
        
        if comparison.get('missing_with_priority'):
            missing_data = [['Skill', 'Priority', 'Required Proficiency']]
            for item in comparison['missing_with_priority']:
                missing_data.append([
                    item['skill'],
                    item['priority'],
                    f"{item['jd_confidence']}%"
                ])
            
            missing_table = Table(missing_data, colWidths=[3*inch, 2*inch, 1.3*inch])
            missing_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#ef4444')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('GRID', (0, 0), (-1, -1), 1, colors.grey),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#fef2f2')])
            ]))
            story.append(missing_table)
        else:
            story.append(Paragraph("🎉 <b>Excellent! You possess all required skills!</b>", 
                                  ParagraphStyle('success', parent=styles['Normal'], 
                                               textColor=colors.HexColor('#10b981'))))
        
        # ===== RECOMMENDATIONS =====
        if recommendations:
            story.append(PageBreak())
            story.append(Paragraph("🎓 Personalized Learning Recommendations", heading_style))
            
            for skill, rec_data in recommendations.items():
                story.append(Paragraph(f"<b>{skill}</b>", subheading_style))
                
                # Priority badge
                priority = rec_data['priority']
                action = rec_data['action']
                story.append(Paragraph(f"<i>Priority: {priority}</i> • {action}", styles['Normal']))
                story.append(Spacer(1, 0.1*inch))
                
                # Courses
                story.append(Paragraph("<b>Recommended Courses:</b>", styles['Normal']))
                for i, course in enumerate(rec_data['courses'], 1):
                    course_text = f"{i}. <b>{course['title']}</b> ({course['platform']})<br/><font color='blue'>{course['url']}</font>"
                    story.append(Paragraph(course_text, ParagraphStyle('course', parent=styles['Normal'], 
                                                                      fontSize=9, leftIndent=20)))
                
                story.append(Spacer(1, 0.15*inch))
        
        # ===== FOOTER =====
        story.append(PageBreak())
        story.append(Spacer(1, 2*inch))
        footer_text = """
        <para align=center>
        <b>Skill Gap AI - Integrated Edition</b><br/>
        Powered by Advanced ML Algorithms (TF-IDF + Cosine Similarity)<br/>
        © 2024 Skill Gap AI | Developed with ❤️ by AI Engineers<br/>
        <i>This report is AI-generated and should be used as a guide for career development.</i>
        </para>
        """
        story.append(Paragraph(footer_text, styles['Normal']))
        
        # Build PDF
        doc.build(story)
        return filename
        
    except Exception as e:
        print(f"PDF generation error: {e}")
        return None

def generate_csv_report(comparison: dict) -> str:
    """
    Generate CSV data export
    
    Args:
        comparison: Comparison results
    
    Returns:
        str: Path to CSV file
    """
    try:
        os.makedirs('reports', exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"reports/skillgap_data_{timestamp}.csv"
        
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            
            # Header
            writer.writerow(['Skill Gap Analysis Data Export'])
            writer.writerow(['Generated:', datetime.now().strftime("%Y-%m-%d %H:%M:%S")])
            writer.writerow([])
            
            # Summary
            writer.writerow(['SUMMARY METRICS'])
            writer.writerow(['Metric', 'Value'])
            writer.writerow(['Overall Match', f"{comparison['overall_match']:.1f}%"])
            writer.writerow(['Matched Skills', comparison['total_matched']])
            writer.writerow(['Partial Matches', comparison['total_partial']])
            writer.writerow(['Missing Skills', comparison['total_missing']])
            writer.writerow(['Extra Skills', comparison['total_extra']])
            writer.writerow([])
            
            # Matched Skills
            writer.writerow(['MATCHED SKILLS'])
            for skill in comparison['matched_skills']:
                writer.writerow([skill])
            writer.writerow([])
            
            # Missing Skills
            writer.writerow(['MISSING SKILLS'])
            writer.writerow(['Skill', 'Priority', 'Required Confidence'])
            for item in comparison.get('missing_with_priority', []):
                writer.writerow([item['skill'], item['priority'], f"{item['jd_confidence']}%"])
            writer.writerow([])
            
            # Partial Skills
            writer.writerow(['PARTIAL MATCHES'])
            writer.writerow(['JD Skill', 'Your Match', 'Similarity'])
            for item in comparison.get('partial_skills', []):
                writer.writerow([
                    item['skill'], 
                    item['closest_match'].title(), 
                    f"{item['similarity']*100:.0f}%"
                ])
            
        return filename
        
    except Exception as e:
        print(f"CSV generation error: {e}")
        return None