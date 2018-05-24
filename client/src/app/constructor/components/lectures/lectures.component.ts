import {Component, OnDestroy, OnInit, Type} from '@angular/core';
import {Lectures} from "../../models/lectures";
import {EditLectureComponent} from "./lecture-card/edit-lecture/edit-lecture.component";
import {ComponentType} from "@angular/core/src/render3";
import {NewSpeakerComponent} from "../speakers/new-speaker/new-speaker.component";
import {StoreService} from "../../../services/store.service";
import {Lecture} from "../../models/lecture";
import NewCommand from "@angular/cli/commands/new";
import {NewLectureComponent} from "./lecture-card/new-lecture/new-lecture.component";
import {ActivatedRoute} from "@angular/router";

@Component({
  selector: 'app-lectures',
  templateUrl: './lectures.component.html',
  styleUrls: ['./lectures.component.css']
})
export class LecturesComponent implements OnInit {
  editLecture : any;
  lectures: Lecture[];
  loading: boolean = true;
  idConference: number;
  constructor(private storeService : StoreService, private activatedRoute: ActivatedRoute ) {
    this.activatedRoute.params.subscribe( val=> this.idConference = parseInt(val.id));
  }

  ngOnInit() {
    this.editLecture = NewLectureComponent;
    this.storeService.getData(this.idConference);
    this.storeService.ConferenceSubject$.subscribe(
      conference => {
        if (conference != null) {
          this.lectures = conference.lectures;
          this.loading = false;
        }
      }
    )
  }
    // this.editLecture = NewLectureComponent;
    // console.log( this.storeService);
    // if ( this.storeService.Loading === true ) {
    //   this.storeService.getData(this.idConference).subscribe(
    //     data => {
    //       this.storeService.Loading = false;
    //       this.loading = false;
    //       this.lectures = this.storeService.Conference.lectures;
    //       // this.newSpeakerComponent = NewSpeakerComponent;
    //     },
    //   );
    // }
    // else {
    //   this.loading = false;
    //   this.lectures = this.storeService.Conference.lectures;
    //   // this.newSpeakerComponent = NewSpeakerComponent;
    // }


}
