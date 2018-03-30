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

const appRoutes: Routes = [
  { path: 'login', component: LoginComponent},
  { path: 'signUp', component: SignUpComponent}
];

@NgModule({
  declarations: [
    AppComponent,
    LoginComponent,
    SignUpComponent,
    CompareFormControlDirective
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
    RouterModule.forRoot(appRoutes)
  ],
  providers: [ {
    provide: HTTP_INTERCEPTORS,
    useClass: AuthInterceptorService,
    multi: true
  }],
  bootstrap: [AppComponent]
})
export class AppModule { }
