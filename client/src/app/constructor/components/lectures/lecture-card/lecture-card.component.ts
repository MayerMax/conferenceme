import {Component, Input, OnInit} from '@angular/core';
import {ActivatedRoute, Router} from "@angular/router";
import {MatDialog, MatDialogConfig} from "@angular/material";
import {Lecture} from "../../../models/lecture";
import {EditLectureComponent} from "./edit-lecture/edit-lecture.component";
@Component({
  selector: 'app-lecture-card',
  templateUrl: './lecture-card.component.html',
  styleUrls: ['./lecture-card.component.css']
})
export class LectureCardComponent implements OnInit {

  @Input() lecture: Lecture;
  constructor(private  route: ActivatedRoute, private router: Router, public dialog: MatDialog) {

  }

  openDialog() {
    let dialogRef = this.dialog.open(EditLectureComponent, {
      width: '70vw',
      height: '89vh',
      data: {
        lecture: this.lecture,
      },
      panelClass: 'dialog-no-padding-panel'
    } as MatDialogConfig<any>);
    dialogRef.afterClosed().subscribe(result => {
      console.log('The dialog was closed');
    });
  }

  ngOnInit() {
    console.log(this.lecture.date.getTime());
  }
}
