import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ConstructorRoutingModule } from './constructor-routing.module';
// import { ConferenceComponent } from './conference/conference.component';
// import {LectureComponent} from "../components/lecture/lecture.component";
// import {SpeakerComponent} from "../components/speaker/speaker.component";
// import {SpeakerElementComponent} from "../components/lecture/speaker-element/speaker-element.component";
import {FormsModule, ReactiveFormsModule} from "@angular/forms";
import {
  MatButtonModule, MatCardModule, MatChipsModule, MatDatepickerModule, MatDialogModule, MatExpansionModule,
  MatFormFieldModule,
  MatGridListModule,
  MatIconModule,
  MatInputModule, MatListModule, MatNativeDateModule, MatOptionModule, MatPaginatorIntl, MatPaginatorModule,
  MatSelectModule,
  MatSidenavModule, MatStepperIntl, MatStepperModule,
  MatToolbarModule
} from "@angular/material";
import {FileUploadModule} from "ng2-file-upload";
import {BrowserAnimationsModule} from "@angular/platform-browser/animations";
import {HttpClientModule} from "@angular/common/http";
// import {ImagePreviewDirective} from '../directive/image-preview.directive';
// import { ConstructorComponent } from './constructor/constructor.component';
// import { AddLectureComponent } from './add-lecture/add-lecture.component';
// import {SectionComponent} from "../components/section/section.component";
// import { SectionsComponent } from './conference/sections/sections.component';
// import { SpeakersComponent } from './conference/speakers/speakers.component';
// import {DialogOverviewExampleDialogComponent} from "../components/speaker/dialog-overview-example-dialog/dialog-overview-example-dialog.component";
// import {CanDeactiveGuardService} from "../services/can-deactive-guard.service";
import {AppModule} from "../app.module";
import {NavBarModule} from "../nav-bar/nav-bar.module";
import { ConferenceComponent } from './components/conference/conference.component';
import { ConstructorComponent } from './components/constructor/constructor.component';
import { SpeakersComponent } from './components/speakers/speakers.component';
import { LecturesComponent } from './components/lectures/lectures.component';
import { SpeakerCardComponent } from './components/speakers/speaker-card/speaker-card.component';
import { NewSpeakerComponent } from './components/speakers/new-speaker/new-speaker.component';
import { ToolbarConstructorComponent } from './components/toolbar-constructor/toolbar-constructor.component';
import { EditSpeakerComponent } from './components/speakers/edit-speaker/edit-speaker.component';
import { ImagePreviewDirective } from './directive/image-preview.directive';
import { LectureCardComponent } from './components/lectures/lecture-card/lecture-card.component';
import { EditLectureComponent } from './components/lectures/lecture-card/edit-lecture/edit-lecture.component';
import {MyMatPaginatorIntl} from "./Intl/MyMatPaginatorIntl";
import {GetDataService} from "../services/get-data.service";
import {MockGetDataService} from "../services/mock-get-data.service";
// import { SpeakerCardComponent } from './conference/speakers/speaker-card/speaker-card.component';
// import { ToolbarConferencesComponent } from './conference/toolbar-conferences/toolbar-conferences.component';
// import { LecturesComponent } from './conference/lectures/lectures.component';
// import { LectureCardComponent } from './conference/lectures/lecture-card/lecture-card.component';
// import { DialogLectureComponent } from './conference/lectures/dialog-lecture/dialog-lecture.component';
// import { SectionCardComponent } from './conference/sections/section-card/section-card.component';
// import { SectionDialogComponent } from './conference/sections/section-dialog/section-dialog.component';
// import {NavBarModule} from "../nav-bar/nav-bar.module";
// import {NavBarComponent} from "../nav-bar/nav-bar/nav-bar.component";
// import { NewSpeakerComponent } from './conference/speakers/speaker-card/new-speaker/new-speaker.component';
// import {MatStepperIntlMy} from "./conference/mat-stepper-intl-my";

@NgModule({
  imports: [
    CommonModule,
    ConstructorRoutingModule,
    FormsModule,
    MatFormFieldModule,
    MatDatepickerModule,
    FileUploadModule,
    MatButtonModule,
    MatIconModule,
    MatNativeDateModule,
    MatInputModule,
    ReactiveFormsModule,
    HttpClientModule,
    MatToolbarModule,
    MatIconModule,
    MatSidenavModule,
    MatListModule,
    MatCardModule,
    MatGridListModule,
    MatExpansionModule,
    MatOptionModule,
    MatSelectModule,
    MatDialogModule,
    MatChipsModule,
    MatPaginatorModule,
    NavBarModule,
    MatStepperModule
  ],
  entryComponents: [EditSpeakerComponent, NewSpeakerComponent, EditLectureComponent],
  providers: [{provide: GetDataService, useClass: MockGetDataService}],
  declarations: [ConferenceComponent, ConstructorComponent, SpeakersComponent, LecturesComponent, SpeakerCardComponent, NewSpeakerComponent, ToolbarConstructorComponent, EditSpeakerComponent, ImagePreviewDirective, LectureCardComponent, EditLectureComponent]
})
export class ConstructorModule { }
