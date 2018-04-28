import {Component, Inject, Input, OnInit, ViewChild} from '@angular/core';
import {COMMA, ENTER} from "@angular/cdk/keycodes";
import {FormGroup} from "@angular/forms";
import {FileUploader} from "ng2-file-upload";
import {
  MAT_DIALOG_DATA, MatChipInputEvent, MatDialog, MatDialogConfig, MatDialogRef,
  MatStepperIntl
} from "@angular/material";
import {Router} from "@angular/router";
import {Speaker} from "../../../models/speaker";
const URL = 'http://localhost';
@Component({
  selector: 'app-new-speaker',
  templateUrl: './new-speaker.component.html',
  styleUrls: ['./new-speaker.component.css']
})
export class NewSpeakerComponent implements OnInit {

  file: any;
  type: any;
  name: string;
  sendData = false;
  visible: boolean = true;
  selectable: boolean = true;
  removable: boolean = true;
  addOnBlur: boolean = true;
  separatorKeysCodes = [ENTER, COMMA];
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
    public dialogRef: MatDialogRef<NewSpeakerComponent>,
    @Inject(MAT_DIALOG_DATA) public data: any, private router: Router, public dialog: MatDialog) {
  }

  onNoClick(): void {
    this.dialogRef.close();
  }
  onReset() {
    this.model = new Speaker();
  }
  onSubmit() {
    console.log(this.uploader.queue[0]._file);
    let ar = this.uploader.queue;
    this.uploader.uploadAll();
    this.form.reset();
    console.log(this.model);
    this.router.navigateByUrl('lecture');

  }
  // canDeactivate() {
  //   console.log(this.form.dirty);
  //   return this.sendData || !this.form.touched ;
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
    this.model = new Speaker
    (0, 0, 0, 0, '', '', '', '', '', );

    //  this.getData.getData(this.router.url).subscribe(
    //    data => { this.model = data; }
    // );
  }

}
