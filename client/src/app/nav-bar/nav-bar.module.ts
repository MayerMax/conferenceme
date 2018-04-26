import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import {RouterModule} from "@angular/router";
import {MatButtonModule, MatIconModule} from "@angular/material";
import { NavBarComponent } from './components/nav-bar/nav-bar.component';
import { NavBarConstructorComponent } from './components/nav-bar/nav-bar-constructor/nav-bar-constructor.component';
import { NavBarHeaderComponent } from './components/nav-bar/nav-bar-header/nav-bar-header.component';
import {HeaderComponent} from "./components/header/header.component";

@NgModule({
  imports: [
    CommonModule,
    RouterModule,
    MatButtonModule,
    MatIconModule
  ],
  declarations: [NavBarComponent, NavBarConstructorComponent, NavBarHeaderComponent, HeaderComponent],
  exports: [CommonModule, NavBarHeaderComponent, NavBarComponent,HeaderComponent]
})
export class NavBarModule { }
