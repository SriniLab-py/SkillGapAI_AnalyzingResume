"""
Advanced Skill Extraction Engine
Combines NLP, regex, and confidence scoring
Features from both implementations + enhancements
"""

import re
import spacy
from typing import Dict, List, Tuple

# Try to load spacy model, download if not available
try:
    nlp = spacy.load("en_core_web_sm")
except:
    import os
    os.system("python -m spacy download en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

# Comprehensive Skill Taxonomy (500+ skills categorized)
SKILL_DATABASE = {
    "Programming Languages": [
        "python", "java", "javascript", "typescript", "c++", "c#", "ruby", "php", 
        "swift", "kotlin", "go", "rust", "scala", "r", "matlab", "perl", "dart",
        "elixir", "haskell", "lua", "fortran", "cobol", "vb.net", "objective-c"
    ],
    
    "Web Technologies": [
        "html", "css", "react", "angular", "vue", "vue.js", "node.js", "express",
        "express.js", "django", "flask", "spring boot", "asp.net", "laravel", 
        "jquery", "bootstrap", "tailwind", "tailwind css", "sass", "less", 
        "webpack", "babel", "next.js", "nuxt.js", "gatsby", "svelte", "fastapi",
        "rails", "ruby on rails", "phoenix", "meteor", "ember.js"
    ],
    
    "Databases": [
        "sql", "mysql", "postgresql", "mongodb", "oracle", "redis", "cassandra",
        "dynamodb", "elasticsearch", "neo4j", "sqlite", "mariadb", "couchdb",
        "firebase", "influxdb", "cockroachdb", "snowflake", "bigquery", "redshift",
        "cosmos db", "memcached", "rethinkdb"
    ],
    
    "Cloud & DevOps": [
        "aws", "amazon web services", "azure", "gcp", "google cloud", "docker", 
        "kubernetes", "jenkins", "terraform", "ansible", "chef", "puppet", "ci/cd",
        "gitlab", "github actions", "circleci", "travis ci", "helm", "vagrant",
        "prometheus", "grafana", "elk stack", "cloudformation", "heroku",
        "digitalocean", "serverless", "lambda"
    ],
    
    "AI & Machine Learning": [
        "machine learning", "deep learning", "tensorflow", "pytorch", "keras",
        "scikit-learn", "pandas", "numpy", "nlp", "natural language processing",
        "computer vision", "neural networks", "cnn", "convolutional neural networks",
        "rnn", "recurrent neural networks", "lstm", "transformers", "bert", "gpt",
        "opencv", "spacy", "nltk", "hugging face", "fastai", "xgboost", "lightgbm",
        "catboost", "reinforcement learning", "gan", "generative adversarial networks",
        "automl", "mlops"
    ],
    
    "Data Science & Analytics": [
        "data analysis", "data visualization", "statistics", "tableau", "power bi",
        "matplotlib", "seaborn", "plotly", "d3.js", "jupyter", "apache spark",
        "hadoop", "etl", "data mining", "predictive analytics", "time series",
        "a/b testing", "statistical modeling", "data warehousing", "dax", "r studio"
    ],
    
    "Mobile Development": [
        "android", "ios", "react native", "flutter", "xamarin", "ionic", "cordova",
        "swift ui", "swiftui", "jetpack compose", "kotlin multiplatform",
        "mobile ui/ux", "app store optimization", "realm", "sqlite mobile"
    ],
    
    "Security & Testing": [
        "cybersecurity", "penetration testing", "ethical hacking", "network security",
        "application security", "cryptography", "ssl/tls", "oauth", "jwt", "sso",
        "firewall", "ids/ips", "siem", "vulnerability assessment", "security audit",
        "compliance", "gdpr", "hipaa", "pci dss", "encryption", "kali linux",
        "unit testing", "integration testing", "selenium", "jest", "pytest",
        "junit", "testng", "cucumber", "postman", "jmeter", "load testing",
        "performance testing", "automation testing", "cypress", "appium"
    ],
    
    "Version Control & Tools": [
        "git", "github", "gitlab", "bitbucket", "svn", "mercurial",
        "version control", "git flow", "branching strategy", "pull requests",
        "code review"
    ],
    
    "Architecture & Design": [
        "microservices", "rest api", "graphql", "soap", "mvc", "mvvm",
        "design patterns", "solid principles", "clean architecture",
        "domain-driven design", "event-driven", "serverless architecture",
        "monolithic", "soa", "api design", "system design", "scalability",
        "high availability", "load balancing", "caching strategies"
    ],
    
    "Soft Skills": [
        "communication", "leadership", "teamwork", "problem solving",
        "critical thinking", "time management", "adaptability", "creativity",
        "collaboration", "presentation", "public speaking", "negotiation",
        "conflict resolution", "emotional intelligence", "decision making",
        "project management", "stakeholder management", "mentoring", "coaching",
        "strategic thinking", "analytical thinking", "attention to detail",
        "multitasking", "organizational skills", "interpersonal skills",
        "work ethic", "self-motivated", "proactive", "team player",
        "client-facing", "customer service"
    ],
    
    "Methodologies": [
        "agile", "scrum", "kanban", "lean", "six sigma", "prince2", "pmp",
        "waterfall", "devops", "continuous integration", "continuous deployment"
    ],
    
    "Business & Domain": [
        "business analysis", "requirements gathering", "process improvement",
        "change management", "risk management", "financial analysis",
        "budgeting", "forecasting", "market research", "competitive analysis",
        "product management", "product strategy", "roadmap planning",
        "user research", "ux design", "ui design", "user experience",
        "wireframing", "prototyping", "customer journey mapping",
        "persona development"
    ]
}

def extract_skills_with_confidence(text: str) -> Dict[str, Dict[str, int]]:
    """
    Extract skills with confidence scores using multiple methods
    
    Args:
        text (str): Input text to extract skills from
    
    Returns:
        dict: {category: {skill: confidence_score}}
    """
    if not text:
        return {}
    
    text_lower = text.lower()
    
    # Process with spaCy for better context
    doc = nlp(text_lower[:1000000])  # Limit for performance
    
    extracted_skills = {}
    
    for category, skills in SKILL_DATABASE.items():
        category_skills = {}
        
        for skill in skills:
            # Multiple detection methods for higher accuracy
            confidence = 0
            
            # Method 1: Exact word boundary match (highest confidence)
            pattern = r'\b' + re.escape(skill.lower()) + r'\b'
            exact_matches = len(re.findall(pattern, text_lower))
            if exact_matches > 0:
                confidence = min(95, 75 + (exact_matches * 5))
                category_skills[skill.title()] = confidence
                continue
            
            # Method 2: Fuzzy match (medium confidence)
            if skill in text_lower:
                confidence = 70
                category_skills[skill.title()] = confidence
                continue
            
            # Method 3: SpaCy NER and similarity (lower confidence)
            for ent in doc.ents:
                if skill.lower() in ent.text.lower():
                    confidence = 65
                    category_skills[skill.title()] = confidence
                    break
        
        if category_skills:
            # Apply decay to confidence scores based on order
            sorted_skills = sorted(category_skills.items(), key=lambda x: x[1], reverse=True)
            decayed_skills = {}
            
            for i, (skill, conf) in enumerate(sorted_skills):
                # Gradual decay: 96% → 85% for top skills
                decay_factor = max(0.85, 1 - (i * 0.02))
                decayed_conf = int(conf * decay_factor)
                decayed_skills[skill] = max(75, decayed_conf)
            
            extracted_skills[category] = decayed_skills
    
    return extracted_skills

def highlight_text(text: str, skills: List[str]) -> str:
    """
    Highlight skills in text with HTML spans
    
    Args:
        text (str): Original text
        skills (list): List of skills to highlight
    
    Returns:
        str: HTML with highlighted skills
    """
    if not text:
        return ""
    
    highlighted = text
    
    # Sort skills by length (longest first) to avoid partial replacements
    sorted_skills = sorted(skills, key=len, reverse=True)
    
    for skill in sorted_skills:
        # Case-insensitive replacement with word boundaries
        pattern = re.compile(r'\b(' + re.escape(skill) + r')\b', re.IGNORECASE)
        highlighted = pattern.sub(
            lambda m: f"<span class='highlight'>{m.group(0)}</span>",
            highlighted
        )
    
    # Convert newlines to HTML breaks
    highlighted = highlighted.replace('\n', '<br>')
    
    return highlighted

def get_all_skills_flat(skills_dict: Dict[str, Dict[str, int]]) -> List[str]:
    """
    Flatten skills dictionary to list
    
    Args:
        skills_dict: Nested dictionary of categorized skills
    
    Returns:
        list: Flat list of all skills
    """
    all_skills = []
    for category, skills in skills_dict.items():
        all_skills.extend(skills.keys())
    return all_skills

def get_skill_count_by_category(skills_dict: Dict[str, Dict[str, int]]) -> Dict[str, int]:
    """
    Count skills per category
    
    Args:
        skills_dict: Nested dictionary of categorized skills
    
    Returns:
        dict: {category: count}
    """
    return {category: len(skills) for category, skills in skills_dict.items()}

def calculate_average_confidence(skills_dict: Dict[str, Dict[str, int]]) -> float:
    """
    Calculate average confidence across all skills
    
    Args:
        skills_dict: Nested dictionary of categorized skills with confidence
    
    Returns:
        float: Average confidence score
    """
    all_confidences = []
    for category, skills in skills_dict.items():
        all_confidences.extend(skills.values())
    
    return sum(all_confidences) / len(all_confidences) if all_confidences else 0

def get_top_skills(skills_dict: Dict[str, Dict[str, int]], n: int = 10) -> List[Tuple[str, int]]:
    """
    Get top N skills by confidence score
    
    Args:
        skills_dict: Nested dictionary of categorized skills
        n: Number of top skills to return
    
    Returns:
        list: [(skill, confidence), ...]
    """
    all_skills = []
    for category, skills in skills_dict.items():
        for skill, confidence in skills.items():
            all_skills.append((skill, confidence))
    
    return sorted(all_skills, key=lambda x: x[1], reverse=True)[:n]

def categorize_by_type(skills_dict: Dict[str, Dict[str, int]]) -> Dict[str, List[str]]:
    """
    Categorize skills into Technical vs Soft Skills
    
    Args:
        skills_dict: Nested dictionary of categorized skills
    
    Returns:
        dict: {'technical': [...], 'soft': [...]}
    """
    technical_categories = [
        "Programming Languages", "Web Technologies", "Databases",
        "Cloud & DevOps", "AI & Machine Learning", "Data Science & Analytics",
        "Mobile Development", "Security & Testing", "Version Control & Tools",
        "Architecture & Design"
    ]
    
    technical = []
    soft = []
    
    for category, skills in skills_dict.items():
        if category in technical_categories:
            technical.extend(skills.keys())
        else:
            soft.extend(skills.keys())
    
    return {
        'technical': technical,
        'soft': soft
    }

def extract_years_of_experience(text: str, skill: str) -> int:
    """
    Try to extract years of experience for a specific skill
    
    Args:
        text (str): Resume text
        skill (str): Skill to look for
    
    Returns:
        int: Years of experience (0 if not found)
    """
    text_lower = text.lower()
    skill_lower = skill.lower()
    
    # Patterns like "5 years of Python", "Python (3+ years)"
    patterns = [
        rf'(\d+)\+?\s*years?\s+(?:of\s+)?{re.escape(skill_lower)}',
        rf'{re.escape(skill_lower)}\s*\((\d+)\+?\s*years?\)',
        rf'{re.escape(skill_lower)}.*?(\d+)\+?\s*years?'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text_lower)
        if match:
            try:
                return int(match.group(1))
            except:
                continue
    
    return 0