from bot.statuses import StatusTypes
from bot.terminated_core.graph.state_graph import StateGraph
from bot.terminated_core.vertex.conference_content import ContentVertex
from bot.terminated_core.vertex.schedule import ScheduleTodayVertex, ScheduleTomorrowVertex, ScheduleByDateVertex, \
    ScheduleSectionVertex, ScheduleAskVertex

from bot.terminated_core.vertex.welcome import WelcomeVertex


def create_graph() -> StateGraph:
    g = StateGraph()
    g.add_action_vertex(WelcomeVertex('Welcome', StatusTypes.ROOT))
    g.add_action_vertex(ScheduleSectionVertex('Schedule', StatusTypes.ROOT, 'Расписание'))

    # расписание
    g.add_action_vertex(ScheduleAskVertex('ScheduleAskVertex', StatusTypes.NEIGHBOUR))

    g.add_action_vertex(ScheduleTodayVertex('ScheduleToday', StatusTypes.LEAF, 'На Сегодня'))
    g.add_action_vertex(ScheduleTomorrowVertex('ScheduleTomorrow', StatusTypes.LEAF, 'На завтра'))
    g.add_action_vertex(ScheduleByDateVertex('ScheduleByDate', StatusTypes.LEAF, 'По дате'))

    g.add_transition_from_parent_to_child_by_names('Welcome', 'Schedule')
    g.add_transition_from_parent_to_child_by_names('Schedule', 'ScheduleAskVertex')

    g.add_transition_from_parent_to_child_by_names('ScheduleAskVertex', 'ScheduleToday')
    g.add_transition_from_parent_to_child_by_names('ScheduleAskVertex', 'ScheduleTomorrow')
    g.add_transition_from_parent_to_child_by_names('ScheduleAskVertex', 'ScheduleByDate')

    # контент
    g.add_action_vertex(ContentVertex('Content', StatusTypes.ROOT, 'Контент'))
    g.add_transition_from_parent_to_child_by_names('Welcome', 'Content')

    g.set_default_vertices([])  # пока что пуст
    return g
