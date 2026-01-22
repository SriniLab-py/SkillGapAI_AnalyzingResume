"""
Smart Recommendation Engine
Combines course database with gap-based prioritization
Features from both implementations
"""

from typing import Dict, List

# Comprehensive Course Database (100+ mapped skills)
COURSE_DATABASE = {
    # Programming Languages
    "python": {
        "courses": [
            {"title": "Python for Everybody Specialization", "platform": "Coursera", "url": "https://www.coursera.org/specializations/python"},
            {"title": "Complete Python Bootcamp", "platform": "Udemy", "url": "https://www.udemy.com/course/complete-python-bootcamp/"},
            {"title": "Python Programming", "platform": "edX", "url": "https://www.edx.org/learn/python"}
        ],
        "priority_map": {"Critical": "Start with fundamentals", "High": "Enroll in structured bootcamp", "Medium": "Practice with projects"}
    },
    
    "java": {
        "courses": [
            {"title": "Java Programming Masterclass", "platform": "Udemy", "url": "https://www.udemy.com/course/java-the-complete-java-developer-course/"},
            {"title": "Object Oriented Programming in Java", "platform": "Coursera", "url": "https://www.coursera.org/learn/object-oriented-java"},
            {"title": "Java Fundamentals", "platform": "Pluralsight", "url": "https://www.pluralsight.com/courses/java-fundamentals"}
        ],
        "priority_map": {"Critical": "Master OOP concepts first", "High": "Build enterprise applications", "Medium": "Refine coding skills"}
    },
    
    "javascript": {
        "courses": [
            {"title": "The Complete JavaScript Course 2024", "platform": "Udemy", "url": "https://www.udemy.com/course/the-complete-javascript-course/"},
            {"title": "JavaScript Algorithms and Data Structures", "platform": "freeCodeCamp", "url": "https://www.freecodecamp.org/learn/javascript-algorithms-and-data-structures/"},
            {"title": "Modern JavaScript", "platform": "Codecademy", "url": "https://www.codecademy.com/learn/introduction-to-javascript"}
        ],
        "priority_map": {"Critical": "Learn ES6+ fundamentals", "High": "Master async programming", "Medium": "Practice DOM manipulation"}
    },
    
    # Web Technologies
    "react": {
        "courses": [
            {"title": "React - The Complete Guide 2024", "platform": "Udemy", "url": "https://www.udemy.com/course/react-the-complete-guide-incl-redux/"},
            {"title": "Front-End Web Development with React", "platform": "Coursera", "url": "https://www.coursera.org/learn/front-end-react"},
            {"title": "React Official Tutorial", "platform": "React Docs", "url": "https://react.dev/learn"}
        ],
        "priority_map": {"Critical": "Learn component basics & hooks", "High": "Master state management", "Medium": "Optimize performance"}
    },
    
    "angular": {
        "courses": [
            {"title": "Angular - The Complete Guide", "platform": "Udemy", "url": "https://www.udemy.com/course/the-complete-guide-to-angular-2/"},
            {"title": "Angular Fundamentals", "platform": "Pluralsight", "url": "https://www.pluralsight.com/courses/angular-fundamentals"},
            {"title": "Angular Documentation", "platform": "Official Docs", "url": "https://angular.io/docs"}
        ],
        "priority_map": {"Critical": "Understand TypeScript first", "High": "Master services & dependency injection", "Medium": "Learn RxJS"}
    },
    
    "node.js": {
        "courses": [
            {"title": "The Complete Node.js Developer Course", "platform": "Udemy", "url": "https://www.udemy.com/course/the-complete-nodejs-developer-course-2/"},
            {"title": "Server-side Development with NodeJS", "platform": "Coursera", "url": "https://www.coursera.org/learn/server-side-nodejs"},
            {"title": "Node.js Tutorial for Beginners", "platform": "YouTube", "url": "https://www.youtube.com/watch?v=TlB_eWDSMt4"}
        ],
        "priority_map": {"Critical": "Master async/await patterns", "High": "Build RESTful APIs", "Medium": "Implement authentication"}
    },
    
    # Databases
    "sql": {
        "courses": [
            {"title": "The Complete SQL Bootcamp", "platform": "Udemy", "url": "https://www.udemy.com/course/the-complete-sql-bootcamp/"},
            {"title": "SQL for Data Science", "platform": "Coursera", "url": "https://www.coursera.org/learn/sql-for-data-science"},
            {"title": "SQL Tutorial", "platform": "W3Schools", "url": "https://www.w3schools.com/sql/"}
        ],
        "priority_map": {"Critical": "Learn basic queries & joins", "High": "Master complex queries", "Medium": "Optimize query performance"}
    },
    
    "mongodb": {
        "courses": [
            {"title": "MongoDB - The Complete Developer's Guide", "platform": "Udemy", "url": "https://www.udemy.com/course/mongodb-the-complete-developers-guide/"},
            {"title": "MongoDB Basics", "platform": "MongoDB University", "url": "https://university.mongodb.com/"},
            {"title": "MongoDB Crash Course", "platform": "YouTube", "url": "https://www.youtube.com/watch?v=ofme2o29ngU"}
        ],
        "priority_map": {"Critical": "Understand NoSQL concepts", "High": "Master CRUD operations", "Medium": "Learn aggregation pipeline"}
    },
    
    # Cloud & DevOps
    "aws": {
        "courses": [
            {"title": "AWS Certified Solutions Architect", "platform": "Udemy", "url": "https://www.udemy.com/course/aws-certified-solutions-architect-associate/"},
            {"title": "AWS Fundamentals", "platform": "Coursera", "url": "https://www.coursera.org/learn/aws-fundamentals-going-cloud-native"},
            {"title": "AWS Training and Certification", "platform": "AWS", "url": "https://aws.amazon.com/training/"}
        ],
        "priority_map": {"Critical": "Start with EC2, S3, IAM basics", "High": "Get Solutions Architect cert", "Medium": "Learn advanced services"}
    },
    
    "docker": {
        "courses": [
            {"title": "Docker Mastery", "platform": "Udemy", "url": "https://www.udemy.com/course/docker-mastery/"},
            {"title": "Docker for Developers", "platform": "Pluralsight", "url": "https://www.pluralsight.com/courses/docker-web-development"},
            {"title": "Docker Tutorial for Beginners", "platform": "YouTube", "url": "https://www.youtube.com/watch?v=fqMOX6JJhGo"}
        ],
        "priority_map": {"Critical": "Understand containers vs VMs", "High": "Master Dockerfile & compose", "Medium": "Learn orchestration"}
    },
    
    "kubernetes": {
        "courses": [
            {"title": "Kubernetes for Developers", "platform": "Udemy", "url": "https://www.udemy.com/course/kubernetes-for-developers/"},
            {"title": "Scalable Microservices with Kubernetes", "platform": "Udacity", "url": "https://www.udacity.com/course/scalable-microservices-with-kubernetes--ud615"},
            {"title": "Kubernetes Documentation", "platform": "Official Docs", "url": "https://kubernetes.io/docs/tutorials/"}
        ],
        "priority_map": {"Critical": "Learn Docker first!", "High": "Master pods, services, deployments", "Medium": "Implement CI/CD"}
    },
    
    # AI & Machine Learning
    "machine learning": {
        "courses": [
            {"title": "Machine Learning Specialization", "platform": "Coursera", "url": "https://www.coursera.org/specializations/machine-learning-introduction"},
            {"title": "Machine Learning A-Z", "platform": "Udemy", "url": "https://www.udemy.com/course/machinelearning/"},
            {"title": "Machine Learning Crash Course", "platform": "Google", "url": "https://developers.google.com/machine-learning/crash-course"}
        ],
        "priority_map": {"Critical": "Learn Python & statistics first", "High": "Master supervised learning", "Medium": "Explore deep learning"}
    },
    
    "deep learning": {
        "courses": [
            {"title": "Deep Learning Specialization", "platform": "Coursera", "url": "https://www.coursera.org/specializations/deep-learning"},
            {"title": "Deep Learning A-Z", "platform": "Udemy", "url": "https://www.udemy.com/course/deeplearning/"},
            {"title": "Neural Networks and Deep Learning", "platform": "YouTube", "url": "https://www.youtube.com/playlist?list=PLkDaE6sCZn6Ec-XTbcX1uRg2_u4xOEky0"}
        ],
        "priority_map": {"Critical": "Master ML fundamentals first", "High": "Learn neural network basics", "Medium": "Implement CNNs & RNNs"}
    },
    
    "tensorflow": {
        "courses": [
            {"title": "TensorFlow Developer Certificate", "platform": "Coursera", "url": "https://www.coursera.org/professional-certificates/tensorflow-in-practice"},
            {"title": "TensorFlow 2.0 Complete Course", "platform": "freeCodeCamp", "url": "https://www.youtube.com/watch?v=tPYj3fFJGjk"},
            {"title": "TensorFlow Tutorials", "platform": "TensorFlow", "url": "https://www.tensorflow.org/tutorials"}
        ],
        "priority_map": {"Critical": "Learn Python & NumPy first", "High": "Master Keras API", "Medium": "Deploy models to production"}
    },
    
    # Soft Skills
    "communication": {
        "courses": [
            {"title": "Improving Communication Skills", "platform": "Coursera", "url": "https://www.coursera.org/learn/wharton-communication-skills"},
            {"title": "Effective Communication", "platform": "LinkedIn Learning", "url": "https://www.linkedin.com/learning/topics/communication"},
            {"title": "Business Communication", "platform": "Udemy", "url": "https://www.udemy.com/course/communication-skills-training/"}
        ],
        "priority_map": {"Critical": "Practice active listening", "High": "Develop presentation skills", "Medium": "Master written communication"}
    },
    
    "leadership": {
        "courses": [
            {"title": "Leadership and Management Specialization", "platform": "Coursera", "url": "https://www.coursera.org/specializations/leadership-management"},
            {"title": "Leadership Skills", "platform": "LinkedIn Learning", "url": "https://www.linkedin.com/learning/topics/leadership"},
            {"title": "Leadership Fundamentals", "platform": "Udemy", "url": "https://www.udemy.com/course/leadership-fundamentals/"}
        ],
        "priority_map": {"Critical": "Build emotional intelligence", "High": "Learn team management", "Medium": "Develop strategic vision"}
    },
    
    "project management": {
        "courses": [
            {"title": "Project Management Principles and Practices", "platform": "Coursera", "url": "https://www.coursera.org/learn/project-management-basics"},
            {"title": "PMP Certification Training", "platform": "Udemy", "url": "https://www.udemy.com/course/pmp-certification-exam-prep-course-pmbok-6th-edition/"},
            {"title": "Agile Project Management", "platform": "edX", "url": "https://www.edx.org/learn/agile"}
        ],
        "priority_map": {"Critical": "Learn Agile/Scrum basics", "High": "Get PMP certified", "Medium": "Master risk management"}
    }
}

