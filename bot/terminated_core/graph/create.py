import emoji

from bot.statuses import StatusTypes
from bot.terminated_core.graph.state_graph import StateGraph
from bot.terminated_core.vertex.auth_mode.info import ConferenceInfoVertex
from bot.terminated_core.vertex.auth_mode.lecture import LectureVertex, LectureDisplayAllVertex, \
    LectureByNameTransitionVertex, LectureByNameFinishVertex
from bot.terminated_core.vertex.auth_mode.news import NewsVertex
from bot.terminated_core.vertex.auth_mode.schedule import ScheduleVertex, ScheduleByDateTransitionVertex, \
    ScheduleByDateFinishVertex, ScheduleAllVertex, ScheduleTodayVertex
from bot.terminated_core.vertex.auth_mode.speaker import SpeakerVertex, AllSpeakersVertex, \
    SearchSpeakerTransitionVertex, SearchSpeakerFinishVertex
from bot.terminated_core.vertex.auth_mode.welcome import WelcomeVertex
from bot.terminated_core.vertex.guest_mode.other import UnavailableActionVertex


def create_auth() -> StateGraph:
    g = StateGraph()
    g.add_action_vertex(WelcomeVertex('Welcome', StatusTypes.ROOT))

    g.add_action_vertex(ScheduleVertex('Schedule', StatusTypes.NEIGHBOUR, emoji.emojize(':calendar: Расписание',
                                                                                               use_aliases=True)))
    g.add_action_vertex(LectureVertex('Lecture', StatusTypes.NEIGHBOUR, emoji.emojize(':books: Лекции',
                                                                                      use_aliases=True)))

    g.add_action_vertex(SpeakerVertex('Speaker', StatusTypes.NEIGHBOUR, emoji.emojize(':man: Спикеры',
                                                                                      use_aliases=True)))

    g.add_action_vertex(ConferenceInfoVertex('ConferenceInfo', StatusTypes.NEIGHBOUR,
                                             emoji.emojize(':interrobang: Информация о конференции', use_aliases=True)))
    g.add_action_vertex(NewsVertex('NewsVertex', StatusTypes.NEIGHBOUR, emoji.emojize(':newspaper: Новости',
                                                                                     use_aliases=True)))

    g.add_transition_from_parent_to_child_by_names('Welcome', 'Schedule')
    g.add_transition_from_parent_to_child_by_names('Welcome', 'Lecture')
    g.add_transition_from_parent_to_child_by_names('Welcome', 'Speaker')
    g.add_transition_from_parent_to_child_by_names('Welcome', 'ConferenceInfo')
    g.add_transition_from_parent_to_child_by_names('Welcome', 'NewsVertex')


    g.add_action_vertex(ScheduleByDateTransitionVertex('ByDateTransitionVertex', StatusTypes.NEIGHBOUR,
                                                       emoji.emojize(':interrobang: По дате', use_aliases=True)))
    g.add_action_vertex(ScheduleByDateFinishVertex('ScheduleByDateFinish', StatusTypes.LEAF))

    g.add_transition_from_parent_to_child_by_names('Schedule', 'ByDateTransitionVertex')
    g.add_transition_from_parent_to_child_by_names('ByDateTransitionVertex', 'ScheduleByDateFinish')

    g.add_action_vertex(ScheduleAllVertex('ScheduleAll', StatusTypes.LEAF, emoji.emojize(':memo: Расписание целиком')))
    g.add_transition_from_parent_to_child_by_names('Schedule', 'ScheduleAll')

    g.add_action_vertex(ScheduleTodayVertex('ScheduleToday', StatusTypes.LEAF, emoji.emojize(':clock1030: Что будет сегодня',
                                                                                             use_aliases=True)))
    g.add_transition_from_parent_to_child_by_names('Schedule', 'ScheduleToday')

    g.add_action_vertex(LectureDisplayAllVertex('DisplayAllLectures', StatusTypes.LEAF, emoji.emojize(':lollipop: Список всех лекций',
                                                                                                      use_aliases=True)))

    g.add_action_vertex(LectureByNameTransitionVertex('LectureByNameTransition', StatusTypes.NEIGHBOUR,
                                                      emoji.emojize(':pencil2: Найти лекцию по названию', use_aliases=True)))
    g.add_action_vertex(LectureByNameFinishVertex('LectureByNameFinish', StatusTypes.LEAF))

    g.add_transition_from_parent_to_child_by_names('Lecture', 'DisplayAllLectures')
    g.add_transition_from_parent_to_child_by_names('Lecture', 'LectureByNameTransition')
    g.add_transition_from_parent_to_child_by_names('LectureByNameTransition', 'LectureByNameFinish')

    g.add_action_vertex(AllSpeakersVertex('AllSpeakers', StatusTypes.LEAF, emoji.emojize(':speaker: Все спикеры',
                                                                                              use_aliases=True)))
    g.add_action_vertex(SearchSpeakerTransitionVertex('SearchSpeakerTransition', StatusTypes.NEIGHBOUR,
                                                      emoji.emojize(':camera: Найти информацию о спикере',
                                                                    use_aliases=True)))
    g.add_action_vertex(SearchSpeakerFinishVertex('SearchSpeakerFinish', StatusTypes.LEAF))

    g.add_transition_from_parent_to_child_by_names('Speaker', 'AllSpeakers')
    g.add_transition_from_parent_to_child_by_names('Speaker', 'SearchSpeakerTransition')
    g.add_transition_from_parent_to_child_by_names('SearchSpeakerTransition', 'SearchSpeakerFinish')


    return g
