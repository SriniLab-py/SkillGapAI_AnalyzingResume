"""
Advanced Skill Comparison Engine
Uses TF-IDF + Cosine Similarity from your Milestone 3
Plus set-based operations for comprehensive analysis
"""

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from typing import Dict, List

def compare_skills_advanced(resume_skills: Dict[str, Dict[str, int]], 
                           jd_skills: Dict[str, Dict[str, int]]) -> Dict:
    """
    Advanced skill comparison using TF-IDF + Cosine Similarity
    Plus traditional set-based comparison
    
    Args:
        resume_skills: {category: {skill: confidence}}
        jd_skills: {category: {skill: confidence}}
    
    Returns:
        dict: Comprehensive comparison results
    """
    
    # Flatten skills for comparison
    resume_skills_flat = {}
    jd_skills_flat = {}
    
    for category, skills in resume_skills.items():
        for skill, conf in skills.items():
            resume_skills_flat[skill.lower()] = {
                'category': category,
                'confidence': conf
            }
    
    for category, skills in jd_skills.items():
        for skill, conf in skills.items():
            jd_skills_flat[skill.lower()] = {
                'category': category,
                'confidence': conf
            }
    
    resume_skill_list = list(resume_skills_flat.keys())
    jd_skill_list = list(jd_skills_flat.keys())
    
    # ========================================
    # Method 1: TF-IDF + Cosine Similarity
    # ========================================
    matched_skills = []
    partial_skills = []
    missing_skills = []
    extra_skills = []
    similarity_scores = {}
    
    if resume_skill_list and jd_skill_list:
        all_skills = resume_skill_list + jd_skill_list
        
        # Create TF-IDF vectors
        vectorizer = TfidfVectorizer(token_pattern=r"(?u)\b\w+\b")
        try:
            skill_vectors = vectorizer.fit_transform(all_skills)
            
            resume_vectors = skill_vectors[:len(resume_skill_list)]
            jd_vectors = skill_vectors[len(resume_skill_list):]
            
            # Calculate similarity matrix
            similarity_matrix = cosine_similarity(resume_vectors, jd_vectors)
            
            # Classify each JD skill
            for jd_idx, jd_skill in enumerate(jd_skill_list):
                max_similarity = similarity_matrix[:, jd_idx].max()
                best_match_idx = similarity_matrix[:, jd_idx].argmax()
                best_resume_skill = resume_skill_list[best_match_idx]
                
                similarity_scores[jd_skill] = {
                    'similarity': max_similarity,
                    'best_match': best_resume_skill
                }
                
                # Three-tier classification (from your Milestone 3)
                if max_similarity >= 0.85:  # High similarity = Matched
                    matched_skills.append(jd_skill)
                elif max_similarity >= 0.50:  # Medium similarity = Partial
                    partial_skills.append({
                        'skill': jd_skill,
                        'similarity': max_similarity,
                        'closest_match': best_resume_skill
                    })
                else:  # Low similarity = Missing
                    missing_skills.append(jd_skill)
            
            # Find extra skills (in resume but not in JD)
            for resume_skill in resume_skill_list:
                resume_idx = resume_skill_list.index(resume_skill)
                max_similarity_to_jd = similarity_matrix[resume_idx, :].max()
                
                if max_similarity_to_jd < 0.50:
                    extra_skills.append(resume_skill)
        
        except Exception as e:
            print(f"TF-IDF comparison error: {e}")
            # Fallback to simple set comparison
            matched_skills = list(set(resume_skill_list) & set(jd_skill_list))
            missing_skills = list(set(jd_skill_list) - set(resume_skill_list))
            extra_skills = list(set(resume_skill_list) - set(jd_skill_list))
    
    # ========================================
    # Method 2: Category-wise Set Comparison
    # ========================================
    category_breakdown = {}
    
    all_categories = set(list(resume_skills.keys()) + list(jd_skills.keys()))
    
    for category in all_categories:
        resume_cat = set(s.lower() for s in resume_skills.get(category, {}).keys())
        jd_cat = set(s.lower() for s in jd_skills.get(category, {}).keys())
        
        cat_matched = resume_cat & jd_cat
        cat_missing = jd_cat - resume_cat
        cat_extra = resume_cat - jd_cat
        
        if cat_matched or cat_missing or cat_extra:
            category_breakdown[category] = {
                'matched': sorted([s.title() for s in cat_matched]),
                'missing': sorted([s.title() for s in cat_missing]),
                'extra': sorted([s.title() for s in cat_extra])
            }
    
    # ========================================
    # Calculate Overall Match Percentage
    # ========================================
    total_jd_skills = len(jd_skill_list)
    total_matched = len(matched_skills)
    total_partial = len(partial_skills)
    
    if total_jd_skills > 0:
        # Weighted match: full credit for matches, half credit for partials
        weighted_match = total_matched + (total_partial * 0.5)
        overall_match = (weighted_match / total_jd_skills) * 100
    else:
        overall_match = 0
    
    # ========================================
    # Skill Confidence Mapping
    # ========================================
    skill_confidences = {}
    for skill in matched_skills:
        if skill in resume_skills_flat:
            skill_confidences[skill.title()] = resume_skills_flat[skill]['confidence']
    
    # ========================================
    # Priority Classification for Missing Skills
    # ========================================
    missing_with_priority = []
    for skill in missing_skills:
        if skill in jd_skills_flat:
            jd_conf = jd_skills_flat[skill]['confidence']
            
            if jd_conf >= 90:
                priority = 'Critical'
            elif jd_conf >= 75:
                priority = 'High'
            else:
                priority = 'Medium'
            
            missing_with_priority.append({
                'skill': skill.title(),
                'priority': priority,
                'jd_confidence': jd_conf
            })
    
    # Sort by priority
    priority_order = {'Critical': 0, 'High': 1, 'Medium': 2}
    missing_with_priority.sort(key=lambda x: priority_order[x['priority']])
    
    # ========================================
    # Gap Analysis Score (from your Milestone 4)
    # ========================================
    if matched_skills or missing_skills:
        gap_percentages = []
        for skill in matched_skills:
            # No gap for matched skills
            gap_percentages.append(0)
        
        for skill_data in missing_with_priority:
            # Gap based on JD confidence
            gap_percentages.append(skill_data['jd_confidence'])
        
        avg_gap = sum(gap_percentages) / len(gap_percentages) if gap_percentages else 0
    else:
        avg_gap = 0
    
    # ========================================
    # Return Comprehensive Results
    # ========================================
    return {
        # Core metrics
        'overall_match': overall_match,
        'avg_gap': avg_gap,
        'total_jd_skills': total_jd_skills,
        'total_matched': total_matched,
        'total_partial': total_partial,
        'total_missing': len(missing_skills),
        'total_extra': len(extra_skills),
        
        # Skill lists (title-cased for display)
        'matched_skills': sorted([s.title() for s in matched_skills]),
        'partial_skills': partial_skills,  # List of dicts with similarity scores
        'missing_skills': sorted([s.title() for s in missing_skills]),
        'extra_skills': sorted([s.title() for s in extra_skills]),
        
        # Advanced data
        'missing_with_priority': missing_with_priority,
        'similarity_scores': similarity_scores,
        'category_breakdown': category_breakdown,
        'skill_confidences': skill_confidences,
        
        # Classification message
        'classification': get_classification_message(overall_match)
    }

