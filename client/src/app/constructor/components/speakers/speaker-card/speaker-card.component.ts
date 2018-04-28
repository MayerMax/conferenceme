import {Component, Input, OnInit} from '@angular/core';

import {MatDialog, MatDialogConfig} from "@angular/material";
import {ActivatedRoute, Router} from "@angular/router";
import {Speaker} from "../../../models/speaker";
import {EditSpeakerComponent} from "../edit-speaker/edit-speaker.component";

@Component({
  selector: 'app-speaker-card',
  templateUrl: './speaker-card.component.html',
  styleUrls: ['./speaker-card.component.css']
})
export class SpeakerCardComponent implements OnInit {
  @Input() speaker: Speaker;

  constructor(private  route: ActivatedRoute, private router: Router, public dialog: MatDialog) {
  }

  openDialog() {
    let dialogRef = this.dialog.open(EditSpeakerComponent, {
      data: {
        speaker: this.speaker
      },
      panelClass: 'dialog-no-padding-panel'
    } as MatDialogConfig<any>);
    dialogRef.afterClosed().subscribe(result => {
      console.log('The dialog was closed');
    });
    dialogRef.backdropClick().subscribe(
      result => {
        console.log('The dialog was clicked');
        console.log(result);
      });
  }
  ngOnInit() {}
}
