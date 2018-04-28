export class Speaker {
  public conference_id: number;
  public section_id: number;
  public lection_id: number;
  public id: number;
  public photoSrc: string;
  public  name: string ;
  public  surName: string ;
  public  otchestvo: string;
  public  info: string;
  public  tagsSpeaker: String[];
  public  link: string[];
  public shortInformation: string;
  public  profession: string;
  constructor(
    conference_id = 0,
    section_id = 0,
    lection_id = 0,
    id = 0,
    photoSrc = '',
    name = '',
    surName = '',
    otchestvo = '',
    informationSpeaker = '',
    tagsSpeaker = [],
    link = [],
    shortInformation = '',
    profession = ''
  ) {
    this.profession = profession;
    this.conference_id = conference_id;
    this.section_id = section_id;
    this.lection_id = lection_id;
    this.id = id;
    this.shortInformation = shortInformation;
    this.name = name;
    this.surName = surName;
    this.info = informationSpeaker;
    this.link = link;
    this.otchestvo = otchestvo;
    this.tagsSpeaker = tagsSpeaker;
    this.photoSrc = photoSrc;
  }
}
