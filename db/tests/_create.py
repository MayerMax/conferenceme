import os
import datetime
import stat

from db.api import AuthApi
from db.models import Base
from db.models.event import Conference, RestActivity
from db.models.content import Section, Lecture
from db.models.infrastructure import ConferenceHashes
from db.models.official import Organization
from db.models.people import Contact, Speaker
from db.alchemy import Alchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session


def create_db(db_path='data.db'):
    Alchemy.get_instance(db_path)
    return fill_db(Alchemy.get_session(db_path))


def fill_db(session):
    media_root_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    org = Organization(name='Microsoft',
                       email_address='endurancemayer@gmail.com',
                       password=hash('123'),
                       description='We’re looking for the next big thing and we know students like you are going to build it! Register today for the Imagine Cup, Microsoft’s foremost global competition for student developers. As a student developer, your team can earn up to $11,000 and 1 of 6 spots to represent the United States at the global finals of Imagine Cup 2018. The top 12-ranked US teams will receive a trip to compete in the National Finals hosted in San Francisco, CA.',
                       logo_path='{}/media/logos/microsoft.jpg'.format(media_root_directory),
                       external_links='https://imagine.microsoft.com/ru-ru/usa;https://vk.com/imcup',
                       tags='it;community;programming;web',
                       headquarters='Moscow, Microsoft LLC')
    session.add(org)
    session.commit()

    contact_face = Contact(org_id=org.id,
                           name='Alexander Popovkin',
                           email='popovkin@mail.ru',
                           duty='Microsoft Student Partners Lead, Student Program Coordinator at MSFT',
                           photo_path='{}/media/faces/alexander.png')

    session.add(contact_face)
    session.commit()

    conference = Conference(organization_name='Microsoft',
                            conference_topics='Students; Imagine Cup; Development',
                            root_path='{}/media/'.format(media_root_directory),
                            name='Imagine Cup 2018',
                            begin_date=datetime.datetime.now(),
                            end_date=datetime.datetime.now() + datetime.timedelta(days=23),
                            logo_path='{}/media/logos/cup-logo.png'.format(media_root_directory),
                            external_links='https://imagine.microsoft.com/ru-ru/usa;https://vk.com/imcup')
    session.add(conference)
    session.commit()

    section_one = Section(conf_id=conference.id,
                          name='It in modern life',
                          tags='science;it; ML',
                          description='Our world is ever changing, from politics to the environment, it is safe to say that if our ancestors were alive, they would be seeing a very strange and different world. One aspect of society that is constantly advancing is technology. ',
                          logo_path='{}/media/logos/it.jpg'.format(media_root_directory)
                          )

    section_two = Section(conf_id=conference.id,
                          name='Bitcoin in 2018',
                          tags='bitcoin;economics',
                          description='Bitcoin Cash brings sound money to the world, fulfilling the original promise of Bitcoin as "Peer-to-Peer Electronic Cash". Merchants and users are empowered with low fees and reliable confirmations. The future shines brightly with unrestricted growth, global adoption, permissionless innovation, and decentralized development.',
                          logo_path='{}/media/logos/bitcoin.png'.format(media_root_directory)
                          )

    session.add(section_one)
    session.commit()

    session.add(section_two)
    session.commit()

    lecture = Lecture(section_id=section_one.id, conf_id=conference.id,
                      topic='Smart bots',
                      description="Azure Bot Service speeds up development by providing an integrated environment that's purpose-built for bot development with the Microsoft Bot Framework connectors and BotBuilder SDKs. Developers can get started in seconds with out-of-the-box templates for scenarios including basic, form, language understanding, question and answer, and proactive bots.",
                      room='First floor, conference hall 233b',
                      tags='IT; data science; Bots',
                      keywords='microsoft; azure; botframework; telegram; development',
                      when=datetime.datetime.now() + datetime.timedelta(days=1),
                      duration='1h 30 minutes')

    lecture2 = Lecture(section_id=section_one.id, conf_id=conference.id,
                       topic='Azure today',
                       description=" Microsoft for building, testing, deploying, and managing applications and services through a global network of Microsoft-managed data centers",
                       room='Second flor, conference hall, one A',
                       tags='IT; data science; Bots',
                       keywords='microsoft; azure; botframework; telegram; development',
                       when=datetime.datetime.now() + datetime.timedelta(days=1, hours=2),
                       duration='1h 20 minutes')

    lecture3 = Lecture(section_id=section_one.id, conf_id=conference.id,
                       topic='LUIS and how it works',
                       description="Together, the Azure Bot Service and Language Understanding service enable developers to create conversational interfaces for various scenarios like banking, travel, and entertainment. ",
                       room='Second flor, conference hall 2b',
                       tags='IT; data science; Bots',
                       keywords='azure;development, LUIS; ML',
                       when=datetime.datetime.now() + datetime.timedelta(days=1, hours=4),
                       duration='1h 15 minutes')

    session.add(lecture)
    session.add(lecture2)
    session.add(lecture3)
    session.commit()

    lecture4 = Lecture(section_id=section_two.id, conf_id=conference.id,
                       topic='Bitcoin Economics',
                       description="Bitcoin shot through the $10,000 (£7,440) barrier on Monday and by the time you read this it has probably gone through $11,000 – the last quote I saw was $10,831.75. So let’s make a prediction. A bitcoin is worthless. ",
                       room='First floor, conference hall 233b',
                       tags='Bitcoin; Money; BlockChain;',
                       keywords='economics; analysis; currency',
                       when=datetime.datetime.now() + datetime.timedelta(days=2, hours=1),
                       duration='1h 30 minutes')

    lecture5 = Lecture(section_id=section_two.id, conf_id=conference.id,
                       topic='BlockChain',
                       description="Blockchain is the world's leading software platform for digital assets. Offering the largest production block chain platform in the world, we are using new technology to build a radically better financial system.",
                       room='First floor, conference hall 233b',
                       tags='Bitcoin; Money; BlockChain;',
                       keywords='economics; analysis; currency',
                       when=datetime.datetime.now() + datetime.timedelta(days=2, hours=2),
                       duration='1h 30 minutes')

    lecture6 = Lecture(section_id=section_two.id, conf_id=conference.id,
                       topic='Python in Finance',
                       description="Before getting started, you may want to find out which IDEs and text editors are tailored to make Python editing easy, browse the list of introductory books, or look at code samples that you might find helpful.",
                       room='First floor, conference hall 233b',
                       tags='Bitcoin; Money; BlockChain;',
                       keywords='economics; analysis; currency',
                       when=datetime.datetime.now() + datetime.timedelta(days=2, hours=6),
                       duration='1h 30 minutes')

    session.add(lecture4)
    session.add(lecture5)
    session.add(lecture6)
    session.commit()

    speaker1 = Speaker(lecture_id=lecture.id, conf_id=conference.id,
                       name='Shaposhnikov Maxim',
                       description='Working at Press Index, Yekaterinburg, Junior developer in ML and Django',
                       tags='science; banking; bots',
                       external_links='https://vk.com/blue_bird_simply',
                       science_degree='bachelor at Ural Federal University',
                       photo_path='{}/media/speakers/maxim.jpg'.format(media_root_directory))

    speaker2 = Speaker(lecture_id=lecture2.id, conf_id=conference.id,
                       name='Elena Arslanova',
                       description='Working at Yandex, backend in Schedule team',
                       tags='science; banking; bots',
                       external_links='https://vk.com/contl',
                       science_degree='bachelor at Ural Federal University',
                       photo_path='{}/media/speakers/elena.jpg'.format(media_root_directory))
    speaker3 = Speaker(lecture_id=lecture3.id, conf_id=conference.id,
                       name='Shaposhnikov Konstantin',
                       description='Working in Шанхай, at turbines company',
                       tags='science; banking; bots',
                       external_links='https://vk.com/id3601333',
                       science_degree='phd in Beijing university',
                       photo_path='{}/media/speakers/konstantin.jpg'.format(media_root_directory))
    speaker4 = Speaker(lecture_id=lecture4.id, conf_id=conference.id,
                       name='Maslov Daniil',
                       description='Working at Kontur, frontend',
                       tags='science; banking; bots',
                       external_links='https://vk.com/id48089738',
                       science_degree='bachelor at Ural Federal University',
                       photo_path='{}/media/speakers/maslov.jpg'.format(media_root_directory))

    speaker5 = Speaker(lecture_id=lecture5.id, conf_id=conference.id,
                       name='Sviridov Sergei',
                       description='working at Microsoft, Yekaterinburg',
                       tags='science; banking; bots',
                       external_links='https://vk.com/xxx',
                       science_degree='master degree at Ural Federal University',
                       photo_path='{}/media/speakers/sviridov.jpg'.format(media_root_directory))

    speaker6 = Speaker(lecture_id=lecture6.id, conf_id=conference.id,
                       name='Egorov Pavel',
                       description='Working at Kontur, java developer',
                       tags='science; banking; bots',
                       external_links='https://vk.com/pe.xoposhiy',
                       science_degree='master degree at Ural Federal University',
                       photo_path='{}/media/speakers/egorov.jpg'.format(media_root_directory))
    session.add_all([speaker1, speaker2, speaker3, speaker4, speaker5, speaker6])
    session.commit()

    rest = RestActivity(conference_id=conference.id,
                        activity_type='Launch',
                        place='Canteen in main hall, SKB kontur',
                        time='At 13: 15, Tuesday and everyday this week',
                        description='Public and free lunch for every conference visitor')

    session.add(rest)
    session.commit()

    conf_hash = ConferenceHashes(conference.id, '12345')
    session.add(conf_hash)
    session.commit()

    return {
        'orgs': [org],
        'contact_faces': [contact_face],
        'conferences': [conference],
        'sections': [section_one, section_two],
        'lectures': [lecture, lecture2, lecture3, lecture4, lecture5, lecture6],
        'speakers': [speaker1, speaker2, speaker3, speaker4, speaker5, speaker6],
        'rest_activities': [rest],
        'conference_hashes': [conf_hash],
    }


if __name__ == '__main__':
    create_db()
    # AuthApi.create_organization_account('123', '123', '123')
    # s = Alchemy.get_session()
    # org = Organization(name='Microsofast',
    #                    email_address='endurancemayer@gmail.com',
    #                    password=hash('123'),
    #                    description='We’re looking for the next big thing and we know students like you are going to build it! Register today for the Imagine Cup, Microsoft’s foremost global competition for student developers. As a student developer, your team can earn up to $11,000 and 1 of 6 spots to represent the United States at the global finals of Imagine Cup 2018. The top 12-ranked US teams will receive a trip to compete in the National Finals hosted in San Francisco, CA.',
    #                    logo_path='{}/media/logos/microsoft.jpg'.format(''),
    #                    external_links='https://imagine.microsoft.com/ru-ru/usa;https://vk.com/imcup',
    #                    tags='it;community;programming;web',
    #                    headquarters='Moscow, Microsoft LLC')
    # s.add(org)
    # s.commit()
    # os.remove('tmp.db')
