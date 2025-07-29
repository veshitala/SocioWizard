from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

# Initialize Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sociowizard.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Define models inline
class SyllabusTopic(db.Model):
    """Main topics in UPSC CSE Sociology syllabus"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False, unique=True)
    code = db.Column(db.String(20), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=True)
    weightage = db.Column(db.Float, default=1.0)
    order_index = db.Column(db.Integer, default=0)
    paper = db.Column(db.String(10), nullable=False)  # PAPER1 or PAPER2
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

class SyllabusSubtopic(db.Model):
    """Subtopics within main topics"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    code = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=True)
    weightage = db.Column(db.Float, default=1.0)
    order_index = db.Column(db.Integer, default=0)
    topic_id = db.Column(db.Integer, db.ForeignKey('syllabus_topic.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

def clear_existing_syllabus():
    """Clear existing syllabus data"""
    with app.app_context():
        # Drop existing tables and recreate them
        db.drop_all()
        db.create_all()
        print("✅ Dropped and recreated all tables")

def reorganize_syllabus_hierarchy():
    """Reorganize syllabus with proper topic and subtopic hierarchy"""
    with app.app_context():
        # Clear existing data and recreate tables
        clear_existing_syllabus()
        
        # PAPER 1 TOPICS
        paper1_topics = [
            # 1. Sociology - The Discipline
            SyllabusTopic(name="1. Sociology - The Discipline", code="PAPER1_1", 
                         description="Modernity and social changes in Europe and emergence of Sociology", 
                         weightage=0.8, order_index=1, paper="PAPER1"),
            
            # 2. Sociology as Science
            SyllabusTopic(name="2. Sociology as Science", code="PAPER1_2", 
                         description="Science, scientific method, and critique", 
                         weightage=0.9, order_index=2, paper="PAPER1"),
            
            # 3. Research Methods and Analysis
            SyllabusTopic(name="3. Research Methods and Analysis", code="PAPER1_3", 
                         description="Qualitative and quantitative methods", 
                         weightage=0.9, order_index=3, paper="PAPER1"),
            
            # 4. Sociological Thinkers
            SyllabusTopic(name="4. Sociological Thinkers", code="PAPER1_4", 
                         description="Karl Marx, Emile Durkheim, Max Weber, and others", 
                         weightage=1.0, order_index=4, paper="PAPER1"),
            
            # 5. Stratification and Mobility
            SyllabusTopic(name="5. Stratification and Mobility", code="PAPER1_5", 
                         description="Concepts of equality, inequality, hierarchy, exclusion, poverty, and deprivation", 
                         weightage=0.9, order_index=5, paper="PAPER1"),
            
            # 6. Works and Economic Life
            SyllabusTopic(name="6. Works and Economic Life", code="PAPER1_6", 
                         description="Social organization of work in different types of society", 
                         weightage=0.8, order_index=6, paper="PAPER1"),
            
            # 7. Politics and Society
            SyllabusTopic(name="7. Politics and Society", code="PAPER1_7", 
                         description="Sociological theories of power", 
                         weightage=0.8, order_index=7, paper="PAPER1"),
            
            # 8. Religion and Society
            SyllabusTopic(name="8. Religion and Society", code="PAPER1_8", 
                         description="Sociological theories of religion", 
                         weightage=0.7, order_index=8, paper="PAPER1"),
            
            # 9. Systems of Kinship
            SyllabusTopic(name="9. Systems of Kinship", code="PAPER1_9", 
                         description="Family, household, marriage", 
                         weightage=0.8, order_index=9, paper="PAPER1"),
            
            # 10. Social Change in Modern Society
            SyllabusTopic(name="10. Social Change in Modern Society", code="PAPER1_10", 
                         description="Sociological theories of social change", 
                         weightage=0.8, order_index=10, paper="PAPER1"),
        ]
        
        # Add Paper 1 topics
        for topic in paper1_topics:
            db.session.add(topic)
        db.session.flush()
        
        # PAPER 2 TOPICS
        paper2_topics = [
            # A. Introducing Indian Society
            SyllabusTopic(name="A. Introducing Indian Society", code="PAPER2_A", 
                         description="Perspectives on the Study of Indian Society", 
                         weightage=0.8, order_index=11, paper="PAPER2"),
            
            # B. Social Structure
            SyllabusTopic(name="B. Social Structure", code="PAPER2_B", 
                         description="Rural and Agrarian Social Structure, Caste System, Tribal Communities", 
                         weightage=1.0, order_index=12, paper="PAPER2"),
            
            # C. Social Changes in India
            SyllabusTopic(name="C. Social Changes in India", code="PAPER2_C", 
                         description="Visions of Social Change, Rural and Agrarian Transformation", 
                         weightage=0.9, order_index=13, paper="PAPER2"),
        ]
        
        # Add Paper 2 topics
        for topic in paper2_topics:
            db.session.add(topic)
        db.session.flush()
        
        # Get topic IDs for reference
        topic_map = {topic.code: topic.id for topic in paper1_topics + paper2_topics}
        
        # PAPER 1 SUBTOPICS
        paper1_subtopics = [
            # 1. Sociology - The Discipline
            SyllabusSubtopic(name="(a) Modernity and social changes in Europe and emergence of Sociology", code="PAPER1_1.1", 
                            description="Modernity and social changes in Europe and emergence of Sociology", 
                            weightage=0.8, order_index=1, topic_id=topic_map["PAPER1_1"]),
            SyllabusSubtopic(name="(b) Scope of the subject and comparison with other social sciences", code="PAPER1_1.2", 
                            description="Scope of the subject and comparison with other social sciences", 
                            weightage=0.6, order_index=2, topic_id=topic_map["PAPER1_1"]),
            SyllabusSubtopic(name="(c) Sociology and common sense", code="PAPER1_1.3", 
                            description="Sociology and common sense", 
                            weightage=0.4, order_index=3, topic_id=topic_map["PAPER1_1"]),
            
            # 2. Sociology as Science
            SyllabusSubtopic(name="(a) Science, scientific method, and critique", code="PAPER1_2.1", 
                            description="Science, scientific method, and critique", 
                            weightage=0.8, order_index=4, topic_id=topic_map["PAPER1_2"]),
            SyllabusSubtopic(name="(b) Major theoretical strands of research methodology", code="PAPER1_2.2", 
                            description="Major theoretical strands of research methodology", 
                            weightage=0.9, order_index=5, topic_id=topic_map["PAPER1_2"]),
            SyllabusSubtopic(name="(c) Positivism and its critique", code="PAPER1_2.3", 
                            description="Positivism and its critique", 
                            weightage=0.7, order_index=6, topic_id=topic_map["PAPER1_2"]),
            SyllabusSubtopic(name="(d) Fact value and objectivity", code="PAPER1_2.4", 
                            description="Fact value and objectivity", 
                            weightage=0.6, order_index=7, topic_id=topic_map["PAPER1_2"]),
            SyllabusSubtopic(name="(e) Non-positivist methodologies", code="PAPER1_2.5", 
                            description="Non-positivist methodologies", 
                            weightage=0.7, order_index=8, topic_id=topic_map["PAPER1_2"]),
            
            # 3. Research Methods and Analysis
            SyllabusSubtopic(name="(a) Qualitative and quantitative methods", code="PAPER1_3.1", 
                            description="Qualitative and quantitative methods", 
                            weightage=0.9, order_index=9, topic_id=topic_map["PAPER1_3"]),
            SyllabusSubtopic(name="(b) Techniques of data collection", code="PAPER1_3.2", 
                            description="Techniques of data collection", 
                            weightage=0.8, order_index=10, topic_id=topic_map["PAPER1_3"]),
            SyllabusSubtopic(name="(c) Variables, sampling, hypothesis, reliability, and validity", code="PAPER1_3.3", 
                            description="Variables, sampling, hypothesis, reliability, and validity", 
                            weightage=0.8, order_index=11, topic_id=topic_map["PAPER1_3"]),
            
            # 4. Sociological Thinkers
            SyllabusSubtopic(name="(a) Karl Marx - Historical materialism, mode of production, alienation, class struggle", code="PAPER1_4.1", 
                            description="Karl Marx - Historical materialism, mode of production, alienation, class struggle", 
                            weightage=1.0, order_index=12, topic_id=topic_map["PAPER1_4"]),
            SyllabusSubtopic(name="(b) Emile Durkheim - Division of labour, social fact, suicide, religion and society", code="PAPER1_4.2", 
                            description="Emile Durkheim - Division of labour, social fact, suicide, religion and society", 
                            weightage=1.0, order_index=13, topic_id=topic_map["PAPER1_4"]),
            SyllabusSubtopic(name="(c) Max Weber - Social action, ideal types, authority, bureaucracy, protestant ethic and the spirit of capitalism", code="PAPER1_4.3", 
                            description="Max Weber - Social action, ideal types, authority, bureaucracy, protestant ethic and the spirit of capitalism", 
                            weightage=1.0, order_index=14, topic_id=topic_map["PAPER1_4"]),
            SyllabusSubtopic(name="(d) Talcott Parsons - Social system, pattern variables", code="PAPER1_4.4", 
                            description="Talcott Parsons - Social system, pattern variables", 
                            weightage=0.7, order_index=15, topic_id=topic_map["PAPER1_4"]),
            SyllabusSubtopic(name="(e) Robert K. Merton - Latent and manifest functions, conformity and deviance, reference groups", code="PAPER1_4.5", 
                            description="Robert K. Merton - Latent and manifest functions, conformity and deviance, reference groups", 
                            weightage=0.7, order_index=16, topic_id=topic_map["PAPER1_4"]),
            SyllabusSubtopic(name="(f) Mead - Self and identity", code="PAPER1_4.6", 
                            description="Mead - Self and identity", 
                            weightage=0.6, order_index=17, topic_id=topic_map["PAPER1_4"]),
            
            # 5. Stratification and Mobility
            SyllabusSubtopic(name="(a) Concepts - equality, inequality, hierarchy, exclusion, poverty, and deprivation", code="PAPER1_5.1", 
                            description="Concepts - equality, inequality, hierarchy, exclusion, poverty, and deprivation", 
                            weightage=0.9, order_index=18, topic_id=topic_map["PAPER1_5"]),
            SyllabusSubtopic(name="(b) Theories of social stratification - Structural functionalist theory, Marxist theory, Weberian theory", code="PAPER1_5.2", 
                            description="Theories of social stratification - Structural functionalist theory, Marxist theory, Weberian theory", 
                            weightage=0.9, order_index=19, topic_id=topic_map["PAPER1_5"]),
            SyllabusSubtopic(name="(c) Dimensions - Social stratification of class, status groups, gender, ethnicity and race", code="PAPER1_5.3", 
                            description="Dimensions - Social stratification of class, status groups, gender, ethnicity and race", 
                            weightage=0.8, order_index=20, topic_id=topic_map["PAPER1_5"]),
            SyllabusSubtopic(name="(d) Social mobility - open and closed systems, types of mobility, sources and causes of mobility", code="PAPER1_5.4", 
                            description="Social mobility - open and closed systems, types of mobility, sources and causes of mobility", 
                            weightage=0.8, order_index=21, topic_id=topic_map["PAPER1_5"]),
            
            # 6. Works and Economic Life
            SyllabusSubtopic(name="(a) Social organization of work in different types of society - slave society, feudal society, industrial capitalist society", code="PAPER1_6.1", 
                            description="Social organization of work in different types of society - slave society, feudal society, industrial capitalist society", 
                            weightage=0.8, order_index=22, topic_id=topic_map["PAPER1_6"]),
            SyllabusSubtopic(name="(b) Formal and informal organization of work", code="PAPER1_6.2", 
                            description="Formal and informal organization of work", 
                            weightage=0.7, order_index=23, topic_id=topic_map["PAPER1_6"]),
            SyllabusSubtopic(name="(c) Labour and society", code="PAPER1_6.3", 
                            description="Labour and society", 
                            weightage=0.7, order_index=24, topic_id=topic_map["PAPER1_6"]),
            
            # 7. Politics and Society
            SyllabusSubtopic(name="(a) Sociological theories of power", code="PAPER1_7.1", 
                            description="Sociological theories of power", 
                            weightage=0.8, order_index=25, topic_id=topic_map["PAPER1_7"]),
            SyllabusSubtopic(name="(b) Power elite, bureaucracy, pressure groups and political parties", code="PAPER1_7.2", 
                            description="Power elite, bureaucracy, pressure groups and political parties", 
                            weightage=0.7, order_index=26, topic_id=topic_map["PAPER1_7"]),
            SyllabusSubtopic(name="(c) Nation, state, citizenship, democracy, civil society, ideology", code="PAPER1_7.3", 
                            description="Nation, state, citizenship, democracy, civil society, ideology", 
                            weightage=0.8, order_index=27, topic_id=topic_map["PAPER1_7"]),
            SyllabusSubtopic(name="(d) Protest, agitation, social movements, collective action, revolution", code="PAPER1_7.4", 
                            description="Protest, agitation, social movements, collective action, revolution", 
                            weightage=0.7, order_index=28, topic_id=topic_map["PAPER1_7"]),
            
            # 8. Religion and Society
            SyllabusSubtopic(name="(a) Sociological theories of religion", code="PAPER1_8.1", 
                            description="Sociological theories of religion", 
                            weightage=0.7, order_index=29, topic_id=topic_map["PAPER1_8"]),
            SyllabusSubtopic(name="(b) Types of religious practices: animism, monism, pluralism, sects, cults", code="PAPER1_8.2", 
                            description="Types of religious practices: animism, monism, pluralism, sects, cults", 
                            weightage=0.7, order_index=30, topic_id=topic_map["PAPER1_8"]),
            SyllabusSubtopic(name="(c) Religion in modern society: religion and science, secularization, religious revivalism, fundamentalism", code="PAPER1_8.3", 
                            description="Religion in modern society: religion and science, secularization, religious revivalism, fundamentalism", 
                            weightage=0.7, order_index=31, topic_id=topic_map["PAPER1_8"]),
            
            # 9. Systems of Kinship
            SyllabusSubtopic(name="(a) Family, household, marriage", code="PAPER1_9.1", 
                            description="Family, household, marriage", 
                            weightage=0.8, order_index=32, topic_id=topic_map["PAPER1_9"]),
            SyllabusSubtopic(name="(b) Types and forms of family", code="PAPER1_9.2", 
                            description="Types and forms of family", 
                            weightage=0.7, order_index=33, topic_id=topic_map["PAPER1_9"]),
            SyllabusSubtopic(name="(c) Lineage and descent", code="PAPER1_9.3", 
                            description="Lineage and descent", 
                            weightage=0.6, order_index=34, topic_id=topic_map["PAPER1_9"]),
            SyllabusSubtopic(name="(d) Patriarchy and sexual division of labour", code="PAPER1_9.4", 
                            description="Patriarchy and sexual division of labour", 
                            weightage=0.7, order_index=35, topic_id=topic_map["PAPER1_9"]),
            SyllabusSubtopic(name="(e) Contemporary trends", code="PAPER1_9.5", 
                            description="Contemporary trends", 
                            weightage=0.6, order_index=36, topic_id=topic_map["PAPER1_9"]),
            
            # 10. Social Change in Modern Society
            SyllabusSubtopic(name="(a) Sociological theories of social change", code="PAPER1_10.1", 
                            description="Sociological theories of social change", 
                            weightage=0.8, order_index=37, topic_id=topic_map["PAPER1_10"]),
            SyllabusSubtopic(name="(b) Development and dependency", code="PAPER1_10.2", 
                            description="Development and dependency", 
                            weightage=0.7, order_index=38, topic_id=topic_map["PAPER1_10"]),
            SyllabusSubtopic(name="(c) Agents of social change", code="PAPER1_10.3", 
                            description="Agents of social change", 
                            weightage=0.7, order_index=39, topic_id=topic_map["PAPER1_10"]),
            SyllabusSubtopic(name="(d) Education and social change", code="PAPER1_10.4", 
                            description="Education and social change", 
                            weightage=0.7, order_index=40, topic_id=topic_map["PAPER1_10"]),
            SyllabusSubtopic(name="(e) Science, technology, and social change", code="PAPER1_10.5", 
                            description="Science, technology, and social change", 
                            weightage=0.6, order_index=41, topic_id=topic_map["PAPER1_10"]),
        ]
        
        # PAPER 2 SUBTOPICS
        paper2_subtopics = [
            # A. Introducing Indian Society
            SyllabusSubtopic(name="Perspectives on the Study of Indian Society", code="PAPER2_A1", 
                            description="(a) Indology (G.S. Ghurye), (b) Structural functionalism (M. N. Srinivas), (c) Marxist sociology (A. R. Desai)", 
                            weightage=0.8, order_index=42, topic_id=topic_map["PAPER2_A"]),
            SyllabusSubtopic(name="Impact of colonial rule on Indian society", code="PAPER2_A2", 
                            description="(a) Social background of Indian nationalism, (b) Modernization of Indian tradition, (c) Protests and movements during the colonial period, (d) Social reforms", 
                            weightage=0.7, order_index=43, topic_id=topic_map["PAPER2_A"]),
            
            # B. Social Structure
            SyllabusSubtopic(name="Rural and Agrarian Social Structure", code="PAPER2_B1", 
                            description="(a) The idea of Indian village and village studies, (b) Agrarian social structure— evolution of land tenure system, land reforms", 
                            weightage=0.9, order_index=44, topic_id=topic_map["PAPER2_B"]),
            SyllabusSubtopic(name="Caste System", code="PAPER2_B2", 
                            description="(a) Perspectives on the study of caste systems: G. S. Ghurye, M. N. Srinivas, Louis Dumont, Andre Beteille, (b) Features of caste system, (c) Untouchability-forms and perspectives", 
                            weightage=1.0, order_index=45, topic_id=topic_map["PAPER2_B"]),
            SyllabusSubtopic(name="Tribal Communities in India", code="PAPER2_B3", 
                            description="(a) Definitional problems, (b) Geographical spread, (c) Colonial policies and tribes, (d) Issues of integration and autonomy", 
                            weightage=0.8, order_index=46, topic_id=topic_map["PAPER2_B"]),
            SyllabusSubtopic(name="Social Classes in India", code="PAPER2_B4", 
                            description="(a) Agrarian class structure, (b) Industrial class structure, (c) Middle classes in India", 
                            weightage=0.8, order_index=47, topic_id=topic_map["PAPER2_B"]),
            SyllabusSubtopic(name="Systems of Kinship in India", code="PAPER2_B5", 
                            description="(a) Lineage and descent in India, (b) Types of kinship systems, (c) Family and marriage in India, (d) Household dimensions of the family, (e) Patriarchy, entitlements, and sexual division of labour", 
                            weightage=0.7, order_index=48, topic_id=topic_map["PAPER2_B"]),
            SyllabusSubtopic(name="Religion and Society", code="PAPER2_B6", 
                            description="(a) Religious communities in India, (b) Problems of religious minorities", 
                            weightage=0.7, order_index=49, topic_id=topic_map["PAPER2_B"]),
            
            # C. Social Changes in India
            SyllabusSubtopic(name="Visions of Social Change in India", code="PAPER2_C1", 
                            description="(a) Idea of development planning and mixed economy, (b) Constitution, law, and social change, (c) Education and social change", 
                            weightage=0.8, order_index=50, topic_id=topic_map["PAPER2_C"]),
            SyllabusSubtopic(name="Rural and Agrarian Transformation in India", code="PAPER2_C2", 
                            description="(a) Programmes of rural development, Community Development Programme, cooperatives, poverty alleviation schemes, (b) Green revolution and social change, (c) Changing modes of production in Indian agriculture, (d) Problems of rural labour, bondage, migration", 
                            weightage=0.7, order_index=51, topic_id=topic_map["PAPER2_C"]),
            SyllabusSubtopic(name="Industrialization and Urbanisation in India", code="PAPER2_C3", 
                            description="(a) Evolution of modern industry in India, (b) Growth of urban settlements in India, (c) Working class: structure, growth, class mobilization, (d) Informal sector, child labour, (e) Slums and deprivation in urban areas", 
                            weightage=0.7, order_index=52, topic_id=topic_map["PAPER2_C"]),
            SyllabusSubtopic(name="Politics and Society", code="PAPER2_C4", 
                            description="(a) Nation, democracy and citizenship, (b) Political parties, pressure groups, social and political elite, (c) Regionalism and decentralization of power, (d) Secularization", 
                            weightage=0.7, order_index=53, topic_id=topic_map["PAPER2_C"]),
            SyllabusSubtopic(name="Social Movements in Modern India", code="PAPER2_C5", 
                            description="(a) Peasants and farmers' movements, (b) Women's movement, (c) Backward classes & Dalit movements, (d) Environmental movements, (e) Ethnicity and Identity movements", 
                            weightage=0.8, order_index=54, topic_id=topic_map["PAPER2_C"]),
            SyllabusSubtopic(name="Population Dynamics", code="PAPER2_C6", 
                            description="Population size, growth, composition and distribution, Components of population growth: birth, death, migration, Population Policy and family planning, Emerging issues: ageing, sex ratios, child and infant mortality, reproductive health", 
                            weightage=0.7, order_index=55, topic_id=topic_map["PAPER2_C"]),
            SyllabusSubtopic(name="Challenges of Social Transformation", code="PAPER2_C7", 
                            description="(a) Crisis of development: displacement, environmental problems and sustainability, (b) Poverty, deprivation and inequalities, (c) Violence against women, (d) Caste conflicts, (e) Ethnic conflicts, communalism, religious revivalism, (f) Illiteracy and disparities in education", 
                            weightage=0.8, order_index=56, topic_id=topic_map["PAPER2_C"]),
        ]
        
        # Add all subtopics
        for subtopic in paper1_subtopics + paper2_subtopics:
            db.session.add(subtopic)
        
        db.session.commit()
        print("✅ UPSC CSE Sociology syllabus reorganized with proper hierarchy!")
        print(f"📊 Created {SyllabusTopic.query.count()} main topics and {SyllabusSubtopic.query.count()} subtopics")
        print(f"📚 Paper 1: {len(paper1_topics)} main topics with {len(paper1_subtopics)} subtopics")
        print(f"📚 Paper 2: {len(paper2_topics)} main topics with {len(paper2_subtopics)} subtopics")
        print("\n📋 Structure:")
        print("Paper 1 - Fundamentals of Sociology:")
        for topic in paper1_topics:
            print(f"  {topic.name}")
        print("\nPaper 2 - Indian Society: Structure and Change:")
        for topic in paper2_topics:
            print(f"  {topic.name}")

if __name__ == '__main__':
    reorganize_syllabus_hierarchy() 