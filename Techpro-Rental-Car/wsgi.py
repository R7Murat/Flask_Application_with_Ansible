from app import app, db
from app import User, Araba
import logging

# Veritabanı tablolarını oluştur
with app.app_context():
    db.create_all()  # Tablolar varsa oluşturulmaz

    # Admin kullanıcısını ekle (eğer yoksa)
    admin = User.query.filter_by(username='admin').first()
    if not admin:
        admin = User(
            username='admin',
            email='admin@example.com',
            is_admin=True
        )
        admin.set_password('admin123')  # Admin şifresini güvenli şekilde oluştur
        db.session.add(admin)
        db.session.commit()
        logging.info("Admin kullanıcısı başarıyla eklendi.")
    
    # Örnek araçları ekle (eğer yoksa)
    arabalar = [
        {
            'marka': 'BMW',
            'model': '320i',
            'yil': 2022,
            'gunluk_fiyat': 500,
            'resim_url': 'bmw-320i.jpg',
            'aciklama': 'Lüks ve konforlu BMW 320i',
            'kategori': 'Lüks'
        },
        {
            'marka': 'Mercedes',
            'model': 'C200',
            'yil': 2023,
            'gunluk_fiyat': 550,
            'resim_url': 'mercedes-c200.jpg',
            'aciklama': 'Şık ve modern Mercedes C200',
            'kategori': 'Lüks'
        },
        {
            'marka': 'Audi',
            'model': 'A4',
            'yil': 2022,
            'gunluk_fiyat': 480,
            'resim_url': 'audi-a4.jpg',
            'aciklama': 'Sportif ve dinamik Audi A4',
            'kategori': 'Lüks'
        },
        {
            'marka': 'Volkswagen',
            'model': 'Passat',
            'yil': 2023,
            'gunluk_fiyat': 400,
            'resim_url': 'volkswagen-passat.jpg',
            'aciklama': 'Ekonomik ve güvenilir VW Passat',
            'kategori': 'Orta Segment'
        },
        {
            'marka': 'Tesla',
            'model': 'Model X',
            'yil': 2023,
            'gunluk_fiyat': 800,
            'resim_url': 'Tesla-ModelX-2016-01.jpg',
            'aciklama': 'Elektrikli ve modern Tesla Model X',
            'kategori': 'Elektrikli'
        }
    ]

    # Araçları veritabanına ekle
    for araba_data in arabalar:
        araba = Araba.query.filter_by(marka=araba_data['marka'], model=araba_data['model']).first()
        if not araba:
            araba = Araba(**araba_data)
            db.session.add(araba)

    db.session.commit()
    logging.info("Örnek araçlar başarıyla eklendi.")

if __name__ == "__main__":
    app.run()
