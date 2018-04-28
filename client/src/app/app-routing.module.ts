import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import {MainComponent} from "./Components/main/main.component";
import {NavBarComponent} from "./nav-bar/components/nav-bar/nav-bar.component";
import {RouterModule, Routes} from "@angular/router";
import {NavBarConstructorComponent} from "./nav-bar/components/nav-bar/nav-bar-constructor/nav-bar-constructor.component";
import {HomeComponent} from "./Components/home/home.component";

const appRoutes: Routes = [
  {
    path: 'constructor',
    loadChildren: 'app/constructor/constructor.module#ConstructorModule'
  },
  {
    path: 'constructor',
    outlet: 'sidemenu',
    component: NavBarConstructorComponent
  },
  {
    path: '',
    redirectTo: '/home',
    pathMatch: 'full'
  },
  // {
  //   path: 'landing',
  //   component: LandingComponent
  // },

  {
    path: '',
    component: MainComponent,
  },
  {
    path: '',
    outlet: 'sidemenu',
    component: NavBarComponent
  },
  {
    path: 'home',
    component: HomeComponent,
  },
  {
    path: 'home',
    outlet: 'sidemenu',
    component: NavBarComponent
  }
  // {
  //   path: 'calendar',
  //   component: CalendarComponent
  // }
];

@NgModule({
  imports: [RouterModule.forRoot(appRoutes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