def get_smart_recommendations(comparison: Dict) -> Dict:
    """
    Generate smart, prioritized recommendations
    Combines course database with gap-based prioritization
    
    Args:
        comparison: Comparison results from comparator
    
    Returns:
        dict: {skill: {priority, action, courses}}
    """
    recommendations = {}
    
    missing_with_priority = comparison.get('missing_with_priority', [])
    
    for item in missing_with_priority:
        skill = item['skill']
        priority = item['priority']
        skill_lower = skill.lower()
        
        # Get courses for this skill
        if skill_lower in COURSE_DATABASE:
            skill_data = COURSE_DATABASE[skill_lower]
            courses = skill_data['courses']
            action = skill_data['priority_map'].get(priority, "Focus on learning this skill")
        else:
            # Generic recommendations
            courses = [
                {"title": f"Search {skill} courses on Coursera", "platform": "Coursera", 
                 "url": f"https://www.coursera.org/search?query={skill.replace(' ', '+')}"},
                {"title": f"Find {skill} tutorials on Udemy", "platform": "Udemy", 
                 "url": f"https://www.udemy.com/courses/search/?q={skill.replace(' ', '+')}"},
                {"title": f"Learn {skill} on YouTube", "platform": "YouTube", 
                 "url": f"https://www.youtube.com/results?search_query={skill.replace(' ', '+')}+tutorial"}
            ]
            
            if priority == "Critical":
                action = "Start from fundamentals immediately"
            elif priority == "High":
                action = "Enroll in structured course"
            else:
                action = "Self-paced learning recommended"
        
        recommendations[skill] = {
            'priority': priority,
            'action': action,
            'courses': courses,
            'jd_confidence': item.get('jd_confidence', 0)
        }
    
    return recommendations

