from emoji import emojize

from bot.statuses import StatusTypes
from bot.terminated_core.graph.state_graph import StateGraph
from bot.terminated_core.vertex.guest_mode.about import AboutUsVertex
from bot.terminated_core.vertex.guest_mode.auth import AuthorizeVertex, AuthorizeConclusionVertex
from bot.terminated_core.vertex.guest_mode.find_more import FindMoreAboutConferenceVertex
from bot.terminated_core.vertex.guest_mode.hello import HelloVertex
from bot.terminated_core.vertex.guest_mode.profile import YourProfileVertex


def create_guest() -> StateGraph:
    g = StateGraph()

    g.add_action_vertex(HelloVertex('Welcome', StatusTypes.ROOT))
    g.add_action_vertex(FindMoreAboutConferenceVertex('FindMoreAboutConferences', StatusTypes.NEIGHBOUR,
                                                      emojize(':mag_right: Поиск Конференций', use_aliases=True)))
    g.add_action_vertex(AuthorizeVertex('Authorization', StatusTypes.NEIGHBOUR, emojize(':key: Авторизация',
                                                                                        use_aliases=True)))
    g.add_action_vertex(YourProfileVertex('Profile', StatusTypes.NEIGHBOUR, emojize(':bust_in_silhouette: Ваш Профиль',
                                                                                    use_aliases=True)))

    g.add_action_vertex(AboutUsVertex('AboutUs', StatusTypes.NEIGHBOUR, emojize(':information_source: О нас',
                                                                                use_aliases=True)))

    g.add_transition_from_parent_to_child_by_names('Welcome', 'FindMoreAboutConferences')
    g.add_transition_from_parent_to_child_by_names('Welcome', 'Authorization')
    g.add_transition_from_parent_to_child_by_names('Welcome', 'Profile')
    g.add_transition_from_parent_to_child_by_names('Welcome', 'AboutUs')

    g.add_action_vertex(AuthorizeConclusionVertex('AuthorizeConclusionVertex', StatusTypes.LEAF))
    g.add_transition_from_parent_to_child_by_names('Authorization', 'AuthorizeConclusionVertex')
    return g
