from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from catalog.models import Category, Product, ProductImage


class Command(BaseCommand):
    help = 'Creates demo catalog data and a demo user.'

    def handle(self, *args, **options):
        image_pool = [
            'products/2026/03/27/Gemini_Generated_Image_1toekm1toekm1toe.png',
            'products/2026/03/27/Gemini_Generated_Image_3fk1ej3fk1ej3fk1.png',
            'products/2026/03/27/Gemini_Generated_Image_3fk1ej3fk1ej3fk1_te55yo5.png',
            'products/2026/03/27/Gemini_Generated_Image_53n3eb53n3eb53n3.png',
            'products/2026/03/27/Gemini_Generated_Image_6n1ykl6n1ykl6n1y.png',
            'products/2026/03/27/Gemini_Generated_Image_75d8z175d8z175d8.png',
            'products/2026/03/27/Gemini_Generated_Image_ip0icfip0icfip0i.png',
            'products/2026/03/27/Gemini_Generated_Image_niijnvniijnvniij.png',
            'products/2026/03/27/Gemini_Generated_Image_x78fx2x78fx2x78f.png',
        ]

        categories = [
            ('Смартфоны', 'smartphones'),
            ('Ноутбуки', 'laptops'),
            ('Аксессуары', 'accessories'),
            ('Умный дом', 'smart-home'),
            ('Аудио', 'audio'),
        ]

        product_specs = [
            ('Смартфоны', 'Aster One', 'aster-one', 129990, 8, 'Компактный смартфон с ярким OLED-дисплеем и хорошей автономностью.', 0),
            ('Смартфоны', 'Aster Pro Max', 'aster-pro-max', 199990, 4, 'Флагманский смартфон с камерой для ночной съемки и быстрой зарядкой.', 1),
            ('Смартфоны', 'Nimbus Lite', 'nimbus-lite', 89990, 0, 'Доступная модель для повседневных задач, мессенджеров и учебы.', 2),
            ('Смартфоны', 'Nimbus Flex', 'nimbus-flex', 159990, 6, 'Смартфон с экраном 120 Гц и защитой от брызг.', 3),
            ('Ноутбуки', 'Orbit 14', 'orbit-14', 289990, 5, 'Легкий ноутбук для учебы и офиса с IPS-экраном 14 дюймов.', 4),
            ('Ноутбуки', 'Orbit 16 Pro', 'orbit-16-pro', 449990, 3, 'Производительный ноутбук для работы с графикой и монтажа.', 5),
            ('Ноутбуки', 'Comet Air', 'comet-air', 339990, 7, 'Тонкий ноутбук с металлическим корпусом и тихим охлаждением.', 6),
            ('Ноутбуки', 'Comet Studio', 'comet-studio', 519990, 2, 'Мощная станция для разработки и многозадачности.', None),
            ('Аксессуары', 'Pulse Mouse', 'pulse-mouse', 14990, 12, 'Беспроводная мышь с тихими переключателями.', 7),
            ('Аксессуары', 'Pulse Keyboard', 'pulse-keyboard', 24990, 9, 'Компактная клавиатура для дома и офиса.', None),
            ('Аксессуары', 'Magnetic Stand', 'magnetic-stand', 9990, 10, 'Настольная подставка для телефона с регулировкой наклона.', 8),
            ('Аксессуары', 'PowerCube 65W', 'powercube-65w', 18990, 0, 'Быстрая зарядка для ноутбуков и смартфонов.', None),
            ('Умный дом', 'Home Hub Mini', 'home-hub-mini', 39990, 11, 'Умная колонка с голосовым управлением и сценариями дома.', 0),
            ('Умный дом', 'Air Sense', 'air-sense', 29990, 8, 'Датчик качества воздуха с мобильными уведомлениями.', None),
            ('Умный дом', 'Light Strip', 'light-strip', 15990, 14, 'Светодиодная лента с несколькими сценариями освещения.', 1),
            ('Умный дом', 'Smart Plug S2', 'smart-plug-s2', 7990, 20, 'Умная розетка с таймером и учетом потребления.', None),
            ('Аудио', 'Wave Buds', 'wave-buds', 34990, 16, 'Беспроводные наушники с шумоподавлением.', 2),
            ('Аудио', 'Wave Studio', 'wave-studio', 68990, 5, 'Полноразмерные наушники для работы, музыки и звонков.', 3),
            ('Аудио', 'Room Beat', 'room-beat', 45990, 9, 'Портативная колонка с насыщенным басом и влагозащитой.', 4),
            ('Аудио', 'Mic Cast USB', 'mic-cast-usb', 27990, 13, 'USB-микрофон для стримов, учебы и видеозвонков.', None),
        ]

        category_map = {}
        for name, slug in categories:
            category, _ = Category.objects.update_or_create(slug=slug, defaults={'name': name})
            category_map[name] = category

        for category_name, name, slug, price, stock, description, image_index in product_specs:
            product, _ = Product.objects.update_or_create(
                slug=slug,
                defaults={
                    'category': category_map[category_name],
                    'name': name,
                    'description': description,
                    'price': price,
                    'stock': stock,
                    'is_active': True,
                },
            )

            if image_index is not None:
                ProductImage.objects.update_or_create(
                    product=product,
                    image=image_pool[image_index],
                    defaults={'alt_text': name, 'is_main': True},
                )

        user_model = get_user_model()
        demo_user, created = user_model.objects.get_or_create(
            username='demo_user',
            defaults={'email': 'demo@example.com'},
        )
        demo_user.email = 'demo@example.com'
        demo_user.set_password('demo12345')
        demo_user.save()

        if created:
            self.stdout.write(self.style.SUCCESS('Создан demo_user / demo12345'))
        else:
            self.stdout.write(self.style.SUCCESS('Обновлен demo_user / demo12345'))

        self.stdout.write(self.style.SUCCESS('Демо-каталог успешно подготовлен.'))
