import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import {ConstructorComponent} from "./components/constructor/constructor.component";
import {SpeakersComponent} from "./components/speakers/speakers.component";
import {LecturesComponent} from "./components/lectures/lectures.component";
import {NavBarConstructorComponent} from "../nav-bar/components/nav-bar/nav-bar-constructor/nav-bar-constructor.component";
import {ConferenceComponent} from "./components/conference/conference.component";
import {NewConferenceComponent} from "./components/conference/new-conference/new-conference.component";

const constructorRoutes: Routes = [

  {
    path: '',
    redirectTo: 'conference/0',
    pathMatch: 'full'
  },
  {
    path: '',
    component: ConstructorComponent,
    children: [
      {
        path: 'conference/:id/speakers',
        component: SpeakersComponent
      },
      {
        path: 'conference/:id/lectures',
        component: LecturesComponent
      },
      {
        path: 'new_conference',
        component: NewConferenceComponent
      },
      {
        path: 'conference/:id',
        component: ConferenceComponent
      },
      {
        path: 'conference',
        outlet: 'sidemenu',
        component: NavBarConstructorComponent
      }
    ]
  }
  // {
  //   path: '',
  //   outlet: 'sidemenu',
  //   component: NavBarContentComponent,
  // }
];
@NgModule({
  imports: [RouterModule.forChild(constructorRoutes)],
  exports: [RouterModule]
})
export class ConstructorRoutingModule { }
