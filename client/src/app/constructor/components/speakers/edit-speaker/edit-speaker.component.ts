import {Component, Inject, Input, OnInit, ViewChild} from '@angular/core';
import {MAT_DIALOG_DATA, MatChipInputEvent, MatDialog, MatDialogConfig, MatDialogRef} from "@angular/material";
// import {GetDataService} from "../../../services/get-data.service";
import {Router} from "@angular/router";
import {COMMA, ENTER} from "@angular/cdk/keycodes";
import {Speaker} from "../../../models/speaker";
import {FormGroup} from "@angular/forms";
import {FileUploader} from "ng2-file-upload";
// import {CanComponentDeactivate} from "../../../services/can-deactive-guard.service";
const URL = 'http://localhost';
@Component({
  selector: 'app-edit-speaker',
  templateUrl: './edit-speaker.component.html',
  styleUrls: ['./edit-speaker.component.css']
})
export class EditSpeakerComponent implements OnInit {
  file: any;
  type: any;
  name: string;
  sendData = false;
  visible: boolean = true;
  selectable: boolean = true;
  removable: boolean = true;
  addOnBlur: boolean = true;
  separatorKeysCodes = [ENTER, COMMA];
  @Input() speakers: Speaker[];
  @ViewChild('f') form: FormGroup;
  model: Speaker;
  public uploader: FileUploader = new FileUploader({url: URL});
  public hasBaseDropZoneOver: boolean = false;
  public fileOverBase(e): void {
    this.hasBaseDropZoneOver = e;
    if (this.uploader.queue.length !== 0) {
      this.file = this.uploader.queue[this.uploader.queue.length - 1]._file;
      this.type = 'image';
    }
  }
  constructor(
    public dialogRef: MatDialogRef<EditSpeakerComponent>,
    @Inject(MAT_DIALOG_DATA) public data: any, private router: Router, public dialog: MatDialog) {
    this.model = data.speaker ;
  }

  onNoClick(): void {
    this.dialogRef.close();
  }
  onSubmit() {
    console.log(this.uploader.queue[0]._file);
    let ar = this.uploader.queue;
    this.uploader.uploadAll();
    this.form.reset();
    this.router.navigateByUrl('lecture');

  }
  canDeactivate() {
    console.log(this.form.dirty);
    return this.sendData || !this.form.touched ;
  }
  // openDialog() {
  //   let dialogRef = this.dialog.open(DialogOverviewExampleDialogComponent,  {
  //     width: '100vw',
  //     height: '96vh',
  //     data: {
  //       speaker: this.model
  //     }
  //   } as MatDialogConfig<any>);
  // }
  addTag(event: MatChipInputEvent): void {
    let input = event.input;
    let value = event.value;

    // Add our fruit
    if ((value || '').trim()) {
      this.model.tagsSpeaker.push(value.trim());
    }

    // Reset the input value
    if (input) {
      input.value = '';
    }
  }

  removeTag(tag: any): void {
    let index = this.model.tagsSpeaker.indexOf(tag);

    if (index >= 0) {
      this.model.tagsSpeaker.splice(index, 1);
    }
  }
  addLink(event: MatChipInputEvent): void {
    let input = event.input;
    let value = event.value;

    // Add our fruit
    if ((value || '').trim()) {
      this.model.link.push(value.trim());
    }

    // Reset the input value
    if (input) {
      input.value = '';
    }
  }

  removeLink(tag: any): void {
    let index = this.model.link.indexOf(tag);

    if (index >= 0) {
      this.model.link.splice(index, 1);
    }
  }
  ngOnInit() {
    // this.model = new Speaker();
    //  this.getData.getData(this.router.url).subscribe(
    //    data => { this.model = data; }
    // );
  }

}
