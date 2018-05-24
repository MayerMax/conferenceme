import {Component, Input, OnInit} from '@angular/core';
import {ActivatedRoute, Router} from "@angular/router";
import {MatDialog, MatDialogConfig} from "@angular/material";
import {Lecture} from "../../../models/lecture";
import {EditLectureComponent} from "./edit-lecture/edit-lecture.component";
import {StoreService} from "../../../../services/store.service";
@Component({
  selector: 'app-lecture-card',
  templateUrl: './lecture-card.component.html',
  styleUrls: ['./lecture-card.component.css']
})
export class LectureCardComponent implements OnInit {

  @Input() lecture: Lecture;
  constructor(private  route: ActivatedRoute, private router: Router, public dialog: MatDialog,private  store: StoreService ) {

  }
  navigate() {
    this.router.navigate([{outlets: {primary: `constructor/conference/${this.lecture.conference_id}/speakers`,sidemenu: 'constructor' }}],
      {queryParams: {lectureId: this.lecture.id}});
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

  }
}
