import {Component, OnInit, Type} from '@angular/core';
import {Lectures} from "../../models/lectures";
import {EditLectureComponent} from "./lecture-card/edit-lecture/edit-lecture.component";
import {ComponentType} from "@angular/core/src/render3";
import {NewSpeakerComponent} from "../speakers/new-speaker/new-speaker.component";

@Component({
  selector: 'app-lectures',
  templateUrl: './lectures.component.html',
  styleUrls: ['./lectures.component.css']
})
export class LecturesComponent implements OnInit {
  editLecture : any;
  lectures: Lectures;
  constructor() {
  }

  ngOnInit() {
    this.lectures = new Lectures();
    // this.editLecture = NewSpeakerComponent;
  }

}
