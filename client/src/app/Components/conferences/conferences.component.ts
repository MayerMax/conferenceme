import { Component, OnInit } from '@angular/core';
import {Conference} from "../../constructor/models/Conference";
import {StoreConferencesService} from "../../services/store-conferences.service";
import {StoreService} from "../../services/store.service";

@Component({
  selector: 'app-conferences',
  templateUrl: './conferences.component.html',
  styleUrls: ['./conferences.component.css']
})
export class ConferencesComponent implements OnInit {

  editLecture : any;
  conferences: Conference[];
  loading: boolean;
  constructor(private storeService: StoreConferencesService) {
  }

  ngOnInit() {
    this.loading =true;
    this.storeService.getData();
    this.storeService.ConferencesSubject$.subscribe(
      conferences => {
        this.conferences = conferences;
        this.loading = false;
        console.log(conferences);
      }
    )
    // if ( this.storeService.Loading === true ) {
    //   this.storeService.getData(0).subscribe(
    //     data => {
    //       this.storeService.Loading = false;
    //       this.loading = false;
    //       this.lectures = this.storeService.Conference.lectures;
    //       // this.newSpeakerComponent = NewSpeakerComponent;
    //     }
    //   );
    // }
    // else {
    //   this.loading = false;
    //   this.lectures = this.storeService.Conference.lectures;
    //   // this.newSpeakerComponent = NewSpeakerComponent;
    // }
  }

}
