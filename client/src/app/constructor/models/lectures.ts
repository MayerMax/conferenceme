import {Lecture} from "./lecture";
import {Photo} from "./photo";

export class Lectures {
  public lectures: Array<Lecture>;

  constructor() {
    this.lectures = new Array<Lecture>();
    for (let i = 1; i < 4; i++) {
      let lecture = new Lecture();
      this.lectures.push(lecture);
    }
  }
}
