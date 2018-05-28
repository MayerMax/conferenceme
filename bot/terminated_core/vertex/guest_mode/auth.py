from bot.query import QueryRequest, QueryResult
from bot.service.history import Context
from bot.statuses import StatusTypes, RequestType
from bot.terminated_core.vertex.vertex import BaseActionVertex
from db.api import ConferenceApi

string_auth_response = 'Я умею авторизовывать по ключу - просто введи код; а могу через qr код по фотографии.' \
                       'Если у тебя вдруг нет ключа, то тебе надо пройти на наш сайт конференций и зарегистрироваться ' \
                       'на какую-нибудь, либо можешь сделать то же самое через меня.'

string_auth_end_response = {
    'Success': 'Отлично, Пароль принят!',
    'Failure': 'Не нашел ни одной конференции с твоим ключом. Либо что-то введено неверно',
    'Exception': 'Пришло что-то не то :)'
}


class AuthorizeVertex(BaseActionVertex):
    def activation_function(self, request: QueryRequest, context: Context) -> QueryResult:
        return QueryResult(StatusTypes.NEIGHBOUR, [string_auth_response], [None], [])

    def predict_is_suitable_input(self, request: QueryRequest, context: Context) -> bool:
        return request.question == self.name or request.question == self.alternative_name


class AuthorizeConclusionVertex(BaseActionVertex):
    def activation_function(self, request: QueryRequest, context: Context) -> QueryResult:
        if request.request_type == RequestType.STRING:
            return self.validate_key(request.question)
        if request.request_type == RequestType.PHOTO:
            pass  # преобразовать фото к тексту и сделать то же самое
        else:
            return QueryResult(StatusTypes.LEAF, [string_auth_end_response.get('Exception')], [None]
                               )

    def predict_is_suitable_input(self, request: QueryRequest, context: Context) -> bool:
        return True

    @staticmethod
    def validate_key(user_key: str) -> QueryResult:
        enter_result = ConferenceApi.is_correct_key(user_key)
        if enter_result:
            key = enter_result.conf_id
            return QueryResult(StatusTypes.LEAF, ['AUTH OK', key, string_auth_end_response.get('Success')],
                               [None, None, None], [])
        else:
            return QueryResult(StatusTypes.LEAF, [string_auth_end_response.get('Failure')], [None], [])