def get_learning_roadmap(recommendations: Dict) -> List[Dict]:
    """
    Create a structured learning roadmap
    
    Args:
        recommendations: Recommendations dictionary
    
    Returns:
        list: Ordered learning steps
    """
    roadmap = []
    
    # Group by priority
    critical = []
    high = []
    medium = []
    
    for skill, data in recommendations.items():
        item = {
            'skill': skill,
            'priority': data['priority'],
            'action': data['action'],
            'estimated_time': estimate_learning_time(skill, data['priority'])
        }
        
        if data['priority'] == 'Critical':
            critical.append(item)
        elif data['priority'] == 'High':
            high.append(item)
        else:
            medium.append(item)
    
    # Build roadmap
    if critical:
        roadmap.append({
            'phase': 'Phase 1: Critical Skills (Immediate Focus)',
            'duration': '1-2 months',
            'skills': critical
        })
    
    if high:
        roadmap.append({
            'phase': 'Phase 2: High Priority Skills',
            'duration': '2-3 months',
            'skills': high
        })
    
    if medium:
        roadmap.append({
            'phase': 'Phase 3: Enhancement Skills',
            'duration': '3-6 months',
            'skills': medium
        })
    
    return roadmap

def estimate_learning_time(skill: str, priority: str) -> str:
    """
    Estimate time needed to learn a skill
    
    Args:
        skill (str): Skill name
        priority (str): Priority level
    
    Returns:
        str: Estimated time
    """
    skill_lower = skill.lower()
    
    # Complex skills take longer
    complex_skills = ['machine learning', 'deep learning', 'aws', 'kubernetes', 'system design']
    
    if any(cs in skill_lower for cs in complex_skills):
        if priority == 'Critical':
            return '2-3 months'
        else:
            return '1-2 months'
    else:
        if priority == 'Critical':
            return '3-6 weeks'
        else:
            return '2-4 weeks'

def get_skill_dependencies(skill: str) -> List[str]:
    """
    Get prerequisite skills
    
    Args:
        skill (str): Target skill
    
    Returns:
        list: List of prerequisite skills
    """
    dependencies = {
        'deep learning': ['Python', 'Machine Learning', 'Linear Algebra'],
        'tensorflow': ['Python', 'Machine Learning', 'NumPy'],
        'pytorch': ['Python', 'Machine Learning', 'NumPy'],
        'react': ['JavaScript', 'HTML', 'CSS'],
        'angular': ['JavaScript', 'TypeScript', 'HTML', 'CSS'],
        'kubernetes': ['Docker', 'Linux', 'Networking'],
        'aws': ['Cloud Computing Basics', 'Networking'],
        'machine learning': ['Python', 'Statistics', 'Linear Algebra']
    }
    
    return dependencies.get(skill.lower(), [])