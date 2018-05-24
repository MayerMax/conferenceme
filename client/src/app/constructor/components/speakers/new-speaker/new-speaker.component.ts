import {Component, ElementRef, Inject, Input, OnInit, ViewChild} from '@angular/core';
import {COMMA, ENTER} from "@angular/cdk/keycodes";
import {FormGroup} from "@angular/forms";
import {FileUploader} from "ng2-file-upload";
import {
  MAT_DIALOG_DATA, MatChipInputEvent, MatDialog, MatDialogConfig, MatDialogRef,
  MatStepperIntl
} from "@angular/material";
import {ActivatedRoute, Router} from "@angular/router";
import {Speaker} from "../../../models/speaker";
import {PostDataService} from "../../../../services/post-data.service";
import {StoreService} from "../../../../services/store.service";
const URL = 'http://localhost';
@Component({
  selector: 'app-new-speaker',
  templateUrl: './new-speaker.component.html',
  styleUrls: ['./new-speaker.component.css'],

})
export class NewSpeakerComponent implements OnInit {
  selectedLecture: number;
  file: any;
  type: any;
  name: string;
  @ViewChild('img') img : ElementRef;
  sendData = false;
  lectures: object[];
  visible: boolean = true;
  selectable: boolean = true;
  removable: boolean = true;
  addOnBlur: boolean = true;
  separatorKeysCodes = [ENTER, COMMA];
  @ViewChild('f') form: FormGroup;
  model: Speaker;
  idConference: number;
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
    @Inject(MAT_DIALOG_DATA) public data: any,private storeConference :StoreService,
    private router: Router, public dialog: MatDialog, private postService: PostDataService,private activatedRoute: ActivatedRoute) {
    this.activatedRoute.params.subscribe( val=> this.idConference = parseInt(val.id));
    console.log( this.activatedRoute.params);
  }

  onNoClick(): void {
    this.dialogRef.close();
  }
  onReset() {
    this.model = new Speaker();
  }
  onSubmit() {
    this.model.photo = this.img.nativeElement.src;
    console.log(JSON.stringify(this.model));
    this.storeConference.ConferenceSubject$.subscribe(
      conference => {
       conference.speakers.unshift(this.model);
       this.storeConference.updateConfernce(conference);
      }
      )}
    canDeactivate() {
      console.log(this.form.dirty);
      return this.sendData || !this.form.touched ;
    }
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
     this.storeConference.ConferenceSubject$.subscribe(
      conference => this.lectures = conference.lectures.map((item)=>{
        this.model = new Speaker
        (conference.id, 0, 9, '', '', '', '', '', );
        return {id: item.id, topic: item.topic}
      })
    )
    //  this.getData.getData(this.router.url).subscribe(
    //    data => { this.model = data; }
    // );
  }

}
