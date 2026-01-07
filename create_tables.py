from db.session import Base, engine  
import models  


Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

print("✅ All tables created successfully!")
