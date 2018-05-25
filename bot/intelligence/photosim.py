import os
from collections import OrderedDict
from typing import List, Union

import face_recognition
from numpy.core.multiarray import ndarray

EXTENSIONS = {'.png', '.bmp', '.jpeg', '.jpg'}


class EmptyDirectoryError(BaseException):
    pass


class NotSupportedExtensionError(BaseException):
    pass


class ConferencePhotoModel:
    def __init__(self, img_dir: str, recursive: bool = False):
        """
        Класс, который хранит в себе векторные признаки известных лиц, фото которых расположено в папке img_path
        :param img_dir: Директория, в которой лежат фото известных лиц
        :param recursive: если True, то рекурсивно обходит директорию, собираю все фотографии
        """
        self.__img_path = img_dir
        self.__recursive = recursive
        if not recursive:
            self.__path_files = ConferencePhotoModel.get_images_from_directory(img_dir, EXTENSIONS)
        else:
            self.__path_files = ConferencePhotoModel.get_images_from_traversed_directory(img_dir, EXTENSIONS)

        if not self.__path_files:
            raise EmptyDirectoryError('no images were found!')

        self.__loaded_images = [face_recognition.load_image_file(image) for image in self.__path_files]

        # хранит в себе по числовому ключу ссылку на вектор признаков фотографии
        self.__face_encodings = OrderedDict({index: face_recognition.face_encodings(image)[0]
                                             for index, image in enumerate(self.__loaded_images)})

    @staticmethod
    def get_images_from_directory(directory_path: str, supported_extensions: set) -> List[str]:
        """
        Возвращает все файлы (имена), которые удовлетворяют допустимым расширениям
        :param directory_path: путь до директории
        :param supported_extensions: расширения файлов, которые допустимы
        :return: список имен файлов
        """
        result_files = []
        for file in os.listdir(directory_path):
            file_path, extension = os.path.splitext(file)
            if extension in supported_extensions:
                result_files.append(os.path.join(directory_path, file))
        return result_files

    @staticmethod
    def get_images_from_traversed_directory(directory_path: str, supported_extensions: set) -> List[str]:
        """
        Возвращает все файлы (имена), которые удовлетворяют допустимым расширениям, сделав полный обход директории
        :param directory_path: путь до директории
        :param supported_extensions: расширения файлов, которые допустимы
        :return: список имен файлов
        """
        result_files = []
        for root, _, files in os.walk(directory_path):
            for f in files:
                file_path, extension = os.path.splitext(f)
                if extension in supported_extensions:
                    result_files.append(os.path.join(root, f))
        return result_files

    def find_relevant_face(self, img: Union[str, ndarray]) -> Union[List[str], None]:
        """
        возвращает список фотографий известных лиц, схожесть которых с фото img_path по евклидовой метрике не превышает
        0.55. Предполагается, что на фото изображен ровно один человек
        :param img: путь до изображения или само изображение
        :return: список путей до похожих фото или None, если таких не нашлось
        """
        given_image = ConferencePhotoModel.__img_loader(img)
        face_encoding = face_recognition.face_encodings(given_image)[0]
        return self.__find_relevant_face(face_encoding)

    def find_relevant_faces(self, img: Union[str, ndarray]) -> Union[List[str], None]:
        """
        находит пути до изображений всех лиц людей, которые есть на фото и возвращает список результатов.
        Предполагается, что на фото присутствует более одного человека; в противном случае использовать -
        find_relevant_face
        :param img: путь до изображения или матричное представление изображения
        :return: лист путей до изображений лиц на данном фото
        """
        given_image = ConferencePhotoModel.__img_loader(img)
        all_found_faces_encodings = face_recognition.face_encodings(given_image)

        result = [self.__find_relevant_face(face_encoding) for face_encoding in all_found_faces_encodings]
        unique_faces_result = [paths[0] for paths in result if paths]
        return unique_faces_result

    def __find_relevant_face(self, face_encoding: ndarray) -> Union[List[str], None]:
        """
        находит среди дескрипторов известных лиц самое подходящее (порог 0.55 по евклиду) и возвращает список
        релевантных фото (путей до них) или же None, если ничего не нашлось
        :param face_encoding: вектор дескрипторов лица
        :return: лист путей до изображений или None
        """
        distances = face_recognition.face_distance(list(self.__face_encodings.values()), face_encoding)
        sorted_distances_with_index = sorted(((i, dist) for i, dist in enumerate(distances)),
                                             key=lambda x: x[1])
        relevant_photo_path_indexes = [idx for idx, dist in sorted_distances_with_index if dist <= 0.55]
        if not relevant_photo_path_indexes:
            return None
        return [self.__path_files[idx] for idx in relevant_photo_path_indexes]

    @staticmethod
    def __img_loader(img: Union[str, ndarray]) -> ndarray:
        """
        Внутрення функция проверки того, подана ли фотография, выбрасывает исключение, если выдано не изображение
        :param img: путь до изображения или само изображение
        :return: возвращает представление изображения в виде матрицы
        """
        if type(img) == str:
            _, ext = os.path.splitext(img)
            if ext not in EXTENSIONS:
                raise NotSupportedExtensionError('the file you provide is not supported')
            given_image = face_recognition.load_image_file(img)
        elif type(img) == ndarray:
            given_image = img
        else:
            raise FileNotFoundError('no file provided')
        return given_image


if __name__ == '__main__':
    m = ConferencePhotoModel('../intelligence')
    results = m.find_relevant_faces('../intelligence/test_dir/lena_and_max.jpg')
    print(results)