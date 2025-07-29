import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from extensions import db

def seed_upsc_sociology_syllabus():
    """Seed the UPSC CSE Sociology syllabus"""
    
    # Import models here to avoid circular imports
    from app.models.syllabus import SyllabusTopic, SyllabusSubtopic
    
    # Check if syllabus already exists
    if SyllabusTopic.query.first():
        print("Syllabus already exists, skipping seeding...")
        return
    
    # Paper 1 - Fundamentals of Sociology
    paper1 = SyllabusTopic(
        name="Paper 1 - Fundamentals of Sociology",
        code="PAPER1",
        description="Sociological Thinkers, Research Methods, and Basic Concepts",
        weightage=1.0,
        order_index=1
    )
    db.session.add(paper1)
    db.session.flush()  # Get the ID
    
    paper1_subtopics = [
        # 1. Sociology - The Discipline
        SyllabusSubtopic(name="Sociology - The Discipline", code="PAPER1_1.1", 
                        description="Modernity and social changes in Europe and emergence of sociology", 
                        weightage=0.8, order_index=1, topic_id=paper1.id),
        SyllabusSubtopic(name="Scope of Sociology", code="PAPER1_1.2", 
                        description="Scope of the subject and comparison with other social sciences", 
                        weightage=0.6, order_index=2, topic_id=paper1.id),
        SyllabusSubtopic(name="Sociology and Common Sense", code="PAPER1_1.3", 
                        description="Sociology and common sense", 
                        weightage=0.4, order_index=3, topic_id=paper1.id),
        
        # 2. Sociology as Science
        SyllabusSubtopic(name="Science, Scientific Method and Critique", code="PAPER1_2.1", 
                        description="Science, scientific method and critique", 
                        weightage=0.8, order_index=4, topic_id=paper1.id),
        SyllabusSubtopic(name="Major Theoretical Strands", code="PAPER1_2.2", 
                        description="Major theoretical strands of research methodology", 
                        weightage=0.9, order_index=5, topic_id=paper1.id),
        SyllabusSubtopic(name="Positivism and its Critique", code="PAPER1_2.3", 
                        description="Positivism and its critique", 
                        weightage=0.7, order_index=6, topic_id=paper1.id),
        SyllabusSubtopic(name="Fact Value and Objectivity", code="PAPER1_2.4", 
                        description="Fact value and objectivity", 
                        weightage=0.6, order_index=7, topic_id=paper1.id),
        SyllabusSubtopic(name="Non-positivist Methodologies", code="PAPER1_2.5", 
                        description="Non-positivist methodologies", 
                        weightage=0.7, order_index=8, topic_id=paper1.id),
        
        # 3. Research Methods and Analysis
        SyllabusSubtopic(name="Qualitative and Quantitative Methods", code="PAPER1_3.1", 
                        description="Qualitative and quantitative methods", 
                        weightage=0.9, order_index=9, topic_id=paper1.id),
        SyllabusSubtopic(name="Techniques of Data Collection", code="PAPER1_3.2", 
                        description="Techniques of data collection", 
                        weightage=0.8, order_index=10, topic_id=paper1.id),
        SyllabusSubtopic(name="Variables, Sampling, Hypothesis", code="PAPER1_3.3", 
                        description="Variables, sampling, hypothesis, reliability and validity", 
                        weightage=0.8, order_index=11, topic_id=paper1.id),
        
        # 4. Sociological Thinkers
        SyllabusSubtopic(name="Karl Marx", code="PAPER1_4.1", 
                        description="Historical materialism, mode of production, alienation, class struggle", 
                        weightage=1.0, order_index=12, topic_id=paper1.id),
        SyllabusSubtopic(name="Emile Durkheim", code="PAPER1_4.2", 
                        description="Division of labour, social fact, suicide, religion and society", 
                        weightage=1.0, order_index=13, topic_id=paper1.id),
        SyllabusSubtopic(name="Max Weber", code="PAPER1_4.3", 
                        description="Social action, ideal types, authority, bureaucracy, protestant ethic and the spirit of capitalism", 
                        weightage=1.0, order_index=14, topic_id=paper1.id),
        SyllabusSubtopic(name="Talcott Parsons", code="PAPER1_4.4", 
                        description="Social system, pattern variables", 
                        weightage=0.7, order_index=15, topic_id=paper1.id),
        SyllabusSubtopic(name="Robert K. Merton", code="PAPER1_4.5", 
                        description="Latent and manifest functions, conformity and deviance, reference groups", 
                        weightage=0.7, order_index=16, topic_id=paper1.id),
        SyllabusSubtopic(name="Mead", code="PAPER1_4.6", 
                        description="Symbolic interactionism", 
                        weightage=0.6, order_index=17, topic_id=paper1.id),
        
        # 5. Stratification and Mobility
        SyllabusSubtopic(name="Concepts", code="PAPER1_5.1", 
                        description="Equality, inequality, hierarchy, exclusion, poverty and deprivation", 
                        weightage=0.9, order_index=18, topic_id=paper1.id),
        SyllabusSubtopic(name="Theories of Social Stratification", code="PAPER1_5.2", 
                        description="Structural functionalist theory, Marxist theory, Weberian theory", 
                        weightage=0.9, order_index=19, topic_id=paper1.id),
        SyllabusSubtopic(name="Dimensions", code="PAPER1_5.3", 
                        description="Social stratification of class, status groups, gender, ethnicity and race", 
                        weightage=0.8, order_index=20, topic_id=paper1.id),
        SyllabusSubtopic(name="Social Mobility", code="PAPER1_5.4", 
                        description="Open and closed systems, types of mobility, sources and causes of mobility", 
                        weightage=0.8, order_index=21, topic_id=paper1.id),
        
        # 6. Works and Economic Life
        SyllabusSubtopic(name="Social Organization of Work", code="PAPER1_6.1", 
                        description="Social organization of work in different types of society", 
                        weightage=0.8, order_index=22, topic_id=paper1.id),
        SyllabusSubtopic(name="Formal and Informal Organization of Work", code="PAPER1_6.2", 
                        description="Formal and informal organization of work", 
                        weightage=0.7, order_index=23, topic_id=paper1.id),
        SyllabusSubtopic(name="Labour and Society", code="PAPER1_6.3", 
                        description="Labour and society", 
                        weightage=0.7, order_index=24, topic_id=paper1.id),
        
        # 7. Politics and Society
        SyllabusSubtopic(name="Sociological Theories of Power", code="PAPER1_7.1", 
                        description="Sociological theories of power", 
                        weightage=0.8, order_index=25, topic_id=paper1.id),
        SyllabusSubtopic(name="Power Elite, Bureaucracy, Pressure Groups", code="PAPER1_7.2", 
                        description="Power elite, bureaucracy, pressure groups, and political parties", 
                        weightage=0.7, order_index=26, topic_id=paper1.id),
        SyllabusSubtopic(name="Nation, State, Citizenship", code="PAPER1_7.3", 
                        description="Nation, state, citizenship, democracy, civil society, ideology", 
                        weightage=0.8, order_index=27, topic_id=paper1.id),
        SyllabusSubtopic(name="Protest, Agitation, Social Movements", code="PAPER1_7.4", 
                        description="Protest, agitation, social movements, collective action, revolution", 
                        weightage=0.7, order_index=28, topic_id=paper1.id),
        
        # 8. Religion and Society
        SyllabusSubtopic(name="Sociological Theories of Religion", code="PAPER1_8.1", 
                        description="Sociological theories of religion", 
                        weightage=0.7, order_index=29, topic_id=paper1.id),
        SyllabusSubtopic(name="Religion in Modern Society", code="PAPER1_8.2", 
                        description="Religion in modern society: religion and science, secularization, religious revivalism, fundamentalism", 
                        weightage=0.7, order_index=30, topic_id=paper1.id),
        SyllabusSubtopic(name="Religious Communities", code="PAPER1_8.3", 
                        description="Religious communities in India", 
                        weightage=0.6, order_index=31, topic_id=paper1.id),
        
        # 9. Systems of Kinship
        SyllabusSubtopic(name="Family and Marriage", code="PAPER1_9.1", 
                        description="Family and marriage in India", 
                        weightage=0.8, order_index=32, topic_id=paper1.id),
        SyllabusSubtopic(name="Lineage and Descent", code="PAPER1_9.2", 
                        description="Lineage and descent in India", 
                        weightage=0.6, order_index=33, topic_id=paper1.id),
        SyllabusSubtopic(name="Patriarchy and Sexual Division of Labour", code="PAPER1_9.3", 
                        description="Patriarchy and sexual division of labour", 
                        weightage=0.7, order_index=34, topic_id=paper1.id),
        SyllabusSubtopic(name="Contemporary Trends", code="PAPER1_9.4", 
                        description="Contemporary trends", 
                        weightage=0.6, order_index=35, topic_id=paper1.id),
        
        # 10. Social Change in Modern Society
        SyllabusSubtopic(name="Theories of Social Change", code="PAPER1_10.1", 
                        description="Theories of social change", 
                        weightage=0.8, order_index=36, topic_id=paper1.id),
        SyllabusSubtopic(name="Agents of Social Change", code="PAPER1_10.2", 
                        description="Agents of social change", 
                        weightage=0.7, order_index=37, topic_id=paper1.id),
        SyllabusSubtopic(name="Education and Social Change", code="PAPER1_10.3", 
                        description="Education and social change", 
                        weightage=0.7, order_index=38, topic_id=paper1.id),
        SyllabusSubtopic(name="Science, Technology and Social Change", code="PAPER1_10.4", 
                        description="Science, technology and social change", 
                        weightage=0.6, order_index=39, topic_id=paper1.id)
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
    
    paper2_subtopics = [
        # 1. Introducing Indian Society
        SyllabusSubtopic(name="Perspectives on the Study of Indian Society", code="PAPER2_1.1", 
                        description="Indology (GS. Ghurye), Structural functionalism (M N Srinivas)", 
                        weightage=0.8, order_index=1, topic_id=paper2.id),
        SyllabusSubtopic(name="Marxist Sociology", code="PAPER2_1.2", 
                        description="Marxist sociology (A R Desai)", 
                        weightage=0.7, order_index=2, topic_id=paper2.id),
        
        # 2. Social Structure
        SyllabusSubtopic(name="Rural and Agrarian Social Structure", code="PAPER2_2.1", 
                        description="The idea of Indian village and village studies", 
                        weightage=0.9, order_index=3, topic_id=paper2.id),
        SyllabusSubtopic(name="Caste System", code="PAPER2_2.2", 
                        description="Caste system: Perspectives on the study of caste systems", 
                        weightage=1.0, order_index=4, topic_id=paper2.id),
        SyllabusSubtopic(name="Caste and Class", code="PAPER2_2.3", 
                        description="Caste and class", 
                        weightage=0.8, order_index=5, topic_id=paper2.id),
        SyllabusSubtopic(name="Caste and Politics", code="PAPER2_2.4", 
                        description="Caste and politics", 
                        weightage=0.7, order_index=6, topic_id=paper2.id),
        SyllabusSubtopic(name="Tribal Communities", code="PAPER2_2.5", 
                        description="Tribal communities in India", 
                        weightage=0.8, order_index=7, topic_id=paper2.id),
        SyllabusSubtopic(name="Social Classes", code="PAPER2_2.6", 
                        description="Social classes in India", 
                        weightage=0.8, order_index=8, topic_id=paper2.id),
        SyllabusSubtopic(name="Systems of Kinship", code="PAPER2_2.7", 
                        description="Systems of kinship in India", 
                        weightage=0.7, order_index=9, topic_id=paper2.id),
        SyllabusSubtopic(name="Religion and Society", code="PAPER2_2.8", 
                        description="Religious communities in India", 
                        weightage=0.7, order_index=10, topic_id=paper2.id),
        
        # 3. Social Changes in India
        SyllabusSubtopic(name="Visions of Social Change", code="PAPER2_3.1", 
                        description="Idea of development planning and mixed economy", 
                        weightage=0.8, order_index=11, topic_id=paper2.id),
        SyllabusSubtopic(name="Constitution, Law and Social Change", code="PAPER2_3.2", 
                        description="Constitution, law and social change", 
                        weightage=0.8, order_index=12, topic_id=paper2.id),
        SyllabusSubtopic(name="Education and Social Change", code="PAPER2_3.3", 
                        description="Education and social change", 
                        weightage=0.7, order_index=13, topic_id=paper2.id),
        SyllabusSubtopic(name="Land Reforms", code="PAPER2_3.4", 
                        description="Land reforms", 
                        weightage=0.6, order_index=14, topic_id=paper2.id),
        SyllabusSubtopic(name="Green Revolution", code="PAPER2_3.5", 
                        description="Green revolution and social change", 
                        weightage=0.6, order_index=15, topic_id=paper2.id),
        SyllabusSubtopic(name="Urbanization", code="PAPER2_3.6", 
                        description="Urbanization and social change", 
                        weightage=0.7, order_index=16, topic_id=paper2.id),
        SyllabusSubtopic(name="Industrialization", code="PAPER2_3.7", 
                        description="Industrialization and social change", 
                        weightage=0.7, order_index=17, topic_id=paper2.id),
        SyllabusSubtopic(name="Globalization", code="PAPER2_3.8", 
                        description="Globalization and social change", 
                        weightage=0.8, order_index=18, topic_id=paper2.id),
        
        # 4. Politics and Society
        SyllabusSubtopic(name="Democratic Decentralization", code="PAPER2_4.1", 
                        description="Democratic decentralization", 
                        weightage=0.7, order_index=19, topic_id=paper2.id),
        SyllabusSubtopic(name="Panchayati Raj", code="PAPER2_4.2", 
                        description="Panchayati raj and 73rd Constitutional amendment", 
                        weightage=0.6, order_index=20, topic_id=paper2.id),
        SyllabusSubtopic(name="Urban Local Governance", code="PAPER2_4.3", 
                        description="Urban local governance", 
                        weightage=0.5, order_index=21, topic_id=paper2.id),
        SyllabusSubtopic(name="Politics of Representation", code="PAPER2_4.4", 
                        description="Politics of representation and participation", 
                        weightage=0.6, order_index=22, topic_id=paper2.id),
        
        # 5. Social Movements in Modern India
        SyllabusSubtopic(name="Peasants and Farmers Movements", code="PAPER2_5.1", 
                        description="Peasants and farmers movements", 
                        weightage=0.8, order_index=23, topic_id=paper2.id),
        SyllabusSubtopic(name="Women's Movement", code="PAPER2_5.2", 
                        description="Women's movement", 
                        weightage=0.8, order_index=24, topic_id=paper2.id),
        SyllabusSubtopic(name="Backward Classes Movement", code="PAPER2_5.3", 
                        description="Backward classes & Dalit movement", 
                        weightage=0.8, order_index=25, topic_id=paper2.id),
        SyllabusSubtopic(name="Environmental Movements", code="PAPER2_5.4", 
                        description="Environmental movements", 
                        weightage=0.6, order_index=26, topic_id=paper2.id),
        SyllabusSubtopic(name="Ethnicity and Identity Movements", code="PAPER2_5.5", 
                        description="Ethnicity and identity movements", 
                        weightage=0.7, order_index=27, topic_id=paper2.id),
        
        # 6. Population Dynamics
        SyllabusSubtopic(name="Population Size, Growth, Composition", code="PAPER2_6.1", 
                        description="Population size, growth, composition and distribution", 
                        weightage=0.8, order_index=28, topic_id=paper2.id),
        SyllabusSubtopic(name="Components of Population Growth", code="PAPER2_6.2", 
                        description="Components of population growth: birth, death, migration", 
                        weightage=0.7, order_index=29, topic_id=paper2.id),
        SyllabusSubtopic(name="Population Policy", code="PAPER2_6.3", 
                        description="Population policy and family planning", 
                        weightage=0.6, order_index=30, topic_id=paper2.id),
        SyllabusSubtopic(name="Emerging Issues", code="PAPER2_6.4", 
                        description="Emerging issues: ageing, sex ratios, child and infant mortality", 
                        weightage=0.6, order_index=31, topic_id=paper2.id),
        
        # 7. Challenges of Social Transformation
        SyllabusSubtopic(name="Crisis of Development", code="PAPER2_7.1", 
                        description="Crisis of development: displacement, environmental problems and sustainability", 
                        weightage=0.8, order_index=32, topic_id=paper2.id),
        SyllabusSubtopic(name="Poverty, Deprivation and Inequalities", code="PAPER2_7.2", 
                        description="Poverty, deprivation and inequalities", 
                        weightage=0.8, order_index=33, topic_id=paper2.id),
        SyllabusSubtopic(name="Violence against Women", code="PAPER2_7.3", 
                        description="Violence against women", 
                        weightage=0.7, order_index=34, topic_id=paper2.id),
        SyllabusSubtopic(name="Caste Conflicts", code="PAPER2_7.4", 
                        description="Caste conflicts", 
                        weightage=0.7, order_index=35, topic_id=paper2.id),
        SyllabusSubtopic(name="Communalism", code="PAPER2_7.5", 
                        description="Communalism, religious revivalism", 
                        weightage=0.7, order_index=36, topic_id=paper2.id),
        SyllabusSubtopic(name="Illiteracy and Disparities", code="PAPER2_7.6", 
                        description="Illiteracy and disparities in education", 
                        weightage=0.6, order_index=37, topic_id=paper2.id)
    ]
    
    for subtopic in paper2_subtopics:
        db.session.add(subtopic)
    
    db.session.commit()
    print("UPSC CSE Sociology syllabus seeded successfully!") 