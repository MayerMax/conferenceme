import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import {ConstructorComponent} from "./components/constructor/constructor.component";
import {SpeakersComponent} from "./components/speakers/speakers.component";
import {LecturesComponent} from "./components/lectures/lectures.component";
import {NavBarConstructorComponent} from "../nav-bar/components/nav-bar/nav-bar-constructor/nav-bar-constructor.component";

const constructorRoutes: Routes = [
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
      // {
      //   path: 'conference/:id/sections',
      //   component: SectionsComponent
      // },
      {
        path: 'conference/:id/speakers',
        outlet: 'sidemenu',
        component: NavBarConstructorComponent
      },
      {
        path: 'conference/:id/lectures',
        outlet: 'sidemenu',
        component: NavBarConstructorComponent
      },
      {
        path: 'conference/:id/sections',
        outlet: 'sidemenu',
        component: NavBarConstructorComponent
      }
    ]
  },
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
