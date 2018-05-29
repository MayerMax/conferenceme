import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';


import { AppComponent } from './app.component';
import {FormsModule, ReactiveFormsModule} from "@angular/forms";
import {
  MatButtonModule, MatFormFieldModule, MatInputModule, MatProgressSpinnerModule,
  MatStepperModule
} from "@angular/material";
import { LoginComponent } from './Components/login/login.component';
import {RouterModule, Routes} from "@angular/router";
import {BrowserAnimationsModule} from "@angular/platform-browser/animations";
import {HTTP_INTERCEPTORS, HttpClientModule} from "@angular/common/http";
import {AuthInterceptorService} from "./services/auth-interceptor.service";
import { SignUpComponent } from './Components/sign-up/sign-up.component';
import { CompareFormControlDirective } from './directive/compare-form-control.directive';
import {EnsureAuthenticatedService} from "./services/ensure-authenticated.service";
import {NavBarModule} from "./nav-bar/nav-bar.module";
import { MainComponent } from './Components/main/main.component';
import { HomeComponent } from './Components/home/home.component';
import {AppRoutingModule} from "./app-routing.module";
import {GetDataService} from "./services/get-data.service";
import {MockGetDataService} from "./services/mock-get-data.service";
import {PostDataService} from "./services/post-data.service";
import { ConferencesComponent } from './Components/conferences/conferences.component';
import {ConstructorModule} from "./constructor/constructor.module";
import { ConferenceCardComponent } from './Components/conferences/conference-card/conference-card.component';
import {StoreService} from "./services/store.service";
import {StoreConferencesService} from "./services/store-conferences.service";
import {LocationStrategy, PathLocationStrategy} from "@angular/common";
import {AmazingTimePickerModule} from "amazing-time-picker";
import { TimeInputComponent } from './Components/time-input/time-input.component';

const appRoutes: Routes = [
  { path: 'login', component: LoginComponent},
  { path: 'signUp', component: SignUpComponent},
  { path: '**', component: LoginComponent}

];

@NgModule({
  declarations: [
    AppComponent,
    LoginComponent,
    SignUpComponent,
    CompareFormControlDirective,
    MainComponent,
    HomeComponent,
    ConferencesComponent,
    ConferenceCardComponent
  ],
  imports: [
    BrowserModule,
    FormsModule,
    BrowserAnimationsModule,
    MatButtonModule,
    MatFormFieldModule,
    ReactiveFormsModule,
    MatInputModule,
    HttpClientModule,
    AppRoutingModule,
    ConstructorModule,
    NavBarModule,
    MatProgressSpinnerModule
  ],
  providers: [
    EnsureAuthenticatedService,
    PostDataService,
    StoreService,
    StoreConferencesService,
    {provide: LocationStrategy, useClass:PathLocationStrategy},
    {
    provide: HTTP_INTERCEPTORS,
    useClass: AuthInterceptorService,
    multi: true
  }],
  bootstrap: [AppComponent]
})
export class AppModule { }