def get_classification_message(match_percentage: float) -> str:
    """
    Get classification message based on match percentage
    
    Args:
        match_percentage (float): Overall match percentage
    
    Returns:
        str: Classification message
    """
    if match_percentage >= 90:
        return "🌟 Excellent Match - You're a perfect fit for this role!"
    elif match_percentage >= 75:
        return "✅ Strong Match - You have most required skills!"
    elif match_percentage >= 60:
        return "⚡ Good Match - Focus on key missing skills to improve."
    elif match_percentage >= 40:
        return "⚠️ Moderate Match - Significant upskilling needed."
    else:
        return "❌ Low Match - Consider gaining foundational skills first."

def get_learning_path_suggestion(missing_skills: List[Dict]) -> List[str]:
    """
    Suggest learning path based on skill dependencies
    
    Args:
        missing_skills: List of missing skills with priority
    
    Returns:
        list: Ordered learning path
    """
    # Simple dependency mapping
    dependencies = {
        'deep learning': ['python', 'machine learning'],
        'tensorflow': ['python', 'machine learning'],
        'pytorch': ['python', 'machine learning'],
        'react': ['javascript', 'html', 'css'],
        'angular': ['javascript', 'typescript', 'html', 'css'],
        'kubernetes': ['docker'],
        'terraform': ['cloud computing', 'devops'],
    }
    
    learning_path = []
    added = set()
    
    def add_with_deps(skill_name):
        skill_lower = skill_name.lower()
        if skill_lower in added:
            return
        
        # Add dependencies first
        if skill_lower in dependencies:
            for dep in dependencies[skill_lower]:
                add_with_deps(dep)
        
        learning_path.append(skill_name.title())
        added.add(skill_lower)
    
    # Add skills in priority order
    for skill_data in sorted(missing_skills, key=lambda x: x['priority']):
        add_with_deps(skill_data['skill'])
    
    return learning_path

def compare_skill_levels(resume_skill_conf: int, jd_skill_conf: int) -> str:
    """
    Compare skill proficiency levels
    
    Args:
        resume_skill_conf (int): Resume confidence score
        jd_skill_conf (int): JD required confidence score
    
    Returns:
        str: Comparison message
    """
    diff = resume_skill_conf - jd_skill_conf
    
    if diff >= 10:
        return "Exceeds requirement"
    elif diff >= 0:
        return "Meets requirement"
    elif diff >= -10:
        return "Close to requirement"
    else:
        return "Below requirement"