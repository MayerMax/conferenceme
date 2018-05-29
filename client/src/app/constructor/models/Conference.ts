import {Lecture} from "./lecture";
import {Speaker} from "./speaker";

export class Conference{
  public id :number;
  public logo : string;
  public name: string;
  public topics: string;
  public begin_date: Date;
  public begin_time: Date;
  public end_date: Date;
  public location: string;
  public lectures: Lecture[];
  public speakers: Speaker[];
  public sections: any;
  constructor(
                id = 0,
                name = 'статусе реальности в искусстве',
                topics = ' Европе Европейская живопись ьство прошлого, открытие современности. Лектор - Илья Доронченков - профессор факультета истории искусств Европейского университета в Санкт-Петербурге.\'\n',
                begin_date = new Date(),
                end_date = new Date(),
                sections = [],
                lectures = [],
                speakers = [],
                logo = '../../../../assets/sber.png'

  ) {
    this.id= id;
    this.name = name;
    this.topics = topics;
    this.begin_date= begin_date;
    this.end_date = end_date;
    this.sections = sections;
    this.lectures = lectures;
    this.speakers = speakers;
    this.logo = logo;
  }
  public static parseDate(date){
    return  new Date(date);
  }
}
