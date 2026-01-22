"""
Integrated Visualization Module
Combines Plotly interactive charts with Matplotlib radar charts
Best of both implementations
"""

import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
from typing import Dict, List

def create_integrated_visualizations(comparison: Dict, 
                                     resume_skills: Dict, 
                                     jd_skills: Dict):
    """
    Create comprehensive visualization dashboard
    Combines Plotly interactive charts + Matplotlib radar chart
    
    Args:
        comparison: Comparison results from comparator
        resume_skills: Resume skills with confidence
        jd_skills: JD skills with confidence
    """
    
    # ============================================
    # ROW 1: Gauge Chart + Similarity Heatmap
    # ============================================
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🎯 Overall Match Score")
        
        # Plotly Gauge Chart (Interactive)
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=comparison['overall_match'],
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Match Percentage", 'font': {'size': 20}},
            delta={'reference': 70, 'increasing': {'color': "#10b981"}},
            gauge={
                'axis': {'range': [None, 100], 'tickwidth': 1},
                'bar': {'color': "#3b82f6"},
                'bgcolor': "rgba(255,255,255,0.1)",
                'borderwidth': 2,
                'bordercolor': "rgba(148,163,184,0.3)",
                'steps': [
                    {'range': [0, 40], 'color': 'rgba(239, 68, 68, 0.3)'},
                    {'range': [40, 70], 'color': 'rgba(251, 191, 36, 0.3)'},
                    {'range': [70, 100], 'color': 'rgba(34, 197, 94, 0.3)'}
                ],
                'threshold': {
                    'line': {'color': "white", 'width': 3},
                    'thickness': 0.75,
                    'value': 75
                }
            }
        ))
        
        fig_gauge.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font={'color': 'white'},
            height=300
        )
        
        st.plotly_chart(fig_gauge, use_container_width=True)
    
    with col2:
        st.markdown("#### 🔥 Skill Similarity Heatmap")
        
        # Get similarity scores for heatmap
        if comparison.get('similarity_scores'):
            skills_list = []
            similarities = []
            
            for jd_skill, data in comparison['similarity_scores'].items():
                skills_list.append(jd_skill.title())
                similarities.append(data['similarity'] * 100)
            
            # Matplotlib heatmap (from your Milestone 3)
            fig, ax = plt.subplots(figsize=(8, 6))
            fig.patch.set_facecolor('#020617')
            ax.set_facecolor('#0f172a')
            
            # Create matrix for heatmap
            matrix = np.array(similarities).reshape(-1, 1)
            
            im = ax.imshow(matrix.T, cmap='RdYlGn', aspect='auto', vmin=0, vmax=100)
            
            ax.set_xticks(range(len(skills_list)))
            ax.set_xticklabels(skills_list, rotation=45, ha='right', fontsize=8, color='white')
            ax.set_yticks([0])
            ax.set_yticklabels(['Similarity'], color='white')
            
            # Colorbar
            cbar = plt.colorbar(im, ax=ax)
            cbar.ax.yaxis.set_tick_params(color='white')
            plt.setp(plt.getp(cbar.ax.axes, 'yticklabels'), color='white')
            
            plt.tight_layout()
            st.pyplot(fig)
        else:
            st.info("Run similarity analysis to see heatmap")
    
    # ============================================
    # ROW 2: Pie Chart + Radar Chart
    # ============================================
    col3, col4 = st.columns(2)
    
    with col3:
        st.markdown("#### 📊 Skill Distribution")
        
        # Plotly Pie Chart
        labels = ['Matched', 'Partial', 'Missing', 'Extra']
        values = [
            comparison['total_matched'],
            comparison['total_partial'],
            comparison['total_missing'],
            comparison['total_extra']
        ]
        colors = ['#10b981', '#f59e0b', '#ef4444', '#3b82f6']
        
        # Filter out zero values
        filtered_data = [(l, v, c) for l, v, c in zip(labels, values, colors) if v > 0]
        if filtered_data:
            labels, values, colors = zip(*filtered_data)
        
        fig_pie = go.Figure(data=[go.Pie(
            labels=labels,
            values=values,
            marker=dict(colors=colors),
            hole=0.4,
            textinfo='label+percent+value',
            textposition='auto',
            hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>'
        )])
        
        fig_pie.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font={'color': 'white'},
            showlegend=True,
            height=350,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.2,
                xanchor="center",
                x=0.5
            )
        )
        
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col4:
        st.markdown("#### 🎯 Radar Comparison")
        
        # Matplotlib Radar Chart (from your Milestone 4)
        # Get top 6 skills from each
        resume_top = []
        jd_top = []
        labels_radar = []
        
        for category, skills in list(resume_skills.items())[:6]:
            if skills:
                skill_name = list(skills.keys())[0]
                labels_radar.append(skill_name[:15])  # Truncate for display
                resume_top.append(list(skills.values())[0])
                
                # Find same skill in JD or use 0
                jd_conf = 0
                for jd_cat, jd_s in jd_skills.items():
                    if skill_name in jd_s:
                        jd_conf = jd_s[skill_name]
                        break
                jd_top.append(jd_conf)
        
        if labels_radar:
            angles = np.linspace(0, 2 * np.pi, len(labels_radar), endpoint=False).tolist()
            resume_top += resume_top[:1]
            jd_top += jd_top[:1]
            angles += angles[:1]
            
            fig_radar = plt.figure(figsize=(7, 7))
            fig_radar.patch.set_facecolor('#020617')
            
            ax = plt.subplot(111, polar=True)
            ax.set_facecolor('#0f172a')
            
            ax.plot(angles, resume_top, 'o-', linewidth=2, label='Your Skills', color='#10b981')
            ax.fill(angles, resume_top, alpha=0.25, color='#10b981')
            
            ax.plot(angles, jd_top, 'o-', linewidth=2, label='Job Required', color='#3b82f6')
            ax.fill(angles, jd_top, alpha=0.25, color='#3b82f6')
            
            ax.set_xticks(angles[:-1])
            ax.set_xticklabels(labels_radar, fontsize=9, color='white')
            ax.set_ylim(0, 100)
            ax.grid(color=(148/255, 163/255, 184/255, 0.2), linestyle='--', linewidth=0.5)

            ax.tick_params(colors='white')
            
            # Set radial labels color
            ax.yaxis.label.set_color('white')
            for label in ax.get_yticklabels():
                label.set_color('white')
            
            ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1), fontsize=9, 
                     facecolor='#0f172a', edgecolor='white', labelcolor='white')
            
            plt.tight_layout()
            st.pyplot(fig_radar)
        else:
            st.info("Need more skills for radar chart")
    
    # ============================================
    # ROW 3: Category Comparison Bar Chart
    # ============================================
    st.markdown("#### 📈 Category-wise Skill Match")
    
    if comparison.get('category_breakdown'):
        categories = []
        matched_counts = []
        missing_counts = []
        extra_counts = []
        
        for cat, data in comparison['category_breakdown'].items():
            categories.append(cat)
            matched_counts.append(len(data.get('matched', [])))
            missing_counts.append(len(data.get('missing', [])))
            extra_counts.append(len(data.get('extra', [])))
        
        fig_bar = go.Figure()
        
        fig_bar.add_trace(go.Bar(
            name='Matched',
            x=categories,
            y=matched_counts,
            marker_color='#10b981',
            hovertemplate='<b>%{x}</b><br>Matched: %{y}<extra></extra>'
        ))
        
        fig_bar.add_trace(go.Bar(
            name='Missing',
            x=categories,
            y=missing_counts,
            marker_color='#ef4444',
            hovertemplate='<b>%{x}</b><br>Missing: %{y}<extra></extra>'
        ))
        
        fig_bar.add_trace(go.Bar(
            name='Extra',
            x=categories,
            y=extra_counts,
            marker_color='#3b82f6',
            hovertemplate='<b>%{x}</b><br>Extra: %{y}<extra></extra>'
        ))
        
        fig_bar.update_layout(
            barmode='group',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font={'color': 'white'},
            xaxis=dict(
                tickangle=-45,
                gridcolor='rgba(148,163,184,0.1)',
                title='Skill Category'
            ),
            yaxis=dict(
                gridcolor='rgba(148,163,184,0.1)',
                title='Number of Skills'
            ),
            height=400,
            legend=dict(
                orientation="h",
                yanchor="top",
                y=1.1,
                xanchor="center",
                x=0.5
            )
        )
        
        st.plotly_chart(fig_bar, use_container_width=True)
    
    # ============================================
    # ROW 4: Priority Missing Skills
    # ============================================
    if comparison.get('missing_with_priority'):
        st.markdown("#### 🎯 Priority Skills to Acquire")
        
        # Create priority-based chart
        skills_to_learn = []
        priorities = []
        priority_colors = []
        
        color_map = {
            'Critical': '#dc2626',
            'High': '#f59e0b',
            'Medium': '#3b82f6'
        }
        
        for item in comparison['missing_with_priority'][:10]:  # Top 10
            skills_to_learn.append(item['skill'])
            priorities.append(item['priority'])
            priority_colors.append(color_map[item['priority']])
        
        fig_priority = go.Figure(go.Bar(
            y=skills_to_learn[::-1],  # Reverse for better display
            x=[1] * len(skills_to_learn),
            orientation='h',
            marker=dict(color=priority_colors[::-1]),
            text=priorities[::-1],
            textposition='inside',
            hovertemplate='<b>%{y}</b><br>Priority: %{text}<extra></extra>'
        ))
        
        fig_priority.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font={'color': 'white'},
            xaxis=dict(
                showticklabels=False,
                showgrid=False,
                title='Focus Areas'
            ),
            yaxis=dict(
                title='Skills to Acquire',
                gridcolor='rgba(148,163,184,0.1)'
            ),
            height=max(300, len(skills_to_learn) * 40),
            showlegend=False
        )
        
        st.plotly_chart(fig_priority, use_container_width=True)
    
    # ============================================
    # ROW 5: Skill Confidence Comparison
    # ============================================
    if comparison.get('matched_skills'):
        st.markdown("#### 💪 Matched Skills Confidence Levels")
        
        matched_skills_conf = []
        conf_values = []
        
        for skill in comparison['matched_skills'][:10]:
            matched_skills_conf.append(skill)
            conf_values.append(comparison.get('skill_confidences', {}).get(skill, 85))
        
        fig_conf = go.Figure(go.Bar(
            x=matched_skills_conf,
            y=conf_values,
            marker=dict(
                color=conf_values,
                colorscale='Viridis',
                showscale=True,
                colorbar=dict(title="Confidence")
            ),
            text=[f"{v}%" for v in conf_values],
            textposition='outside',
            hovertemplate='<b>%{x}</b><br>Confidence: %{y}%<extra></extra>'
        ))
        
        fig_conf.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font={'color': 'white'},
            xaxis=dict(
                tickangle=-45,
                title='Matched Skills',
                gridcolor='rgba(148,163,184,0.1)'
            ),
            yaxis=dict(
                title='Confidence Score (%)',
                range=[0, 100],
                gridcolor='rgba(148,163,184,0.1)'
            ),
            height=400
        )
        
        st.plotly_chart(fig_conf, use_container_width=True)