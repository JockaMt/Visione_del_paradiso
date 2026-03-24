from app.main import app
from app.src.database import db
from app.src.models import User, Rooms, Services, Events

def seed_database():
    with app.app_context():
        # Garante que as tabelas existam
        from app.src import models
        db.create_all()

        print("Populando usuários...")
        if not User.exists("admin"):
            User.create("admin", "admin@hotel.com", "Administrador", "123456", "Super", "Masculino", 35, "11999999999", admin=True)
        if not User.exists("joaosilva"):
            User.create("joaosilva", "joao@email.com", "João", "senha123", "Silva", "Masculino", 28, "11888888888")
        if not User.exists("mariap"):
            User.create("mariap", "maria@email.com", "Maria", "senha123", "Pereira", "Feminino", 32, "11777777777")

        print("Populando quartos...")
        if not Rooms.exists("Suíte Presidencial"):
            r1 = Rooms.create("Suíte Presidencial", "Uma acomodação de luxo com vista panorâmica para o mar, banheira de hidromassagem e serviço exclusivo.", capacity=2)
            r1.price = 1500.00
            db.session.commit()
        if not Rooms.exists("Quarto Standard Duplo"):
            r2 = Rooms.create("Quarto Standard Duplo", "Quarto confortável e econômico ideal para casais. Inclui TV, frigobar e ar-condicionado.", capacity=2)
            r2.price = 350.00
            r2.image = "https://images.pexels.com/photos/164595/pexels-photo-164595.jpeg"
            db.session.commit()
        if not Rooms.exists("Quarto Familiar Premium"):
            r3 = Rooms.create("Quarto Familiar Premium", "Amplo espaço ideal para toda a família, com duas camas de casal e varanda.", capacity=4)
            r3.price = 650.00
            db.session.commit()
            
        print("Populando serviços de hotel...")
        if not Services.exists("Café da Manhã Completo"):
            s1 = Services.create("Café da Manhã Completo", "Buffet livre com diversas opções de pães, frutas, sucos e frios.", price=45.0)
            s1.image = "https://images.pexels.com/photos/103124/pexels-photo-103124.jpeg"
            db.session.commit()
        if not Services.exists("Serviço de Quarto 24h"):
            s2 = Services.create("Serviço de Quarto 24h", "Peça refeições, lanches e bebidas no conforto do seu quarto a qualquer momento.", price=20.0)
            s2.image = "https://images.pexels.com/photos/205961/pexels-photo-205961.jpeg"
            db.session.commit()
        if not Services.exists("Acesso ao Spa"):
            s3 = Services.create("Acesso ao Spa", "Relaxe com sessões de massagem, sauna e piscinas térmicas exclusivas.", price=120.0)
            db.session.commit()

        print("Populando eventos e experiências...")
        from datetime import datetime, timedelta
        if not Events.exists("Show de Mágica Infantil"):
            e1 = Events.create("Show de Mágica Infantil", "Entretenimento garantido para as crianças durante a tarde na área de lazer.", date=datetime.now() + timedelta(days=2))
        if not Events.exists("Jantar Romântico com Música ao Vivo"):
            e2 = Events.create("Jantar Romântico com Música ao Vivo", "Uma noite especial no restaurante principal com cardápio diferenciado e violino.", date=datetime.now() + timedelta(days=1))
        if not Events.exists("Stand-up Comedy"):
            e3 = Events.create("Stand-up Comedy", "Sessão de risadas para os hóspedes no auditório principal.", date=datetime.now() + timedelta(days=5))

        print("Banco de dados populado com itens de exemplo com sucesso!")

if __name__ == '__main__':
    seed_database()
