import { Component, OnInit } from '@angular/core';
import {ActivatedRoute, Router} from "@angular/router";
import {Speakers} from "../../models/Speakers";
@Component({
  selector: 'app-speakers',
  templateUrl: './speakers.component.html',
  styleUrls: ['./speakers.component.css']
})
export class SpeakersComponent implements OnInit {

  speakers: Speakers;

  constructor(private  route: ActivatedRoute, private router: Router) { }
  // navigate(speaker: Speaker) {
  //   this.router.navigate
  //   (['/constructor/conference', speaker.conference_id, 'section', speaker.section_id, 'lecture', speaker.lection_id,
  //     'speaker', speaker.id] );
  // }

  ngOnInit() {
    this.speakers = new Speakers();
  }

}
