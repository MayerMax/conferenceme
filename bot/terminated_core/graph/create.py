import emoji

from bot.statuses import StatusTypes
from bot.terminated_core.graph.state_graph import StateGraph
from bot.terminated_core.vertex.auth_mode.info import ConferenceInfoVertex
from bot.terminated_core.vertex.auth_mode.lecture import LectureVertex
from bot.terminated_core.vertex.auth_mode.news import NewsVertex
from bot.terminated_core.vertex.auth_mode.schedule import ScheduleVertex, ScheduleByDateTransitionVertex, \
    ScheduleByDateFinishVertex, ScheduleAllVertex, ScheduleTodayVertex
from bot.terminated_core.vertex.auth_mode.speaker import SpeakerVertex
from bot.terminated_core.vertex.auth_mode.welcome import WelcomeVertex


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

    # g.add_action_vertex(ScheduleAskVertex('ScheduleAskVertex', StatusTypes.NEIGHBOUR))
    #
    # g.add_action_vertex(ScheduleTodayVertex('ScheduleToday', StatusTypes.LEAF, 'На Сегодня'))
    # g.add_action_vertex(ScheduleTomorrowVertex('ScheduleTomorrow', StatusTypes.LEAF, 'На завтра'))
    #
    # g.add_action_vertex(ScheduleDateAskVertex('ScheduleDateAskVertex', StatusTypes.NEIGHBOUR, 'По дате'))
    # g.add_action_vertex(ScheduleByDateVertex('ScheduleByDate', StatusTypes.LEAF))
    #
    # g.add_transition_from_parent_to_child_by_names('Welcome', 'Schedule')
    # g.add_transition_from_parent_to_child_by_names('Schedule', 'ScheduleAskVertex')
    #
    # g.add_transition_from_parent_to_child_by_names('ScheduleAskVertex', 'ScheduleToday')
    # g.add_transition_from_parent_to_child_by_names('ScheduleAskVertex', 'ScheduleTomorrow')
    #
    # g.add_transition_from_parent_to_child_by_names('ScheduleAskVertex', 'ScheduleDateAskVertex')
    #
    # g.add_transition_from_parent_to_child_by_names('ScheduleDateAskVertex', 'ScheduleByDate')
    #
    # # контент
    # g.add_action_vertex(ContentVertex('Content', StatusTypes.ROOT, 'Контент'))
    # g.add_action_vertex(BeginAskAboutSpeaker('BeginAskAboutSpeaker', StatusTypes.NEIGHBOUR, 'Узнать о лекторе'))
    # g.add_action_vertex(AskAboutSpeaker('AskAboutSpeaker', StatusTypes.LEAF))
    #
    # g.add_transition_from_parent_to_child_by_names('Welcome', 'Content')
    # g.add_transition_from_parent_to_child_by_names('Content', 'BeginAskAboutSpeaker')
    # g.add_transition_from_parent_to_child_by_names('BeginAskAboutSpeaker', 'AskAboutSpeaker')
    #
    # g.set_default_vertices(['Content', 'Schedule'])  # пока что пуст

    return g
