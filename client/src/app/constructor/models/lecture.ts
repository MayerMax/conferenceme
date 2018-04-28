import {Speaker} from "./speaker";
import {Photo} from "./photo";

export class Lecture {
  public conference_id: number;
  public section_id: number;
  public nameSection: string;
  public nameSections:  Array<String>;
  public id: number;
  public topic: string;
  public about: string;
  public date: Date;
  public duration: string;
  public tagsLecture: string[];
  public hallLecture: string;
  public  files: File[];
  public shortInfAboutLecture: string;
public  photo = new Photo('http://www.manege.spb.ru/wp-content/uploads/2016/06/auditoriya.jpg');

  constructor(topic = 'статусе реальности в искусстве',
              about = '',
              dateLecture = new Date(),
              hallLecture = '9 кабинет',
              tagsLecture = [] ,
              shortInfAboutLecture = 'Европейская живопись XIX века: строительство прошлого, открытие современности. Лектор - Илья Доронченков - профессор факультета истории искусств Европейского университета в Санкт-Петербурге.',
              duration = '2 часа',
              photo = new Photo('http://www.manege.spb.ru/wp-content/uploads/2016/06/auditoriya.jpg')
              ) {
    this.id = 1;
    this.about = about;
    this.date = dateLecture;
    this.topic = topic;
    this.hallLecture = hallLecture;
    this.tagsLecture = [];
    this.shortInfAboutLecture = shortInfAboutLecture;
    this.duration = duration;
    this.photo = photo;
    this.tagsLecture = tagsLecture;
  }
}
