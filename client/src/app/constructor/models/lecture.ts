import {Speaker} from "./speaker";
import {Photo} from "./photo";

export class Lecture {
  public conference_id: number;
  public nameSection: string;
  public id: number;
  public topic: string;
  public about: string;
  public date: Date;
  public duration: string;
  public tagsLecture: string[];
  public hallLecture: string;
  public  files: File[];
  public shortInfAboutLecture: string;
public  photo = 'http://www.manege.spb.ru/wp-content/uploads/2016/06/auditoriya.jpg';

  constructor(
    conference_id = 0,
    id = 0,
    topic = '',
    about = '',
    date = '',
    hallLecture = '',
    tagsLecture = [] ,
    shortInfAboutLecture = '',
    duration = '',
    photoSrc = '',
    ) {
    this.id = id;
    this.conference_id  = conference_id;
    this.photo = photoSrc;
    this.about = about;
    this.date = new Date(date);
    this.topic = topic;
    this.hallLecture = hallLecture;
    this.tagsLecture = [];
    this.shortInfAboutLecture = shortInfAboutLecture;
    this.duration = duration;
    this.tagsLecture = tagsLecture;
  }
}
