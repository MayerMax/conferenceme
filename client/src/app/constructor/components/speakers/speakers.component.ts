import {Component, DoCheck, OnDestroy, OnInit} from '@angular/core';
import {ActivatedRoute, Router} from "@angular/router";
import {Speakers} from "../../models/Speakers";
import {NewSpeakerComponent} from "./new-speaker/new-speaker.component";
import {MyMatPaginatorIntl} from "../../Intl/MyMatPaginatorIntl";
import {MatPaginatorIntl} from "@angular/material";
import {GetDataService} from "../../../services/get-data.service";
import {Speaker} from "../../models/speaker";
import {StoreService} from "../../../services/store.service";
@Component({
  selector: 'app-speakers',
  templateUrl: './speakers.component.html',
  styleUrls: ['./speakers.component.css'],
  providers: [{provide: MatPaginatorIntl, useClass: MyMatPaginatorIntl}],
})
export class SpeakersComponent implements OnInit, DoCheck {
  newSpeakerComponent: any;
  speakers: Speaker[];
  loading: boolean = true;
  idConference: number;
  lectureId: number;
  constructor(private  activatedRoute: ActivatedRoute, private router: Router,private getDataService: GetDataService,private storeService: StoreService) {
    this.activatedRoute.params.subscribe( params=> {this.idConference = parseInt(params.id); console.log(params) });
    this.activatedRoute.queryParams.subscribe(params => {this.lectureId =params['lectureId']})
  }

  // navigate(speaker: Speaker) {
  //   this.router.navigate
  //   (['/constructor/conference', speaker.conference_id, 'section', speaker.section_id, 'lecture', speaker.lection_id,
  //     'speaker', speaker.id] );
  // }

  ngOnInit() {
    console.log('ds');
    this.newSpeakerComponent = NewSpeakerComponent;
    this.storeService.getData(this.idConference);
    this.storeService.ConferenceSubject$.subscribe(
      conference => {
        if (conference != null) {
          this.speakers =  Object.assign(conference.speakers);
          console.log(this.speakers );
          this.loading = false;
        }
      }
    )
  }
  ngDoCheck(){
    if(this.lectureId != null)
      this.speakers= this.speakers.filter((speaker)=> speaker.lection_id == this.lectureId)
    else  this.storeService.ConferenceSubject$.subscribe(
      conference => {
        if (conference != null) {
          this.speakers =  Object.assign(conference.speakers);
          console.log(this.speakers );
          this.loading = false;
        }
      }
    )
  }
    // this.loading =true;
    // this.newSpeakerComponent = NewSpeakerComponent;
    // console.log( this.storeService);
    // if ( this.storeService.Loading === true ) {
    //   this.storeService.getData(this.idConference).subscribe(
    //     data => {
    //       this.loading = false;
    //       this.storeService.Loading = false;
    //       this.speakers = this.storeService.Conference.speakers;
    //       this.newSpeakerComponent = NewSpeakerComponent;
    //     }
    //   );
    // }
    // else {
    //   this.loading = false;
    //   this.speakers = this.storeService.Conference.speakers;
    // }


}
