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
        SyllabusSubtopic.query.delete()
        SyllabusTopic.query.delete()
        db.session.commit()
        print("Cleared existing syllabus data")

def update_syllabus_from_pdf():
    """Update syllabus with exact PDF structure"""
    with app.app_context():
        # Create tables first
        db.create_all()
        print("✅ Database tables created successfully!")
        
        # Clear existing data
        clear_existing_syllabus()
        
        # Paper 1 - Fundamentals of Sociology
        paper1 = SyllabusTopic(
            name="Paper 1 - Fundamentals of Sociology",
            code="PAPER1",
            description="Sociological Thinkers, Research Methods, and Basic Concepts",
            weightage=1.0,
            order_index=1
        )
        db.session.add(paper1)
        db.session.flush()
        
        # Paper 1 subtopics based on your PDF
        paper1_subtopics = [
            # 1. Sociology - The Discipline
            SyllabusSubtopic(name="Modernity and social changes in Europe and emergence of Sociology", code="PAPER1_1.1", 
                            description="Modernity and social changes in Europe and emergence of Sociology", 
                            weightage=0.8, order_index=1, topic_id=paper1.id),
            SyllabusSubtopic(name="Scope of the subject and comparison with other social sciences", code="PAPER1_1.2", 
                            description="Scope of the subject and comparison with other social sciences", 
                            weightage=0.6, order_index=2, topic_id=paper1.id),
            SyllabusSubtopic(name="Sociology and common sense", code="PAPER1_1.3", 
                            description="Sociology and common sense", 
                            weightage=0.4, order_index=3, topic_id=paper1.id),
            
            # 2. Sociology as Science
            SyllabusSubtopic(name="Science, scientific method, and critique", code="PAPER1_2.1", 
                            description="Science, scientific method, and critique", 
                            weightage=0.8, order_index=4, topic_id=paper1.id),
            SyllabusSubtopic(name="Major theoretical strands of research methodology", code="PAPER1_2.2", 
                            description="Major theoretical strands of research methodology", 
                            weightage=0.9, order_index=5, topic_id=paper1.id),
            SyllabusSubtopic(name="Positivism and its critique", code="PAPER1_2.3", 
                            description="Positivism and its critique", 
                            weightage=0.7, order_index=6, topic_id=paper1.id),
            SyllabusSubtopic(name="Fact value and objectivity", code="PAPER1_2.4", 
                            description="Fact value and objectivity", 
                            weightage=0.6, order_index=7, topic_id=paper1.id),
            SyllabusSubtopic(name="Non-positivist methodologies", code="PAPER1_2.5", 
                            description="Non-positivist methodologies", 
                            weightage=0.7, order_index=8, topic_id=paper1.id),
            
            # 3. Research Methods and Analysis
            SyllabusSubtopic(name="Qualitative and quantitative methods", code="PAPER1_3.1", 
                            description="Qualitative and quantitative methods", 
                            weightage=0.9, order_index=9, topic_id=paper1.id),
            SyllabusSubtopic(name="Techniques of data collection", code="PAPER1_3.2", 
                            description="Techniques of data collection", 
                            weightage=0.8, order_index=10, topic_id=paper1.id),
            SyllabusSubtopic(name="Variables, sampling, hypothesis, reliability, and validity", code="PAPER1_3.3", 
                            description="Variables, sampling, hypothesis, reliability, and validity", 
                            weightage=0.8, order_index=11, topic_id=paper1.id),
            
            # 4. Sociological Thinkers
            SyllabusSubtopic(name="Karl Marx - Historical materialism, mode of production, alienation, class struggle", code="PAPER1_4.1", 
                            description="Karl Marx - Historical materialism, mode of production, alienation, class struggle", 
                            weightage=1.0, order_index=12, topic_id=paper1.id),
            SyllabusSubtopic(name="Emile Durkheim - Division of labour, social fact, suicide, religion and society", code="PAPER1_4.2", 
                            description="Emile Durkheim - Division of labour, social fact, suicide, religion and society", 
                            weightage=1.0, order_index=13, topic_id=paper1.id),
            SyllabusSubtopic(name="Max Weber - Social action, ideal types, authority, bureaucracy, protestant ethic and the spirit of capitalism", code="PAPER1_4.3", 
                            description="Max Weber - Social action, ideal types, authority, bureaucracy, protestant ethic and the spirit of capitalism", 
                            weightage=1.0, order_index=14, topic_id=paper1.id),
            SyllabusSubtopic(name="Talcott Parsons - Social system, pattern variables", code="PAPER1_4.4", 
                            description="Talcott Parsons - Social system, pattern variables", 
                            weightage=0.7, order_index=15, topic_id=paper1.id),
            SyllabusSubtopic(name="Robert K. Merton - Latent and manifest functions, conformity and deviance, reference groups", code="PAPER1_4.5", 
                            description="Robert K. Merton - Latent and manifest functions, conformity and deviance, reference groups", 
                            weightage=0.7, order_index=16, topic_id=paper1.id),
            SyllabusSubtopic(name="Mead - Self and identity", code="PAPER1_4.6", 
                            description="Mead - Self and identity", 
                            weightage=0.6, order_index=17, topic_id=paper1.id),
            
            # 5. Stratification and Mobility
            SyllabusSubtopic(name="Concepts - equality, inequality, hierarchy, exclusion, poverty, and deprivation", code="PAPER1_5.1", 
                            description="Concepts - equality, inequality, hierarchy, exclusion, poverty, and deprivation", 
                            weightage=0.9, order_index=18, topic_id=paper1.id),
            SyllabusSubtopic(name="Theories of social stratification - Structural functionalist theory, Marxist theory, Weberian theory", code="PAPER1_5.2", 
                            description="Theories of social stratification - Structural functionalist theory, Marxist theory, Weberian theory", 
                            weightage=0.9, order_index=19, topic_id=paper1.id),
            SyllabusSubtopic(name="Dimensions - Social stratification of class, status groups, gender, ethnicity and race", code="PAPER1_5.3", 
                            description="Dimensions - Social stratification of class, status groups, gender, ethnicity and race", 
                            weightage=0.8, order_index=20, topic_id=paper1.id),
            SyllabusSubtopic(name="Social mobility - open and closed systems, types of mobility, sources and causes of mobility", code="PAPER1_5.4", 
                            description="Social mobility - open and closed systems, types of mobility, sources and causes of mobility", 
                            weightage=0.8, order_index=21, topic_id=paper1.id),
            
            # 6. Works and Economic Life
            SyllabusSubtopic(name="Social organization of work in different types of society - slave society, feudal society, industrial capitalist society", code="PAPER1_6.1", 
                            description="Social organization of work in different types of society - slave society, feudal society, industrial capitalist society", 
                            weightage=0.8, order_index=22, topic_id=paper1.id),
            SyllabusSubtopic(name="Formal and informal organization of work", code="PAPER1_6.2", 
                            description="Formal and informal organization of work", 
                            weightage=0.7, order_index=23, topic_id=paper1.id),
            SyllabusSubtopic(name="Labour and society", code="PAPER1_6.3", 
                            description="Labour and society", 
                            weightage=0.7, order_index=24, topic_id=paper1.id),
            
            # 7. Politics and Society
            SyllabusSubtopic(name="Sociological theories of power", code="PAPER1_7.1", 
                            description="Sociological theories of power", 
                            weightage=0.8, order_index=25, topic_id=paper1.id),
            SyllabusSubtopic(name="Power elite, bureaucracy, pressure groups and political parties", code="PAPER1_7.2", 
                            description="Power elite, bureaucracy, pressure groups and political parties", 
                            weightage=0.7, order_index=26, topic_id=paper1.id),
            SyllabusSubtopic(name="Nation, state, citizenship, democracy, civil society, ideology", code="PAPER1_7.3", 
                            description="Nation, state, citizenship, democracy, civil society, ideology", 
                            weightage=0.8, order_index=27, topic_id=paper1.id),
            SyllabusSubtopic(name="Protest, agitation, social movements, collective action, revolution", code="PAPER1_7.4", 
                            description="Protest, agitation, social movements, collective action, revolution", 
                            weightage=0.7, order_index=28, topic_id=paper1.id),
            
            # 8. Religion and Society
            SyllabusSubtopic(name="Sociological theories of religion", code="PAPER1_8.1", 
                            description="Sociological theories of religion", 
                            weightage=0.7, order_index=29, topic_id=paper1.id),
            SyllabusSubtopic(name="Types of religious practices: animism, monism, pluralism, sects, cults", code="PAPER1_8.2", 
                            description="Types of religious practices: animism, monism, pluralism, sects, cults", 
                            weightage=0.7, order_index=30, topic_id=paper1.id),
            SyllabusSubtopic(name="Religion in modern society: religion and science, secularization, religious revivalism, fundamentalism", code="PAPER1_8.3", 
                            description="Religion in modern society: religion and science, secularization, religious revivalism, fundamentalism", 
                            weightage=0.7, order_index=31, topic_id=paper1.id),
            
            # 9. Systems of Kinship
            SyllabusSubtopic(name="Family, household, marriage", code="PAPER1_9.1", 
                            description="Family, household, marriage", 
                            weightage=0.8, order_index=32, topic_id=paper1.id),
            SyllabusSubtopic(name="Types and forms of family", code="PAPER1_9.2", 
                            description="Types and forms of family", 
                            weightage=0.7, order_index=33, topic_id=paper1.id),
            SyllabusSubtopic(name="Lineage and descent", code="PAPER1_9.3", 
                            description="Lineage and descent", 
                            weightage=0.6, order_index=34, topic_id=paper1.id),
            SyllabusSubtopic(name="Patriarchy and sexual division of labour", code="PAPER1_9.4", 
                            description="Patriarchy and sexual division of labour", 
                            weightage=0.7, order_index=35, topic_id=paper1.id),
            SyllabusSubtopic(name="Contemporary trends", code="PAPER1_9.5", 
                            description="Contemporary trends", 
                            weightage=0.6, order_index=36, topic_id=paper1.id),
            
            # 10. Social Change in Modern Society
            SyllabusSubtopic(name="Sociological theories of social change", code="PAPER1_10.1", 
                            description="Sociological theories of social change", 
                            weightage=0.8, order_index=37, topic_id=paper1.id),
            SyllabusSubtopic(name="Development and dependency", code="PAPER1_10.2", 
                            description="Development and dependency", 
                            weightage=0.7, order_index=38, topic_id=paper1.id),
            SyllabusSubtopic(name="Agents of social change", code="PAPER1_10.3", 
                            description="Agents of social change", 
                            weightage=0.7, order_index=39, topic_id=paper1.id),
            SyllabusSubtopic(name="Education and social change", code="PAPER1_10.4", 
                            description="Education and social change", 
                            weightage=0.7, order_index=40, topic_id=paper1.id),
            SyllabusSubtopic(name="Science, technology, and social change", code="PAPER1_10.5", 
                            description="Science, technology, and social change", 
                            weightage=0.6, order_index=41, topic_id=paper1.id)
        ]
        
        for subtopic in paper1_subtopics:
            db.session.add(subtopic)
        
        # Paper 2 - Indian Society: Structure and Change
        paper2 = SyllabusTopic(
            name="Paper 2 - Indian Society: Structure and Change",
            code="PAPER2",
            description="Indian Society, Social Structure, and Contemporary Issues",
            weightage=1.0,
            order_index=2
        )
        db.session.add(paper2)
        db.session.flush()
        
        # Paper 2 subtopics based on your PDF
        paper2_subtopics = [
            # A. Introducing Indian Society
            SyllabusSubtopic(name="Perspectives on the Study of Indian Society - Indology (G.S. Ghurye)", code="PAPER2_A1.1", 
                            description="Indology (G.S. Ghurye)", 
                            weightage=0.8, order_index=1, topic_id=paper2.id),
            SyllabusSubtopic(name="Perspectives on the Study of Indian Society - Structural functionalism (M. N. Srinivas)", code="PAPER2_A1.2", 
                            description="Structural functionalism (M. N. Srinivas)", 
                            weightage=0.8, order_index=2, topic_id=paper2.id),
            SyllabusSubtopic(name="Perspectives on the Study of Indian Society - Marxist sociology (A. R. Desai)", code="PAPER2_A1.3", 
                            description="Marxist sociology (A. R. Desai)", 
                            weightage=0.7, order_index=3, topic_id=paper2.id),
            SyllabusSubtopic(name="Impact of colonial rule on Indian society - Social background of Indian nationalism", code="PAPER2_A2.1", 
                            description="Social background of Indian nationalism", 
                            weightage=0.7, order_index=4, topic_id=paper2.id),
            SyllabusSubtopic(name="Impact of colonial rule on Indian society - Modernization of Indian tradition", code="PAPER2_A2.2", 
                            description="Modernization of Indian tradition", 
                            weightage=0.7, order_index=5, topic_id=paper2.id),
            SyllabusSubtopic(name="Impact of colonial rule on Indian society - Protests and movements during the colonial period", code="PAPER2_A2.3", 
                            description="Protests and movements during the colonial period", 
                            weightage=0.6, order_index=6, topic_id=paper2.id),
            SyllabusSubtopic(name="Impact of colonial rule on Indian society - Social reforms", code="PAPER2_A2.4", 
                            description="Social reforms", 
                            weightage=0.6, order_index=7, topic_id=paper2.id),
            
            # B. Social Structure
            SyllabusSubtopic(name="Rural and Agrarian Social Structure - The idea of Indian village and village studies", code="PAPER2_B1.1", 
                            description="The idea of Indian village and village studies", 
                            weightage=0.9, order_index=8, topic_id=paper2.id),
            SyllabusSubtopic(name="Rural and Agrarian Social Structure - Agrarian social structure, evolution of land tenure system, land reforms", code="PAPER2_B1.2", 
                            description="Agrarian social structure, evolution of land tenure system, land reforms", 
                            weightage=0.8, order_index=9, topic_id=paper2.id),
            SyllabusSubtopic(name="Caste System - Perspectives on the study of caste systems: G. S. Ghurye, M. N. Srinivas, Louis Dumont, Andre Beteille", code="PAPER2_B2.1", 
                            description="Perspectives on the study of caste systems: G. S. Ghurye, M. N. Srinivas, Louis Dumont, Andre Beteille", 
                            weightage=1.0, order_index=10, topic_id=paper2.id),
            SyllabusSubtopic(name="Caste System - Features of caste system", code="PAPER2_B2.2", 
                            description="Features of caste system", 
                            weightage=0.9, order_index=11, topic_id=paper2.id),
            SyllabusSubtopic(name="Caste System - Untouchability-forms and perspectives", code="PAPER2_B2.3", 
                            description="Untouchability-forms and perspectives", 
                            weightage=0.8, order_index=12, topic_id=paper2.id),
            SyllabusSubtopic(name="Tribal Communities in India - Definitional problems", code="PAPER2_B3.1", 
                            description="Definitional problems", 
                            weightage=0.7, order_index=13, topic_id=paper2.id),
            SyllabusSubtopic(name="Tribal Communities in India - Geographical spread", code="PAPER2_B3.2", 
                            description="Geographical spread", 
                            weightage=0.6, order_index=14, topic_id=paper2.id),
            SyllabusSubtopic(name="Tribal Communities in India - Colonial policies and tribes", code="PAPER2_B3.3", 
                            description="Colonial policies and tribes", 
                            weightage=0.7, order_index=15, topic_id=paper2.id),
            SyllabusSubtopic(name="Tribal Communities in India - Issues of integration and autonomy", code="PAPER2_B3.4", 
                            description="Issues of integration and autonomy", 
                            weightage=0.8, order_index=16, topic_id=paper2.id),
            SyllabusSubtopic(name="Social Classes in India - Agrarian class structure", code="PAPER2_B4.1", 
                            description="Agrarian class structure", 
                            weightage=0.8, order_index=17, topic_id=paper2.id),
            SyllabusSubtopic(name="Social Classes in India - Industrial class structure", code="PAPER2_B4.2", 
                            description="Industrial class structure", 
                            weightage=0.8, order_index=18, topic_id=paper2.id),
            SyllabusSubtopic(name="Social Classes in India - Middle classes in India", code="PAPER2_B4.3", 
                            description="Middle classes in India", 
                            weightage=0.7, order_index=19, topic_id=paper2.id),
            SyllabusSubtopic(name="Systems of Kinship in India - Lineage and descent in India", code="PAPER2_B5.1", 
                            description="Lineage and descent in India", 
                            weightage=0.7, order_index=20, topic_id=paper2.id),
            SyllabusSubtopic(name="Systems of Kinship in India - Types of kinship systems", code="PAPER2_B5.2", 
                            description="Types of kinship systems", 
                            weightage=0.6, order_index=21, topic_id=paper2.id),
            SyllabusSubtopic(name="Systems of Kinship in India - Family and marriage in India", code="PAPER2_B5.3", 
                            description="Family and marriage in India", 
                            weightage=0.8, order_index=22, topic_id=paper2.id),
            SyllabusSubtopic(name="Systems of Kinship in India - Household dimensions of the family", code="PAPER2_B5.4", 
                            description="Household dimensions of the family", 
                            weightage=0.6, order_index=23, topic_id=paper2.id),
            SyllabusSubtopic(name="Systems of Kinship in India - Patriarchy, entitlements, and sexual division of labour", code="PAPER2_B5.5", 
                            description="Patriarchy, entitlements, and sexual division of labour", 
                            weightage=0.7, order_index=24, topic_id=paper2.id),
            SyllabusSubtopic(name="Religion and Society - Religious communities in India", code="PAPER2_B6.1", 
                            description="Religious communities in India", 
                            weightage=0.7, order_index=25, topic_id=paper2.id),
            SyllabusSubtopic(name="Religion and Society - Problems of religious minorities", code="PAPER2_B6.2", 
                            description="Problems of religious minorities", 
                            weightage=0.7, order_index=26, topic_id=paper2.id),
            
            # C. Social Changes in India
            SyllabusSubtopic(name="Visions of Social Change in India - Idea of development planning and mixed economy", code="PAPER2_C1.1", 
                            description="Idea of development planning and mixed economy", 
                            weightage=0.8, order_index=27, topic_id=paper2.id),
            SyllabusSubtopic(name="Visions of Social Change in India - Constitution, law, and social change", code="PAPER2_C1.2", 
                            description="Constitution, law, and social change", 
                            weightage=0.8, order_index=28, topic_id=paper2.id),
            SyllabusSubtopic(name="Visions of Social Change in India - Education and social change", code="PAPER2_C1.3", 
                            description="Education and social change", 
                            weightage=0.7, order_index=29, topic_id=paper2.id),
            SyllabusSubtopic(name="Rural and Agrarian Transformation in India - Programmes of rural development, Community Development Programme, cooperatives, poverty alleviation schemes", code="PAPER2_C2.1", 
                            description="Programmes of rural development, Community Development Programme, cooperatives, poverty alleviation schemes", 
                            weightage=0.7, order_index=30, topic_id=paper2.id),
            SyllabusSubtopic(name="Rural and Agrarian Transformation in India - Green revolution and social change", code="PAPER2_C2.2", 
                            description="Green revolution and social change", 
                            weightage=0.6, order_index=31, topic_id=paper2.id),
            SyllabusSubtopic(name="Rural and Agrarian Transformation in India - Changing modes of production in Indian agriculture", code="PAPER2_C2.3", 
                            description="Changing modes of production in Indian agriculture", 
                            weightage=0.6, order_index=32, topic_id=paper2.id),
            SyllabusSubtopic(name="Rural and Agrarian Transformation in India - Problems of rural labour, bondage, migration", code="PAPER2_C2.4", 
                            description="Problems of rural labour, bondage, migration", 
                            weightage=0.7, order_index=33, topic_id=paper2.id),
            SyllabusSubtopic(name="Industrialization and Urbanisation in India - Evolution of modern industry in India", code="PAPER2_C3.1", 
                            description="Evolution of modern industry in India", 
                            weightage=0.7, order_index=34, topic_id=paper2.id),
            SyllabusSubtopic(name="Industrialization and Urbanisation in India - Growth of urban settlements in India", code="PAPER2_C3.2", 
                            description="Growth of urban settlements in India", 
                            weightage=0.7, order_index=35, topic_id=paper2.id),
            SyllabusSubtopic(name="Industrialization and Urbanisation in India - Working class: structure, growth, class mobilization", code="PAPER2_C3.3", 
                            description="Working class: structure, growth, class mobilization", 
                            weightage=0.8, order_index=36, topic_id=paper2.id),
            SyllabusSubtopic(name="Industrialization and Urbanisation in India - Informal sector, child labour", code="PAPER2_C3.4", 
                            description="Informal sector, child labour", 
                            weightage=0.6, order_index=37, topic_id=paper2.id),
            SyllabusSubtopic(name="Industrialization and Urbanisation in India - Slums and deprivation in urban areas", code="PAPER2_C3.5", 
                            description="Slums and deprivation in urban areas", 
                            weightage=0.6, order_index=38, topic_id=paper2.id),
            SyllabusSubtopic(name="Politics and Society - Nation, democracy and citizenship", code="PAPER2_C4.1", 
                            description="Nation, democracy and citizenship", 
                            weightage=0.8, order_index=39, topic_id=paper2.id),
            SyllabusSubtopic(name="Politics and Society - Political parties, pressure groups, social and political elite", code="PAPER2_C4.2", 
                            description="Political parties, pressure groups, social and political elite", 
                            weightage=0.7, order_index=40, topic_id=paper2.id),
            SyllabusSubtopic(name="Politics and Society - Regionalism and decentralization of power", code="PAPER2_C4.3", 
                            description="Regionalism and decentralization of power", 
                            weightage=0.6, order_index=41, topic_id=paper2.id),
            SyllabusSubtopic(name="Politics and Society - Secularization", code="PAPER2_C4.4", 
                            description="Secularization", 
                            weightage=0.6, order_index=42, topic_id=paper2.id),
            SyllabusSubtopic(name="Social Movements in Modern India - Peasants and farmers' movements", code="PAPER2_C5.1", 
                            description="Peasants and farmers' movements", 
                            weightage=0.8, order_index=43, topic_id=paper2.id),
            SyllabusSubtopic(name="Social Movements in Modern India - Women's movement", code="PAPER2_C5.2", 
                            description="Women's movement", 
                            weightage=0.8, order_index=44, topic_id=paper2.id),
            SyllabusSubtopic(name="Social Movements in Modern India - Backward classes & Dalit movements", code="PAPER2_C5.3", 
                            description="Backward classes & Dalit movements", 
                            weightage=0.8, order_index=45, topic_id=paper2.id),
            SyllabusSubtopic(name="Social Movements in Modern India - Environmental movements", code="PAPER2_C5.4", 
                            description="Environmental movements", 
                            weightage=0.6, order_index=46, topic_id=paper2.id),
            SyllabusSubtopic(name="Social Movements in Modern India - Ethnicity and Identity movements", code="PAPER2_C5.5", 
                            description="Ethnicity and Identity movements", 
                            weightage=0.7, order_index=47, topic_id=paper2.id),
            SyllabusSubtopic(name="Population Dynamics - Population size, growth, composition and distribution", code="PAPER2_C6.1", 
                            description="Population size, growth, composition and distribution", 
                            weightage=0.8, order_index=48, topic_id=paper2.id),
            SyllabusSubtopic(name="Population Dynamics - Components of population growth: birth, death, migration", code="PAPER2_C6.2", 
                            description="Components of population growth: birth, death, migration", 
                            weightage=0.7, order_index=49, topic_id=paper2.id),
            SyllabusSubtopic(name="Population Dynamics - Population Policy and family planning", code="PAPER2_C6.3", 
                            description="Population Policy and family planning", 
                            weightage=0.6, order_index=50, topic_id=paper2.id),
            SyllabusSubtopic(name="Population Dynamics - Emerging issues: ageing, sex ratios, child and infant mortality, reproductive health", code="PAPER2_C6.4", 
                            description="Emerging issues: ageing, sex ratios, child and infant mortality, reproductive health", 
                            weightage=0.6, order_index=51, topic_id=paper2.id),
            SyllabusSubtopic(name="Challenges of Social Transformation - Crisis of development: displacement, environmental problems and sustainability", code="PAPER2_C7.1", 
                            description="Crisis of development: displacement, environmental problems and sustainability", 
                            weightage=0.8, order_index=52, topic_id=paper2.id),
            SyllabusSubtopic(name="Challenges of Social Transformation - Poverty, deprivation and inequalities", code="PAPER2_C7.2", 
                            description="Poverty, deprivation and inequalities", 
                            weightage=0.8, order_index=53, topic_id=paper2.id),
            SyllabusSubtopic(name="Challenges of Social Transformation - Violence against women", code="PAPER2_C7.3", 
                            description="Violence against women", 
                            weightage=0.7, order_index=54, topic_id=paper2.id),
            SyllabusSubtopic(name="Challenges of Social Transformation - Caste conflicts", code="PAPER2_C7.4", 
                            description="Caste conflicts", 
                            weightage=0.7, order_index=55, topic_id=paper2.id),
            SyllabusSubtopic(name="Challenges of Social Transformation - Ethnic conflicts, communalism, religious revivalism", code="PAPER2_C7.5", 
                            description="Ethnic conflicts, communalism, religious revivalism", 
                            weightage=0.7, order_index=56, topic_id=paper2.id),
            SyllabusSubtopic(name="Challenges of Social Transformation - Illiteracy and disparities in education", code="PAPER2_C7.6", 
                            description="Illiteracy and disparities in education", 
                            weightage=0.6, order_index=57, topic_id=paper2.id)
        ]
        
        for subtopic in paper2_subtopics:
            db.session.add(subtopic)
        
        db.session.commit()
        print("✅ UPSC CSE Sociology syllabus updated successfully with PDF structure!")
        print(f"📊 Created {SyllabusTopic.query.count()} topics and {SyllabusSubtopic.query.count()} subtopics")
        print(f"📚 Paper 1: {len(paper1_subtopics)} subtopics")
        print(f"📚 Paper 2: {len(paper2_subtopics)} subtopics")

if __name__ == '__main__':
    update_syllabus_from_pdf() 