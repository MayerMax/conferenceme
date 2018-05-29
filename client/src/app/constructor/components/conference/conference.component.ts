import {Component, OnInit, ViewChild} from '@angular/core';
import {StoreService} from "../../../services/store.service";
import {FormGroup} from "@angular/forms";
import {Conference} from "../../models/Conference";
import {ActivatedRoute} from "@angular/router";
import {FileUploader} from "ng2-file-upload";
import {AmazingTimePickerService} from "amazing-time-picker";
const URL = '';
@Component({
  selector: 'app-conference',
  templateUrl: './conference.component.html',
  styleUrls: ['./conference.component.css']
})
export class ConferenceComponent implements OnInit {

  @ViewChild('f') form: FormGroup;
  model: Conference;
  loading: boolean;
  file: any;
  type: any;
  idConfernce: number;
  public uploader: FileUploader = new FileUploader({url: URL});
  public hasBaseDropZoneOver: boolean = false;
  public fileOverBase(e): void {
    this.hasBaseDropZoneOver = e;
    if (this.uploader.queue.length !== 0) {
      this.file = this.uploader.queue[this.uploader.queue.length - 1]._file;
      this.type = 'image';
    }
  }
  constructor(private  storeService: StoreService, private activatedRoute: ActivatedRoute,private atp:AmazingTimePickerService) {
    this.activatedRoute.params.subscribe(val => {
      this.idConfernce = parseInt(val.id);
      }
    );

  }

  ngOnInit() {
    this.loading = true;
    this.storeService.getData(this.idConfernce);
    this.storeService.ConferenceSubject$.subscribe(
      conference => {
        if (conference != null) {
          this.model = conference;
          this.loading = false;
        }
      }
    )


    // if (this.idConfernce == 0) {
    //   this.storeService.Loading = false;
    //   this.storeService.Conference = new Conference();
    //   this.model =  this.storeService.Conference;
    // }
    // else {
    //   this.loading = true;
    //   if (this.storeService.Loading === true) {
    //     this.storeService.getData(this.idConfernce).subscribe(
    //       data => {
    //         this.storeService.Loading = false;
    //         this.loading = false;
    //         this.model = this.storeService.Conference;
    //         // this.newSpeakerComponent = NewSpeakerComponent;
    //       }
    //     );
    //   }
    //   else {
    //     this.loading = false;
    //     this.model = this.storeService.Conference;
    //     // this.newSpeakerComponent = NewSpeakerComponent;
    //   }
    // }
  }

  onSubmit() {
    this.storeService.ConferenceSubject$.subscribe(
      conference => {
        conference = this.model;
        this.storeService.updateConfernce(conference);
      }
    )
  }
}
    // this.router.navigateByUrl('lecture');

