import string
import requests
import uuid
from datetime import datetime, timedelta
from secrets import choice, randbelow, SystemRandom
from functools import lru_cache
from deep_translator import GoogleTranslator
import lorem


class Randize:
    _system_random = SystemRandom()

    def __init__(self):
        pass

    @staticmethod
    def shuffle(lst):
        """
        shuffle a list in place and return it.
        """
        for i in range(len(lst) - 1, 0, -1):
            j = Randize._system_random.randint(0, i)
            lst[i], lst[j] = lst[j], lst[i]
        return lst

    @staticmethod
    def choice(lst):
        """
        Return a random item from a list.
        """
        return choice(lst)

    @staticmethod
    def uuid():
        """
        Return a random UUID.
        """
        return str(uuid.uuid4())

    @staticmethod
    def number(min_value=0, max_value=100):
        """
        Return a secure number between min_value and max_value.
        """
        return min_value + randbelow(max_value - min_value + 1)

    @staticmethod
    def digit(length=1):
        """
        Return a random digit string with a given length.
        """
        return ''.join(choice(string.digits) for _ in range(length))

    @staticmethod
    @lru_cache(maxsize=10)
    def word(api_url="https://random-word-api.herokuapp.com/word?number=1", language='en'):
        """
        Return a random word in the specified language (default is English).
        """
        try:
            response = requests.get(api_url, timeout=2)
            if response.status_code == 200:
                word = response.json()[0]

                if language != 'en':
                    return GoogleTranslator(source='en', target=language).translate(word)

                return word
        except requests.RequestException:
            pass
        return 'unknown'

    @staticmethod
    def password(length=12, include_digits=True, include_punctuation=True):
        """
        Return a random password of specified length.
        """
        chars = string.ascii_letters
        if include_digits:
            chars += string.digits
        if include_punctuation:
            chars += string.punctuation
        return ''.join(choice(chars) for _ in range(length))

    @staticmethod
    def email(domain='gmail.com'):
        """
        Generate a random email address.
        """
        first_name = Randize.word()
        username = first_name.lower().replace(' ', '')
        return f"{username}@{domain}"

    @staticmethod
    @lru_cache(maxsize=100)
    def name(api_url="https://api.uinames.com/?amount=1", language='en'):
        """
        Return a random name in the specified language (default is English).
        """
        try:
            response = requests.get(api_url, timeout=2)
            if response.status_code == 200:
                name_data = response.json()
                full_name = f"{name_data['name']} {name_data['surname']}"

                if language != 'en':
                    return GoogleTranslator(source='auto', target=language).translate(full_name)

                return full_name
        except requests.RequestException:
            pass

        fallback_names = [
            "John Doe", "Jane Smith", "Robert Brown", "Emily White", "Michael Johnson", "Sarah Davis",
            "David Wilson", "Laura Miller", "James Anderson", "Olivia Taylor", "William Thomas",
            "Sophia Martinez", "Daniel Harris", "Isabella Clark", "Matthew Lewis", "Mia Robinson",
            "Joseph Walker", "Charlotte Young", "Henry Allen", "Amelia King", "Jackson Scott",
            "Evelyn Adams", "Andrew Baker", "Avery Nelson", "Ryan Carter", "Harper Mitchell",
            "Alexander Perez", "Ella Roberts", "Benjamin Turner", "Grace Phillips", "Jacob Cooper",
            "Chloe Parker", "Ethan Evans", "Lily Edwards", "Logan Collins", "Sofia Stewart",
            "Lucas Morris", "Zoe Rogers", "Aiden Murphy", "Mila Reed", "Elijah Morris",
            "Aria Wood", "Jameson Foster", "Luna Bell", "Samuel Bailey", "Nora Cox",
            "Jack Murphy", "Riley Ward", "Owen Powell", "Hannah Bell", "Luke Barnes",
            "Madison Ross", "Nathaniel Wood", "Leah Rivera", "Isaac Howard", "Zara James",
            "Mason Reed", "Aurora Hughes", "Julian Price", "Stella Collins", "Leo Hughes",
            "Maya Sanders", "Eli Bennett", "Addison Gray", "Henry Phillips", "Ella Adams",
            "Christopher Turner", "Samantha Murphy", "Caleb Nelson", "Victoria Howard",
            "Wyatt Hughes", "Eleanor Ross", "Landon Cooper", "Hailey Scott", "Gabriel Turner",
            "Addison Lee", "Thomas Richardson", "Katherine Jenkins", "Daniel Walker",
            "Sophie Murphy", "Zachary Gray", "Mackenzie Evans", "Lucas Clark", "Maya Allen",
            "Elijah Parker", "Sophia Martinez", "Ethan Collins", "Emily Miller", "Avery Taylor",
            "Michael Johnson", "Natalie Ross", "James Anderson", "Isabella Adams", "Robert Clark",
            "Olivia Scott", "John Harris", "Lololowka Deivison", "Vladimir Burenko",
            "Cillian Murphy", "John Week", "Jack Black"
        ]
        selected_name = Randize.choice(fallback_names)

        if language != 'en':
            return GoogleTranslator(source='auto', target=language).translate(selected_name)

        return selected_name

    @staticmethod
    def payment_card():
        """
        Generate a random payment card number (16-digit Visa/MasterCard style), name, expiration date, and CVV code.
        """

        def luhn_checksum(card_number):
            digits = [int(d) for d in str(card_number)]
            checksum = sum(digits[-1::-2]) + sum(sum(divmod(2 * d, 10)) for d in digits[-2::-2])
            return checksum % 10

        card_number = [randbelow(9) + 1] + [randbelow(10) for _ in range(14)]
        card_number_str = ''.join(map(str, card_number))
        card_number.append((10 - luhn_checksum(card_number_str)) % 10)

        card_name = Randize.name()
        expiration_date = f"{randbelow(12) + 1:02}/{randbelow(8) + 23}"
        cvv = Randize.digit(3)

        return {'number': ''.join(map(str, card_number)), 'name': card_name, 'expiration_date': expiration_date,
                'cvv': cvv}

    @staticmethod
    def struct(custom_structure=None):
        """
        Generate a random data structure (dictionary) with randomized keys/values.
        Custom structure can be passed as a dictionary template.
        Example: {'name': 'name', 'age': 'number'}
        """
        default_structure = {'name': 'name', 'age': 'number', 'card': 'payment_card'}
        structure = custom_structure if custom_structure else default_structure

        randomized_struct = {}
        for key, value_type in structure.items():
            # Dynamically call the function based on value_type string.
            func = getattr(Randize, value_type, lambda: None)
            randomized_struct[key] = func() if callable(func) else None

        return randomized_struct

    @staticmethod
    def zip_code():
        """
        Return a random country, city, and zip code.
        Now includes more European and Asian countries.
        """
        countries = {
            # Europe
            'USA': {
                'cities': ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix'],
                'zip_format': '#####'
            },
            'Germany': {
                'cities': ['Berlin', 'Munich', 'Hamburg', 'Cologne', 'Frankfurt'],
                'zip_format': '#####'
            },
            'France': {
                'cities': ['Paris', 'Marseille', 'Lyon', 'Toulouse', 'Nice'],
                'zip_format': '#####'
            },
            'United Kingdom': {
                'cities': ['London', 'Manchester', 'Birmingham', 'Leeds', 'Glasgow'],
                'zip_format': '??# #??'
            },
            'Italy': {
                'cities': ['Rome', 'Milan', 'Naples', 'Turin', 'Florence'],
                'zip_format': '#####'
            },
            'Spain': {
                'cities': ['Madrid', 'Barcelona', 'Valencia', 'Seville', 'Zaragoza'],
                'zip_format': '#####'
            },
            'Netherlands': {
                'cities': ['Amsterdam', 'Rotterdam', 'The Hague', 'Utrecht', 'Eindhoven'],
                'zip_format': '#### ??'
            },
            'Russia': {
                'cities': ['Moscow', 'Saint Petersburg', 'Novosibirsk', 'Yekaterinburg', 'Kazan'],
                'zip_format': '######'
            },
            'Sweden': {
                'cities': ['Stockholm', 'Gothenburg', 'Malmo', 'Uppsala', 'Vasteras'],
                'zip_format': '### ##'
            },
            'Switzerland': {
                'cities': ['Zurich', 'Geneva', 'Basel', 'Bern', 'Lausanne'],
                'zip_format': '####'
            },
            'Poland': {
                'cities': ['Warsaw', 'Krakow', 'Lodz', 'Wroclaw', 'Poznan'],
                'zip_format': '##-###'
            },
            'Norway': {
                'cities': ['Oslo', 'Bergen', 'Stavanger', 'Trondheim', 'Drammen'],
                'zip_format': '####'
            },
            'Greece': {
                'cities': ['Athens', 'Thessaloniki', 'Patras', 'Heraklion', 'Larissa'],
                'zip_format': '#####'
            },
            'Finland': {
                'cities': ['Helsinki', 'Espoo', 'Tampere', 'Vantaa', 'Oulu'],
                'zip_format': '#####'
            },
            'Denmark': {
                'cities': ['Copenhagen', 'Aarhus', 'Odense', 'Aalborg', 'Esbjerg'],
                'zip_format': '####'
            },
            'Ireland': {
                'cities': ['Dublin', 'Cork', 'Galway', 'Limerick', 'Waterford'],
                'zip_format': '??# ???'
            },
            'Belgium': {
                'cities': ['Brussels', 'Antwerp', 'Ghent', 'Charleroi', 'Liege'],
                'zip_format': '####'
            },
            'Czech Republic': {
                'cities': ['Prague', 'Brno', 'Ostrava', 'Plzen', 'Liberec'],
                'zip_format': '#####'
            },
            'Austria': {
                'cities': ['Vienna', 'Graz', 'Linz', 'Salzburg', 'Innsbruck'],
                'zip_format': '####'
            },
            'Portugal': {
                'cities': ['Lisbon', 'Porto', 'Braga', 'Coimbra', 'Funchal'],
                'zip_format': '####-###'
            },
            'Romania': {
                'cities': ['Bucharest', 'Cluj-Napoca', 'Timisoara', 'Iasi', 'Constanta'],
                'zip_format': '######'
            },
            'Turkey': {
                'cities': ['Istanbul', 'Ankara', 'Izmir', 'Bursa', 'Antalya'],
                'zip_format': '#####'
            },
            'Hungary': {
                'cities': ['Budapest', 'Debrecen', 'Szeged', 'Miskolc', 'Pecs'],
                'zip_format': '####'
            },

            # Asia
            'Japan': {
                'cities': ['Tokyo', 'Osaka', 'Kyoto', 'Yokohama', 'Nagoya'],
                'zip_format': '###-####'
            },
            'China': {
                'cities': ['Beijing', 'Shanghai', 'Shenzhen', 'Guangzhou', 'Chengdu'],
                'zip_format': '######'
            },
            'India': {
                'cities': ['Mumbai', 'Delhi', 'Bangalore', 'Hyderabad', 'Chennai'],
                'zip_format': '######'
            },
            'South Korea': {
                'cities': ['Seoul', 'Busan', 'Incheon', 'Daegu', 'Daejeon'],
                'zip_format': '#####'
            },
            'Vietnam': {
                'cities': ['Hanoi', 'Ho Chi Minh City', 'Da Nang', 'Haiphong', 'Can Tho'],
                'zip_format': '#####'
            },
            'Indonesia': {
                'cities': ['Jakarta', 'Surabaya', 'Bandung', 'Medan', 'Bekasi'],
                'zip_format': '#####'
            },
            'Malaysia': {
                'cities': ['Kuala Lumpur', 'George Town', 'Ipoh', 'Kuching', 'Johor Bahru'],
                'zip_format': '#####'
            },
            'Thailand': {
                'cities': ['Bangkok', 'Chiang Mai', 'Pattaya', 'Phuket', 'Nonthaburi'],
                'zip_format': '#####'
            },
            'Philippines': {
                'cities': ['Manila', 'Quezon City', 'Davao City', 'Cebu City', 'Zamboanga City'],
                'zip_format': '####'
            },
            'Singapore': {
                'cities': ['Singapore'],
                'zip_format': '######'
            },
            'Kazakhstan': {
                'cities': ['Almaty', 'Nur-Sultan', 'Shymkent', 'Karaganda', 'Aktobe'],
                'zip_format': '######'
            },
            'Uzbekistan': {
                'cities': ['Tashkent', 'Samarkand', 'Bukhara', 'Andijan', 'Namangan'],
                'zip_format': '######'
            },
            'Kyrgyzstan': {
                'cities': ['Bishkek', 'Osh', 'Jalal-Abad', 'Karakol', 'Tokmok'],
                'zip_format': '######'
            },
            'Turkmenistan': {
                'cities': ['Ashgabat', 'Turkmenabat', 'Dashoguz', 'Mary', 'Balkanabat'],
                'zip_format': '######'
            },
            'Tajikistan': {
                'cities': ['Dushanbe', 'Khujand', 'Bokhtar', 'Kulob', 'Istaravshan'],
                'zip_format': '######'
            }
        }

        country = Randize.choice(list(countries.keys()))
        city = Randize.choice(countries[country]['cities'])
        zip_format = countries[country]['zip_format']

        # Generate a zip code based on the format (e.g., "#####")
        zip_code = ''.join(choice(string.digits) if char == '#' else char for char in zip_format)

        return {'country': country, 'city': city, 'zip_code': zip_code}
    @staticmethod
    def date(start_year=2000, end_year=2023):
        """
        Generate a random date between start_year and end_year.
        """
        start_date = datetime(start_year, 1, 1)
        end_date = datetime(end_year, 12, 31)
        random_date = start_date + (end_date - start_date) * Randize._system_random.random()
        return random_date.strftime("%Y-%m-%d")

    @staticmethod
    def time():
        """
        Generate a random time in HH:MM:SS format.
        """
        return f"{randbelow(24):02}:{randbelow(60):02}:{randbelow(60):02}"

    @staticmethod
    def ipv4():
        """
        Generate a random IPv4 address.
        """
        return ".".join(str(randbelow(256)) for _ in range(4))

    @staticmethod
    def ipv6():
        """
        Generate a random IPv6 address.
        """
        return ":".join(f'{randbelow(65536):x}' for _ in range(8))

    @staticmethod
    def random_color_palette(n=5):
        """
        Generate a random color palette with 'n' colors.
        """
        return [f'#{randbelow(0xFFFFFF):06x}' for _ in range(n)]

    @staticmethod
    def random_coordinate(min_lat=-90, max_lat=90, min_lon=-180, max_lon=180):
        """
        Generate a random geographic coordinate (latitude, longitude).
        """
        lat = min_lat + (max_lat - min_lat) * Randize._system_random.random()
        lon = min_lon + (max_lon - min_lon) * Randize._system_random.random()
        return {'latitude': lat, 'longitude': lon}

    @staticmethod
    def random_emoji_pair():
        """
        Generate a random pair of emojis.
        """
        emojis = ['😀', '😂', '😍', '🤣', '😊', '😎', '😢', '😭', '😡', '👍', '🔥', '✨', '🌈', '🍕', '🎉', '🚀']
        return choice(emojis), choice(emojis)

    @staticmethod
    def random_weather():
        """
        Generate random weather conditions.
        """
        conditions = ['Sunny', 'Cloudy', 'Rainy', 'Snowy', 'Stormy', 'Windy', 'Foggy', 'Hail', 'Thunderstorm']
        temperature = randbelow(71) - 30  # Random temperature between -30 and 40 Celsius
        humidity = randbelow(101)  # Random humidity percentage
        return {'condition': choice(conditions), 'temperature': temperature, 'humidity': humidity}

    @staticmethod
    def random_hex_code():
        """
        Generate a random HEX color code.
        """
        return f'#{randbelow(0xFFFFFF):06x}'

    @staticmethod
    def random_mac_address():
        """
        Generate a random MAC address.
        """
        return ':'.join(f'{randbelow(256):02x}' for _ in range(6))

    @staticmethod
    def random_direction():
        """
        Generate a random cardinal direction.
        """
        directions = ['North', 'South', 'East', 'West']
        return choice(directions)

    @staticmethod
    def random_url():
        """
        Generate a random URL with a meaningful path and domain.
        """
        domain_names = ["example", "mysite", "coolblog", "app", "company"]
        paths = ["about", "contact", "products", "services", "home"]
        domain = f"{choice(domain_names)}{choice(['.com', '.org', '.net', '.io', '.ai'])}"
        path = '/'.join(Randize.word().split())
        return f"https://www.{domain}/{path}"

    @staticmethod
    def random_choice(options=['yes', 'no']):
        """
        Generate a random choice from a list of options.
        """
        return choice(options)

    @staticmethod
    def random_datetime(start_date='2000-01-01', end_date='2023-12-31', fmt='%Y-%m-%d %H:%M:%S', tz='UTC',
                        granularity='seconds'):
        """
        Generate a random date and time within a specified range.
        """
        start = datetime.strptime(start_date, '%Y-%m-%d')
        end = datetime.strptime(end_date, '%Y-%m-%d')
        delta = end - start
        random_days = randbelow(delta.days + 1)
        random_date = start + timedelta(days=random_days)

        if granularity == 'seconds':
            random_time = timedelta(hours=randbelow(24), minutes=randbelow(60), seconds=randbelow(60))
        elif granularity == 'minutes':
            random_time = timedelta(hours=randbelow(24), minutes=randbelow(60))
        elif granularity == 'hours':
            random_time = timedelta(hours=randbelow(24))
        else:
            random_time = timedelta()

        random_datetime = random_date + random_time
        return random_datetime.strftime(fmt)

    @staticmethod
    def random_user_agent():
        """
        Generate a random user-agent string
        """
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Safari/605.1.15",
            "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:90.0) Gecko/20100101 Firefox/90.0",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Safari/605.1.15",
            "Mozilla/5.0 (Linux; Android 11; SM-G998U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Mobile Safari/537.36",
            "Mozilla/5.0 (iPad; CPU OS 14_7 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Safari/605.1.15",
            "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; AS; rv:11.0) like Gecko",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0",
        ]
        return choice(user_agents)

    @staticmethod
    def string(length=8, include_digits=True, include_punctuation=False):
        """
        Generate a random string of a given length.
        """
        characters = string.ascii_letters

        if include_digits:
            characters += string.digits

        if include_punctuation:
            characters += string.punctuation

        return ''.join(choice(characters) for _ in range(length))

    @staticmethod
    def random_text(language='english', word_count=50):
        """
        Generates random text
        """
        words = []
        while len(words) < word_count:
            words.extend(lorem.text().split())
        text = ' '.join(words[:word_count])

        if language == 'en':
            return text

        try:
            translated_text = GoogleTranslator(source='auto', target=language).translate(text)
            return translated_text
        except Exception as e:
            print(f"Text translation error: {e}")
            return text
