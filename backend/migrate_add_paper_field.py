from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

# Initialize Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sociowizard.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

def migrate_add_paper_field():
    """Add paper field to syllabus_topic table and update existing records"""
    with app.app_context():
        try:
            # Add the paper column to the syllabus_topic table
            with db.engine.connect() as conn:
                conn.execute(db.text('ALTER TABLE syllabus_topic ADD COLUMN paper VARCHAR(10)'))
                conn.commit()
            print("✅ Added paper column to syllabus_topic table")
            
            # Update existing records based on their code
            with db.engine.connect() as conn:
                conn.execute(db.text("UPDATE syllabus_topic SET paper = 'PAPER1' WHERE code LIKE 'PAPER1%' OR code = 'PAPER1'"))
                conn.execute(db.text("UPDATE syllabus_topic SET paper = 'PAPER2' WHERE code LIKE 'PAPER2%' OR code = 'PAPER2'"))
                conn.commit()
            print("✅ Updated existing records with paper field")
            
            # Verify the migration
            with db.engine.connect() as conn:
                result = conn.execute(db.text("SELECT id, name, code, paper FROM syllabus_topic ORDER BY order_index"))
                print("\n📊 Verification - Updated records:")
                for row in result:
                    print(f"  ID: {row[0]}, Name: {row[1]}, Code: {row[2]}, Paper: {row[3]}")
            
            print(f"\n✅ Migration completed successfully!")
            
        except Exception as e:
            print(f"❌ Migration failed: {e}")
            # If the column already exists, just update the data
            try:
                with db.engine.connect() as conn:
                    conn.execute(db.text("UPDATE syllabus_topic SET paper = 'PAPER1' WHERE code LIKE 'PAPER1%' OR code = 'PAPER1'"))
                    conn.execute(db.text("UPDATE syllabus_topic SET paper = 'PAPER2' WHERE code LIKE 'PAPER2%' OR code = 'PAPER2'"))
                    conn.commit()
                print("✅ Updated existing records with paper field (column already existed)")
            except Exception as e2:
                print(f"❌ Update failed: {e2}")

if __name__ == '__main__':
    migrate_add_paper_field() 