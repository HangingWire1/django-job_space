from django.core.management.base import BaseCommand
from authentication.models import State, Township


class Command(BaseCommand):
    help = 'Populates all 330 Myanmar Townships'

    def handle(self, *args, **options):
        DATA = {
            "Kachin State": ["Nawngmun", "Puta-O", "Machanbaw", "Khaunglanhpu", "Tanai", "Sumprabum", "Tsawlaw",
                             "Injangyang", "Chipwi", "Hsawlaw", "Myitkyina", "Mogaung", "Waingmaw", "Mohnyin", "Momauk",
                             "Shwegu", "Bhamo", "Mansi"],
            "Kayah State": ["Loikaw", "Shadaw", "Demoso", "Hpruso", "Bawlakhe", "Hpasawng", "Mese"],
            "Kayin State": ["Thandaunggyi", "Hpapun", "Hlaingbwe", "Hpa-An", "Myawaddy", "Kawkareik", "Kyainseikgyi"],
            "Chin State": ["Tonzang", "Tedim", "Falam", "Htantlang", "Hakha", "Matupi", "Mindat", "Paletwa",
                           "Kanpetlet"],
            "Sagaing Region": ["Nanyun", "Lahe", "Hkamti", "Leshi", "Homalin", "Banmauk", "Indaw", "Paungbyin", "Tamu",
                               "Pinlebu", "Wuntho", "Tigyaing", "Mawlaik", "Kawlin", "Kyunhla", "Kalewa", "Kanbalu",
                               "Kale", "Taze", "Mingin", "Ye-U", "Khin-U", "Tabayin", "Shwebo", "Kani", "Budalin",
                               "Wetlet", "Ayadaw", "Yinmabin", "Salingyi", "Pale", "Monywa", "Chaung-U", "Myinmu",
                               "Sagaing", "Myaung"],
            "Tanintharyi Region": ["Yebyu", "Launglon", "Dawei", "Thayetchaung", "Palaw", "Myeik", "Kyunsu",
                                   "Tanintharyi", "Bokpyin", "Kawthoung"],
            "Bago Region (East)": ["Yedashe", "Taungoo", "Oktwin", "Htantabin", "Phyu", "Kyaukkyi", "Kyauktaga",
                                   "Nyaunglebin", "Shwegyin", "Daik-U", "Bago", "Waw", "Thanatpin", "Kawa"],
            "Bago Region (West)": ["Paukkaung", "Pyay", "Padaung", "Paungde", "Thegon", "Shwedaung", "Nattalin",
                                   "Zigon", "Gyobingauk", "Okpho", "Monyo", "Minhla", "Letpadan", "Tharrawaddy"],
            "Magway Region": ["Gangaw", "Tilin", "Saw", "Yesagyo", "Pauk", "Pakokku", "Myaing", "Seikphyu", "Chauk",
                              "Salin", "Sidoktaya", "Pwintbyu", "Yenangyaung", "Natmauk", "Myothit", "Minbu", "Magway",
                              "Ngape", "Taungdwingyi", "Minhla", "Sinbaungwe", "Thayet", "Mindon", "Aunglan", "Kamma"],
            "Mandalay Region": ["Thabeikkyin", "Mogoke", "Singu", "Madaya", "Patheingyi", "Aungmyethazan",
                                "Chanayethazan", "Pyinoolwin", "Mahaaungmye", "Chanmyathazi", "Pyigyidagun",
                                "Amarapura", "Ngazun", "Sintgaing", "Tada-U", "Kyaukse", "Myingyan", "Natogyi",
                                "Myittha", "Taungtha", "Wundwin", "Mahlaing", "Meiktila", "Kyaukpadaung", "Thazi",
                                "Pyawbwe", "Yamethin"],
            "Mon State": ["Kyaikto", "Bilin", "Thaton", "Paung", "Mawlamyine", "Chaungzon", "Kyaikmarraw", "Mudon",
                          "Thanbyuzayat", "Ye"],
            "Rakhine State": ["Maungdaw", "Buthidaung", "Kyauktaw", "Mrauk-U", "Ponnagyun", "Rathedaung", "Minbya",
                              "Sittwe", "Pauktaw", "Myebon", "Ann", "Kyaukpyu", "Ramree", "Toungup", "Manaung",
                              "Thandwe", "Gwa"],
            "Yangon Region": ["Taikkyi", "Hlegu", "Hmawbi", "Htantabin", "Shwepyithar", "Mingaladon", "Insein",
                              "North Okkalapa", "North Dagon", "Hlaingtharyar", "Mayangone", "South Okkalapa",
                              "South Dagon", "East Dagon", "Dagon Seikkan", "Hlaing", "Yankin", "Thingangyun",
                              "Kamaryut", "Bahan", "Tamwe", "Kyimyindaing", "Sanchaung", "Mingalartaungnyunt", "Dawbon",
                              "Thaketa", "Ahlone", "Lanmadaw", "Latha", "Pabedan", "Kyauktada", "Pazundaung",
                              "Botataung", "Dala", "Seikkyikanaungto", "Seikkan", "Thanlyin", "Kyauktan", "Thongwa",
                              "Kayan", "Twantay", "Kawhmu", "Kungyangon", "Cocokyun"],
            "Shan State (South)": ["Ywangan", "Lawksawk", "Mongkaung", "Kehsi", "Hopong", "Pindaya", "Kalaw",
                                   "Taunggyi", "Monghsu", "Loilen", "Laihka", "Nansang", "Kunhing", "Mongnai",
                                   "Pinlaung", "Nyaungshwe", "Hsihseng", "Mawkmai", "Langkho", "Mongpan", "Pekon"],
            "Shan State (North)": ["Mabein", "Mongmit", "Manton", "Namhkan", "Muse", "Kutkai", "Konkyan", "Laukkaing",
                                   "Kunlong", "Namhsan", "Namtu", "Hseni", "Kyaukme", "Hopang", "Mongmao", "Pangwaun",
                                   "Lashio", "Naungcho", "Hsipaw", "Mongyai", "Tangyan", "Pangsang", "Namphan"],
            "Shan State (East)": ["Matman", "Mongyang", "Mongkhet", "Mongla", "Mongping", "Kengtung", "Monghpyak",
                                  "Mongyawng", "Mongton", "Monghsat", "Tachileik"],
            "Ayeyarwady Region": ["Kyangin", "Myanaung", "Ingapu", "Hinthada", "Lemyethna", "Zalun", "Yegyi",
                                  "Kyonpyaw", "Danubyu", "Kyaunggon", "Tharrawaddy", "Nyaungdon", "Pantanaw", "Maubin",
                                  "Pathein", "Kangyidaunt", "Einme", "Wakema", "Kyaiklat", "Myaungmya", "Ngapudaw",
                                  "Mawlamyinegyun", "Dedaye", "Pyapon", "Bogale", "Labutta"],
            "Nay Pyi Taw": ["Tatkon", "Zeyarthiri", "Ottarathiri", "Pobbathiri", "Zabuthiri", "Dekkhinathiri",
                            "Pyinmana", "Lewe"]
        }

        self.stdout.write("Initializing Myanmar Location Database...")
        for state_name, townships in DATA.items():
            state_obj, _ = State.objects.get_or_create(name=state_name)
            for ts_name in townships:
                Township.objects.get_or_create(state=state_obj, name=ts_name)

        self.stdout.write(self.style.SUCCESS(
            f"Done! Created {State.objects.count()} Regions and {Township.objects.count()} Townships."))