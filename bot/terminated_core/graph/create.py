from bot.statuses import StatusTypes
from bot.terminated_core.graph.state_graph import StateGraph
from bot.terminated_core.vertex.schedule import ScheduleTodayVertex, ScheduleTomorrowVertex, ScheduleByDateVertex, \
    ScheduleSectionVertex, ScheduleAskVertex

from bot.terminated_core.vertex.welcome import WelcomeVertex


def create_graph() -> StateGraph:
    g = StateGraph()
    g.add_action_vertex(WelcomeVertex('Welcome', StatusTypes.ROOT))
    g.add_action_vertex(ScheduleSectionVertex('ScheduleSection', StatusTypes.ROOT))
    g.add_action_vertex(ScheduleAskVertex('ScheduleAskVertex', StatusTypes.NEIGHBOUR))

    g.add_action_vertex(ScheduleTodayVertex('ScheduleToday', StatusTypes.LEAF))
    g.add_action_vertex(ScheduleTomorrowVertex('ScheduleTomorrow', StatusTypes.LEAF))
    g.add_action_vertex(ScheduleByDateVertex('ScheduleByDate', StatusTypes.LEAF))

    g.add_transition_from_parent_to_child_by_names('Welcome', 'ScheduleSection')
    g.add_transition_from_parent_to_child_by_names('ScheduleSection', 'ScheduleAskVertex')

    g.add_transition_from_parent_to_child_by_names('ScheduleAskVertex', 'ScheduleToday')
    g.add_transition_from_parent_to_child_by_names('ScheduleAskVertex', 'ScheduleTomorrow')
    g.add_transition_from_parent_to_child_by_names('ScheduleAskVertex', 'ScheduleByDate')

    g.set_default_vertices([])  # пока что пуст
    return g
