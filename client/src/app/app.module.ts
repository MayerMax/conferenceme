import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';


import { AppComponent } from './app.component';
import {FormsModule, ReactiveFormsModule} from "@angular/forms";
import {MatButtonModule, MatFormFieldModule, MatInputModule} from "@angular/material";
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
    HomeComponent
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
    NavBarModule,
    AppRoutingModule
  ],
  providers: [
    EnsureAuthenticatedService,
    PostDataService,
    {
    provide: HTTP_INTERCEPTORS,
    useClass: AuthInterceptorService,
    multi: true
  }],
  bootstrap: [AppComponent]
})
export class AppModule { }
