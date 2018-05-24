import {Speaker} from "./speaker";
import {Photo} from "./photo";

export class Speakers {
  speakers:  Array<Speaker>;
  constructor() {
    this.speakers = new Array<Speaker>();
    let speaker = new Speaker();
    console.log(speaker);
    this.speakers.push(speaker);
    // for ( let i = 1; i < 6; i++) {
    //   let sp = new Speaker
    //   (i, i, i, i, 'https://uploadrb.ru/upload/admins/picture/1237/507ab9f409db99d5aaeb46f8652c72d0.jpg', 'Иван', 'Иванов', 'Иваныч',
    //     'Работет в Максим Банке. Ис. Исполнительный директор и соучредитель. Банкир.', ['fd', 'fg'], [], 'Работет в Максим Банке. Ис. Исполнительный директор и соучредитель',
    //     'банкир' );
    //   this.speakers.push(sp);
    // }
  }
}
