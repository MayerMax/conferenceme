import {Component, ElementRef, Inject, OnInit, ViewChild} from '@angular/core';
import {COMMA, ENTER} from "@angular/cdk/keycodes";
import {FormGroup} from "@angular/forms";
import {Lecture} from "../../../../models/lecture";
import {FileUploader} from "ng2-file-upload";
import {MAT_DIALOG_DATA, MatChipInputEvent, MatDialog, MatDialogRef} from "@angular/material";
import {Router} from "@angular/router";
import {StoreService} from "../../../../../services/store.service";
const URL = 'http://localhost';
@Component({
  selector: 'app-edit-lecture',
  templateUrl: './edit-lecture.component.html',
  styleUrls: ['./edit-lecture.component.css']
})
export class EditLectureComponent implements OnInit {
@ViewChild('srcPhoto')
  srcPhoto: ElementRef;
  file: any;
  type: any;
  name: string;
  sendData = false;
  selectable: boolean = true;
  removable: boolean = true;
  addOnBlur: boolean = true;
  public hasBaseDropZoneOver: boolean = false;
  separatorKeysCodes = [ENTER, COMMA];
  @ViewChild('f') form: FormGroup;
  model: Lecture;
  public uploaderPhoto: FileUploader = new FileUploader({url: URL});
  public uploaderFile: FileUploader = new FileUploader({url: URL});
  constructor(
    public dialogRef: MatDialogRef<EditLectureComponent>,
    @Inject(MAT_DIALOG_DATA) public data: any, private router: Router, public dialog: MatDialog,
    private storeConference: StoreService) {
    this.model = data.lecture;
  }
  public fileOverBase(e): void {
    this.hasBaseDropZoneOver = e;
    if (this.uploaderPhoto.queue.length !== 0) {
      this.file = this.uploaderPhoto.queue[0]._file;
      this.type = 'image';
    }
  }
  onNoClick(): void {
    this.dialogRef.close();
  }

  onSubmit() {
    console.log(this.srcPhoto);
    this.model.photo = this.srcPhoto.nativeElement.src;
    this.uploaderFile.cancelAll();
    console.log( JSON.stringify(this.model));
    this.storeConference.ConferenceSubject$.subscribe(
      conference => {
        conference.lectures[conference.lectures.findIndex((lecture)=> lecture.id === this.model.id)] = this.model;
        this.storeConference.updateConfernce(conference);
      });
  }
  // canDeactivate() {
  //   console.log(this.form.dirty);
  //   return this.sendData || !this.form.touched ;
  // }
  // openDialog() {
  //   let dialogRef = this.dialog.open(DialogOverviewExampleDialogComponent,  {
  //     width: '100vw',
  //     height: '96vh',
  //     data: {
  //       speaker: this.model
  //     }
  //   } as MatDialogConfig<any>);
  //   dialogRef.afterClosed().subscribe(result => {
  //     console.log('The dialog was closed');
  //     this.animal = result;
  //   });
  // }
  addTag(event: MatChipInputEvent): void {
    let input = event.input;
    let value = event.value;

    // Add our fruit
    if ((value || '').trim()) {
      this.model.tagsLecture.push(value.trim());
    }
    // Reset the input value
    if (input) {
      input.value = '';
    }
  }
  removeTag(tag: any): void {
    let index = this.model.tagsLecture.indexOf(tag);

    if (index >= 0) {
      this.model.tagsLecture.splice(index, 1);
    }
  }
  ngOnInit() {
    // this.model = new Speaker();
    //  this.getData.getData(this.router.url).subscribe(
    //    data => { this.model = data; }
    // );
  }

}
